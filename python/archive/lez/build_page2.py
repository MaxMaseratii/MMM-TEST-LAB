import json, numpy as np, pandas as pd
P=json.load(open('page.json'))
def f(x,p=4):
    if x is None: return None
    try:
        x=float(x)
    except: return x
    if np.isnan(x): return None
    if np.isinf(x): return 999
    return round(x,p)
PER={'2022–25':'o','2026':'f','Both':'b'}
STAT=['trades','per_month','WR','PF','avgRR','t','netRR','won_usd','lost_usd','net_usd','maxDD_RR','max_wins','max_losses','avg_stop']
STOP={'S20':'20 pts','S30':'30 pts','S50':'50 pts','Sbox':'zone edge (20–50 pts)','Szone':'zone edge (no cap)'}
TGT={'TP2':'1:2','TP3':'1:3','TP5':'1:5','TP10':'1:10','RUN':'runner'}
TRL={'':'none','BE1':'BE after 1 BC in profit','BE2':'BE after 2 BC in profit','trailBC':'under / over each new BC in profit','trailOpp':'after the 1st opposite candle, then a BC in profit → to that pullback low / high',
     'BE+fees after 1 BC · 3 re-entries':'BE + fees after the 1st BC in profit · re-enter up to 3 times (touch → BC out) while the box holds'}
LV1={'H1 UPG':'H1 UPG gap · level held','ALL UPG gaps':'any UPG gap (M15 · H1 · H4 · D · W)','M15 UPG':'M15 UPG gap','NY PM OR L':'NY PM opening range low (13:30–13:45)',
    'ALL session / range H-L':'any session / range high or low','M15 I':'PRO FVA M15 internal box','ALL LEZ (any TF)':'PRO FVA Bu / Be LEZ · level held','ALL PRO FVA boxes H1':'any PRO FVA H1 box · level held'}
EN1={'M3 · limit at box edge':'limit at the LTF reversal box edge (1st touch fills)','M1 B · touch, then BC':'retest touches the box (no close inside) → BC out → next open'}
FL1={'all':'any time','sess: NY PM 12-16':'12:00–16:00','sess: NY AM 09:30-12':'09:30–12:00','sess: London 02-08':'02:00–08:00','H1 trend: with':'with the PRO FVA H1 trend'}
ROB={'FVA.M1':100,'FVA.M2':100,'FVA.M3':93,'FVA.M4':96,'FVA.M5':87,'FVA.M6':94,'FVA.M7':86,'FVA.M8':100,'FVA.M9':87,'FVA.M10':81,'FVA.M11':97,'FVA.M12':96,'FVA.M13':89,'FVA.M14':98,'FVA.M15':97,'FVA.M16':77}
S=[]
def add(df,rnd,txt):
    for code,g in pd.DataFrame(df).groupby('code',sort=False):
        r=g.iloc[0]; d=dict(code=code,round=rnd,ltf=r.ltf,**txt(r),stop=STOP.get(r.stop,r.stop),boxexit=bool(r.boxexit) and r.boxexit!='',target=TGT.get(r.target,r.target),trail=TRL.get(r.trail,r.trail))
        d['rob']=ROB.get(code)
        for _,x in g.iterrows(): d[PER[x.period]]={k:f(x[k]) for k in STAT+['no_loss','full_loss'] if k in x and x[k] is not None}
        S.append(d)
add(P['s1'],'Round 1 · HTF level → LTF box',lambda r:dict(level=LV1.get(r.level,r.level)+(' · level held' if r.held=='held' and 'held' not in LV1.get(r.level,'') else ''),entry=EN1.get(r.entry,r.entry),time=FL1.get(r['filter'],r['filter']),setup=None))
add(P['s2'],'Round 2 · close back inside + refined retest',lambda r:dict(level=r.level,entry=r.entry,time='as written',setup=None))
s3=pd.read_parquet('strats3.parquet'); s3=s3[s3.code=='FVA.M16']
add(s3.to_dict('records'),'Round 2 · your management',lambda r:dict(level=r.level,entry=r.entry,time='any time',setup='per setup'))
s4=pd.read_parquet('strats4.parquet')
TX={'FVA.M17':('any UPG gap (M15 · H1 · H4 · D · W) touched, level held → 15m reversal box','retest that only wicks the box (no close inside) → 1st BC out of the box → enter at the next open'),
    'FVA.M18':('M15 UPG gap touched, level held → 15m reversal box','retest that only wicks the box → 1st BC out → limit at the high / low that BC broke'),
    'FVA.M19':('any PRO FVA break box (CDL · CDS · LD · SD on M15 / H1 / H4) touched → 5m reversal box that has an NBC inside','retest → 1st BC out → enter at the next open'),
    'FVA.M20':('any UPG gap touched, level held → 15m reversal box','the break candle is followed straight away by the retest (no BC, NBC or opposite candle in between) → 1st BC out → next open'),
    'FVA.M21':('M15 UPG gap touched → 5m reversal box','break → an NBC → then the retest → 1st BC out → next open · after a stop, re-enter once on touch → BC out while the box holds'),
    'FVA.M22':('PRO FVA M15 internal box touched → 1m reversal box','break → 2nd BC, NBC and an opposite candle → retest closes inside the box → 1st BC out → next open')}
L4=s4.to_dict('records')
for r in L4:
    c=r['cfg'].split(' | ')
    if r['kind']=='s2': r.update(stop=c[0],boxexit=c[1],target=c[2],trail=c[3])
    else: r.update(stop=c[0],boxexit='',target=c[1],trail=('none' if c[2]=='no BE' else c[2])+' · '+c[3])
s4=pd.DataFrame(L4)
for code,g in s4.groupby('code',sort=False):
    r=g.iloc[0]; d=dict(code=code,round='Round 3 · pre-touch sequence + retest + 1st BC',ltf=r.ltf,level=TX[code][0],entry=TX[code][1],time='any time',setup=None,
        stop=STOP[r.stop],boxexit=r.boxexit=='+box exit',target=TGT[r.target],trail=TRL.get(r.trail,r.trail),rob=round(r.rob*100))
    for _,x in g.iterrows(): d[PER[x.period]]={k:f(x[k]) for k in STAT+['no_loss','full_loss']}
    S.append(d)
# ── explorer table7
def pack(df,cols):
    out={'cols':cols,'rows':[],'dict':{}}
    for c in cols:
        if df[c].dtype==object or str(df[c].dtype).startswith('str') or str(df[c].dtype)=='string': out['dict'][c]=sorted(df[c].astype(str).unique().tolist())
    idx={c:{v:i for i,v in enumerate(out['dict'][c])} for c in out['dict']}
    for row in df[cols].itertuples(index=False):
        out['rows'].append([idx[c][str(v)] if c in idx else f(v,3) for c,v in zip(cols,row)])
    return out
T=pd.read_parquet('table7.parquet'); T=T[(T.n_o>=60)]
C7=['ltf','level','pre','touch','box','area','held','n_o','n_f','both','o_med','f_med','best_cfg','best_b_wr','best_o_avg','best_f_avg','best_b_pf','best_b_t','best_b_dd','best_b_net','max_b_wr','max_o_avg','max_f_avg','max_b_pf']
X7=pack(T,C7)
M=pd.read_parquet('table7m.parquet')
CM=['ltf','level','pre','touch','box','held','n_o','n_f','both','o_med','f_med','best_cfg','best_b_wr','best_o_avg','best_f_avg','best_b_pf','best_b_t','best_b_dd','mg1_o_avg','mg1_f_avg','mg2_o_avg','mg2_f_avg','mg1r_o_avg','mg1r_f_avg']
M7=pack(M,CM)
T3=pd.read_parquet('table3.parquet'); T3=T3[(T3['filter']=='all')]
C3=['ltf','level','valid','seq','area','held','n_o','n_f','both','o_med','f_med','best_cfg','best_b_wr','best_o_avg','best_f_avg','best_b_pf','best_b_t','best_b_dd']
X3=pack(T3,C3)
R=pd.read_parquet('retest7.parquet')
FIRST={'0':'box broke straight away (no retest)','1':'2nd BC (same way)','2':'NBC','3':'opposite BC'}
F2={'1':'2nd BC','2':'NBC','3':'opp BC','0':'—'}
def vname(dim,v):
    if dim=='all': return 'all boxes'
    if dim=='first': return FIRST[str(int(float(v)))]
    if dim=='boxtype': return {'1':'BC on BC (no NBC)','2':'box with NBC'}[str(int(float(v)))]
    a,b=v[0],v[1]
    if a=='0': return 'box broke straight away'
    if b=='0': return F2[a]+' → '+('entry right away' if a=='1' else 'box broke')
    return F2[a]+' → '+F2[b]
R['name']=[vname(d,v) for d,v in zip(R.dim,R.val)]
R=R.pivot_table(index=['ltf','L','dim','name'],columns='per',values=['n','retest','entry','bars']).reset_index()
R.columns=['_'.join([c for c in col if c]) for col in R.columns]
R=R[R.n_old>=40]
RT=pack(R,['ltf','L','dim','name','n_old','n_fresh','retest_old','retest_fresh','entry_old','entry_fresh','bars_old','bars_fresh'])
BI=P['backin']; OF=P['of']; FD=P['found']
Mg=pd.read_parquet('mgmt_page.parquet'); Mg.columns=['_'.join([c for c in col if c]) if isinstance(col,tuple) else col for col in Mg.columns]
MG=[{k:f(v) for k,v in r.items()} for r in Mg.to_dict('records')]
W8=pd.read_parquet('post8.parquet'); W8=W8[W8.n_old>=30].copy()
PS=pack(W8,['tf','L','firstN','nxN','nx','n_old','n_fresh','share_old','share_fresh','entry_old','entry_fresh','broke_old','broke_fresh','wr50_old','wr50_fresh','av50_old','av50_fresh','wrbx_old','wrbx_fresh','avbx_old','avbx_fresh'])
D=dict(S=S,X7=X7,M7=M7,X3=X3,RT=RT,BI=BI,OF=OF,FD=FD,MG=MG,PS=PS)
js=json.dumps(D,ensure_ascii=False,separators=(',',':'),default=lambda o:f(o))
open('page2.json','w').write(js); print(len(js), len(X7['rows']), len(M7['rows']), len(X3['rows']), len(RT['rows']), len(S))
