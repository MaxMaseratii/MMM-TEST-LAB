import json, html, numpy as np, pandas as pd
P=json.load(open('page.json'))
esc=html.escape
def sg(x,p=2): return '—' if x is None else (f'{x:+.{p}f}')
def pc(x): return '—' if x is None else f'{x*100:.0f}%'
def tone(a,b): return 'g' if (a>0 and b>0) else ('r' if (a<=0 and b<=0) else 'y')
def tbl(cols,rows,cls=''):
    h='<div class="tw"><table class="'+cls+'"><thead><tr>'+''.join(f'<th>{esc(c)}</th>' for c in cols)+'</tr></thead><tbody>'
    for t,r in rows: h+=f'<tr class="{t}">'+''.join(f'<td>{v}</td>' for v in r)+'</tr>'
    return h+'</tbody></table></div>'
STOP={'S20':'20 pts','S30':'30 pts','S50':'50 pts','Sbox':'zone edge (20–50 pts)','Szone':'zone edge (no cap)'}
TGT={'TP2':'1:2','TP3':'1:3','TP5':'1:5','TP10':'1:10','RUN':'runner'}
TRL={'':'none','BE1':'BE after 1 BC in profit','BE2':'BE after 2 BC in profit','trailBC':'under / over each new BC in profit','trailOpp':'after the 1st opposite candle, then a BC in profit → to that pullback low / high'}
ROB={'F.M1':100,'F.M2':100,'F.M3':93,'F.M4':96,'F.M5':87,'F.M6':94,'F.M7':86,'F.M8':100,'F.M9':87,'F.M10':81,'F.M11':97,'F.M12':96,'F.M13':89,'F.M14':98,'F.M15':97,'F.M16':77}
LV1={'H1 UPG':'H1 UPG gap · level held','ALL UPG gaps':'any UPG gap (M15 · H1 · H4 · D · W)','M15 UPG':'M15 UPG gap','NY PM OR L':'NY PM opening range low (13:30–13:45)',
    'ALL session / range H-L':'any session / range high or low','M15 I':'PRO f M15 internal box','ALL LEZ (any TF)':'PRO f Bu / Be LEZ · level held','ALL PRO f boxes H1':'any PRO f H1 box · level held'}
EN1={'M3 · limit at box edge':'limit at the LTF reversal box edge (1st touch fills)','M1 B · touch, then BC':'your model: retest touches the box (no close inside) → BC out → next open'}
FL1={'all':'any time','sess: NY PM 12-16':'12:00–16:00','sess: NY AM 09:30-12':'09:30–12:00','sess: London 02-08':'02:00–08:00','H1 trend: with':'with the PRO f H1 trend'}
def cards(rows,r1):
    out=''; df=pd.DataFrame(rows)
    for code,g in df.groupby('code',sort=False):
        r=g.iloc[0]; o=g[g.period=='2022–25'].iloc[0]; f=g[g.period=='2026'].iloc[0]
        if r1:
            lvl=LV1.get(r['level'],r['level']); ent=EN1.get(r['entry'],r['entry']); tm=FL1.get(r['filter'],r['filter'])
        else:
            lvl=r['level']; ent=r['entry']; tm='as written'
        spec=f'''<dl><div><dt>Entry TF</dt><dd>{r.ltf}</dd></div><div><dt>Level / signal</dt><dd>{esc(lvl)}</dd></div><div><dt>Entry</dt><dd>{esc(ent)}</dd></div>
        {'<div><dt>Time</dt><dd>'+esc(tm)+'</dd></div>' if r1 else ''}<div><dt>Stop</dt><dd>{STOP[r.stop]}</dd></div><div><dt>Close back past the zone = out</dt><dd>{'yes' if r.boxexit else 'no'}</dd></div>
        <div><dt>Target</dt><dd>{TGT[r.target]} RR</dd></div><div><dt>Trail</dt><dd>{TRL[r.trail]}</dd></div></dl>'''
        rr=[]
        for _,x in g.iterrows():
            rr.append(('b' if x.period=='Both' else '',[x.period,int(x.trades),f'{x.per_month:.1f}',pc(x.WR),f'{x.PF:.2f}',sg(x.avgRR),f'{x.t:.1f}',sg(x.netRR,1),
                f'W: +${x.won_usd:,.0f} · L: −${-x.lost_usd:,.0f} · Net: ${x.net_usd:,.0f}',f'{x.maxDD_RR:.1f}',f'{int(x.max_wins)} / {int(x.max_losses)}']))
        out+=f'''<article class="card {tone(o.avgRR,f.avgRR)}"><header><h3>{code}</h3><span class="pass">PASS · {ROB[code]}% of settings + in both</span></header>{spec}
        {tbl(['Period','Trades','Trades / month','WR = win rate','PF = profit factor','avg RR','t-score','Net RR','Money (1 MNQ)','Max DD (RR)','Max wins / losses in a row'],rr,'st')}</article>'''
    return out
# ── back inside table
B=pd.DataFrame(P['backin']); rows=[]
for (tf,grp),g in B.groupby(['tf','grp']):
    for per in ('old','fresh'):
        s=g[(g.per==per)&(g['after the break']=='stayed outside')].iloc[0]; c=g[(g.per==per)&(g['after the break']=='closed back inside')].iloc[0]
        rows.append(('',[tf,grp,'2022–25' if per=='old' else '2026',f'{int(s.n)} / {int(c.n)}',
            f'<b class="up">{pc(s["P(next break = same way)"])}</b> vs {pc(c["P(next break = same way)"])}',
            f'{pc(s["P(close through far edge)"])} vs <b class="dn">{pc(c["P(close through far edge)"])}</b>',
            f'<b class="up">{s["median MFE pts"]:.0f}</b> vs {c["median MFE pts"]:.0f}',f'{s["median MAE pts"]:.0f} vs <b class="dn">{c["median MAE pts"]:.0f}</b>']))
tf_order={'1m':0,'5m':1,'15m':2,'1h':3}
rows=sorted(rows,key=lambda r:(tf_order[r[1][0]],r[1][1],r[1][2]))
backin=tbl(['TF','Break','Period','Breaks (outside / back inside)','Next break the same way','Closes through the far edge (deeper pullback)','Median move with the break (pts)','Median move against (pts)'],rows)
# ── foundations
Fd=pd.DataFrame(P['found']); rows=[]
for _,r in Fd.sort_values(['tf','grp','per'],key=lambda s:s.map(tf_order) if s.name=='tf' else s).iterrows():
    rows.append(('',[r.tf,r.grp,'2022–25' if r.per=='old' else '2026',int(r.n),f'{r.bc_opp:.2f}',f'{r.bc_nbc:.2f}',pc(r.opp_next),f'{r.mfe:.1f}',f'{r.mfe_med:.1f}',pc(r.p_cont),pc(r.p_backin)]))
found=tbl(['TF','Break','Period','Breaks','Avg BCs before an opposite BC','Avg BCs before the 1st NBC','Opposite BC straight away','Avg pts before the opposite BC','Median pts','Next break the same way','Closes back inside before the next break'],rows)
# ── retest sequences / validation / areas
def cmp(key,label):
    D=pd.DataFrame(P[key]); rows=[]
    for _,r in D.sort_values(['ltf',key if key!='valid' else 'valid'],key=lambda s:s.map(tf_order) if s.name=='ltf' else s).iterrows():
        nm=r['seq'] if key=='seq' else r['valid'] if key=='valid' else r['area']
        rows.append(('g' if r.both>=0.3 else ('r' if r.both<0.06 else 'y'),[r.ltf,esc(nm),sg(r.o,3),sg(r.f,3),pc(r.both)]))
    return tbl(['Entry TF',label,'Median avg RR 2022–25','Median avg RR 2026','% settings + in both'],rows)
seq=cmp('seq','Retest sequence (after the touch)'); val=cmp('valid','Validation before the retest'); area=cmp('area','Entry area')
# ── order flow entries
O=pd.DataFrame(P['of']); rows=[]
for _,r in O.sort_values(['tf','break','entry'],key=lambda s:s.map(tf_order) if s.name=='tf' else s).iterrows():
    rows.append(('g' if r.both>=0.6 else ('r' if r.both<0.1 else 'y'),[r.tf,r['break'],esc(r.entry),int(r.n_o),int(r.n_f),pc(r.both),sg(r.o_med,3),sg(r.f_med,3)]))
of=tbl(['TF','Break','Entry','Trades 22–25','Trades 2026','% settings + in both','Median avg RR 22–25','Median avg RR 2026'],rows)
c1=cards(P['s1'],True); c2=cards(P['s2'],False)
s3=pd.read_parquet('strats3.parquet').replace([np.inf],999); s3=s3[s3.code=='F.M16']
TRL['BE+fees after 1 BC · 3 re-entries']='BE + fees after the 1st BC in profit · re-enter up to 3 times (touch → BC out) while the box holds'
c3=cards(s3.to_dict('records'),False)
Mg=pd.read_parquet('mgmt_page.parquet'); Mg.columns=['_'.join([c for c in col if c]) if isinstance(col,tuple) else col for col in Mg.columns]
rows=[]
for _,r in Mg[(Mg.target=='RUN')&(Mg.ltf.isin(['1m','5m']))].sort_values(['ltf','level','mgmt','reentry']).iterrows():
    rows.append((tone(r.avg_setup_old,r.avg_setup_fresh),[r.ltf,r.level,r.mgmt,r.reentry,sg(r.avg_setup_old,3),sg(r.avg_setup_fresh,3),pc(r.no_loss_old),pc(r.no_loss_fresh),f'{r.trades_per_setup_old:.2f}']))
mg=tbl(['Entry TF','HTF level','Stop to BE + fees','Re-entry','avg RR per setup 22–25','avg RR per setup 2026','Setups with no loss 22–25','Setups with no loss 2026','Trades per setup'],rows)
tpl=open('/tmp/claude-0/-home-claude/2f55ff78-2cd0-5f42-a374-6a674bbb5d06/scratchpad/lezpage/tpl.html').read()
for k,v in dict(BACKIN=backin,FOUND=found,SEQ=seq,VAL=val,AREA=area,OF=of,C1=c1,C2=c2,C3=c3,MGMT=mg).items(): tpl=tpl.replace('{{'+k+'}}',v)
open('/tmp/claude-0/-home-claude/2f55ff78-2cd0-5f42-a374-6a674bbb5d06/scratchpad/lezpage/MMM_PRO_f_Backtest.html','w').write(tpl)
print(len(tpl))
