import json, pandas as pd, numpy as np
D=json.load(open('sheet.json'))
STOP={'S20':'20 pts','S30':'30 pts','S50':'50 pts','Sbox':'box (20–50)'}
TGT={'TP2':'1:2','TP3':'1:3','TP5':'1:5','TP10':'1:10','RUN':'runner'}
TRL={'':'none','BE1':'BE after 1 BC','BE2':'BE after 2 BC','trailBC':'under each BC','trailOpp':'after 1st opp candle'}
BX={'+box exit':'yes','':'no'}
def f(x,p=2,pct=False,sign=False):
    if x is None or (isinstance(x,float) and np.isnan(x)): return '—'
    if pct: return f'{x*100:.0f}%'
    s=f'{x:+.{p}f}' if sign else f'{x:.{p}f}'
    return s
def tone(a,b): return 'g' if (a>0 and b>0) else ('r' if (a<=0 and b<=0) else 'y')
tabs=[]
# ── 1. strategies
S=pd.DataFrame(D['strats']); rows=[]
for code,g in S.groupby('code',sort=False):
    o=g[g.period=='2022–25'].iloc[0]; fr=g[g.period=='2026'].iloc[0]
    for _,r in g.iterrows():
        rows.append({'t':tone(o.avgRR,fr.avgRR),'c':[code,r.ltf,r.level,r.entry,'held' if r.held=='held' else 'any',r['filter'].replace('sess: ','').replace('all','—'),
            STOP[r.stop],BX[r.boxexit],TGT[r.target],TRL[r.trail],r.period,int(r.trades),f(r.per_month,1),f(r.WR,pct=True),f(r.PF),f(r.avgRR,2,sign=True),f(r.t,1),
            f(r.netRR,1,sign=True),f'+${r.won_usd:,.0f}',f'−${-r.lost_usd:,.0f}',f'${r.net_usd:,.0f}',f(r.maxDD_RR,1),int(r.max_wins),int(r.max_losses),f(r.avg_stop,1)]})
tabs.append(dict(id='best',name='Best strategies',note='Each strategy = one HTF level + one LTF entry + one stop/exit. 3 rows each: 2022–25 (NQ 1m) → 2026 (MNQ 1m) → Both. Money = 1 MNQ ($2/pt), 1 pt cost per trade taken off. Green = PASS (made money in both periods). Pick ONE, study it, backtest it yourself before trading it.',
  cols=['Strategy','Entry TF','HTF level','Entry','Level','Time / filter','Stop','Close past box = out','Target','Trail','Period','Trades','Trades / month','WR','PF','avg RR','t-score','Net RR','Won','Lost','Net $ (1 MNQ)','Max DD (RR)','Max wins in a row','Max losses in a row','Avg stop pts'],rows=rows))
# ── 2. your model
Y=pd.DataFrame(D['yours']); rows=[]
for _,r in Y.sort_values(['ltf','level','target','trail']).iterrows():
    rows.append({'t':tone(r.o_avg,r.f_avg),'c':[r.ltf,r.level,TGT[r.target],TRL[r.trail],int(r.o_n),f(r.o_wr,pct=True),f(r.o_avg,2,True),f(r.o_pf),f(r.o_t,1),int(r.f_n),f(r.f_wr,pct=True),f(r.f_avg,2,True),f(r.f_t,1)]})
tabs.append(dict(id='yours',name='Your model by level',note='Your exact model: HTF level touched (and HELD: no close through it) → first reversal box on the LTF → proper retest (not the break candle) → 2nd BC closes outside the box → enter at the next candle open. Stop = box edge, 20–50 pts. Close back past the box = out. Shown with 1:2, 1:5, runner + BE after 2 BC, runner + trail after the 1st opposite candle.',
  cols=['Entry TF','HTF level','Target','Trail','Trades 22–25','WR 22–25','avg RR 22–25','PF 22–25','t 22–25','Trades 2026','WR 2026','avg RR 2026','t 2026'],rows=rows))
# ── 3. entry models + retest types
E=pd.DataFrame(D['entries']); rows=[]
for _,r in E.iterrows():
    rows.append({'t':tone(r['median avg RR 2022–25'],r['median avg RR 2026']),'c':[r.ltf,r.entry,f(r['median avg RR 2022–25'],3,True),f(r['median avg RR 2026'],3,True),f(r['% settings + in both'],0)+'%',f(r['best avg RR 2022–25'],2,True)]})
tabs.append(dict(id='entries',name='Entry models',note='All level groups together. "Median avg RR" = the middle result over every stop × exit × trail setting (200 settings). "% settings + in both" = how many settings made money in BOTH periods. M1 = your retest + 2nd BC model, split by retest type.',
  cols=['Entry TF','Entry model','Median avg RR 2022–25','Median avg RR 2026','% settings + in both','Best avg RR 2022–25'],rows=rows))
# ── 4. levels
L=pd.DataFrame(D['levels']); rows=[]
for _,r in L.iterrows():
    rows.append({'t':'g' if r.both>=80 else ('r' if r.both<=20 else 'y'),'c':[r.ltf,r.level,r.entry,int(r.n_o),int(r.n_f),f(r.both,0)+'%',f(r.o_med,3,True),f(r.f_med,3,True),f(r.o_best,2,True)]})
tabs.append(dict(id='levels',name='Levels × entries',note='Every HTF level with every entry model (no time filter). "% settings + in both" = share of the 70 stop/exit settings that made money in BOTH periods: the robustness test. Green ≥ 80%, red ≤ 20%. Type in the box to filter (e.g. "UPG", "LEZ", "PDH").',
  cols=['Entry TF','HTF level','Entry model','Trades 22–25','Trades 2026','% settings + in both','Median avg RR 22–25','Median avg RR 2026','Best avg RR 22–25'],rows=rows))
# ── 5. sessions & trend
Q=pd.DataFrame(D['filters']); rows=[]
for _,r in Q.sort_values(['level','ltf','entry','filter']).iterrows():
    rows.append({'t':'g' if r.both>=80 else ('r' if r.both<=20 else 'y'),'c':[r.ltf,r.level,r.entry,r['filter'].replace('sess: ',''),int(r.n_o),int(r.n_f),f(r.both,0)+'%',f(r.o_med,3,True),f(r.f_med,3,True)]})
tabs.append(dict(id='filters',name='Sessions & trend',note='Same groups split by the entry time (New York) and by the PRO f trend on H1 / M15 at entry ("with" = trade in the trend direction).',
  cols=['Entry TF','HTF level','Entry model','Time / trend','Trades 22–25','Trades 2026','% settings + in both','Median avg RR 22–25','Median avg RR 2026'],rows=rows))
# ── 6. exits
X=pd.DataFrame(D['exits']); rows=[]
for _,r in X.sort_values(['ltf','entry','o'],ascending=[True,True,False]).iterrows():
    rows.append({'t':tone(r.o,r.f),'c':[r.ltf,r.entry,STOP[r.stop],BX[r.boxexit],TGT[r.target],TRL[r.trail],f(r.wr_o,pct=True),f(r.o,3,True),f(r.f,3,True)]})
tabs.append(dict(id='exits',name='Stops & exits',note='Every stop × exit × trail, average over all level groups, for your model (M1) and the box-edge limit (M3).',
  cols=['Entry TF','Entry model','Stop','Close past box = out','Target','Trail','WR 22–25','avg RR 22–25','avg RR 2026'],rows=rows))
# ── 7. foundations
Fd=pd.DataFrame(D['found']); rows=[]
for _,r in Fd.sort_values(['group','ltf','period']).iterrows():
    rows.append({'t':'n','c':[r.group,r.ltf,'2026' if r.period=='fresh' else '2022–25',int(r.breaks),f(r['avg BCs before opp BC']),f(r['avg BCs before 1st NBC']),f(r['% opp BC next (0 BCs)'],pct=True),f(r['avg pts max move before opp BC'],1),f(r['median pts'],1),f(r['avg pts at the opp BC close'],1,True)]})
tabs.append(dict(id='found',name='Break foundations',note='The reversal box break on the LTF after the HTF level touch: how many BCs follow in the same direction before the first opposite BC, and before the first NBC, and how many points price moves before that opposite BC.',
  cols=['HTF level group','LTF','Period','Breaks','Avg BCs before opposite BC','Avg BCs before 1st NBC','Opposite BC straight away','Avg pts max move','Median pts max move','Avg pts at the opposite BC close'],rows=rows))
json.dump(tabs,open('/tmp/claude-0/-home-claude/2f55ff78-2cd0-5f42-a374-6a674bbb5d06/scratchpad/lezsheet/tabs.json','w'),ensure_ascii=False)
print([ (t['name'],len(t['rows'])) for t in tabs])
