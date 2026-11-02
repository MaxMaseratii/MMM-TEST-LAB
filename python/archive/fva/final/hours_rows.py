import sys, json; sys.path.insert(0, '/home/claude/fva/final')
from fva_final import *
L = load_all('1h'); old, news, mo_o, mo_n = L; MO = mo_o + mo_n
STL = {'atr1': 'ATR(14) × 1', 'atr15': 'ATR(14) × 1.5', 'datr': 'daily ATR × 0.15', 'fix': 'fixed 50 pts', 'box': 'box / zone edge', 'swing': 'swing'}
EXL = {'X0': 'stop / target only', 'XH': 'hold to next session open', 'XN2W': '2-NBC stall exit', 'XSA': 'Pro Plus stall exit'}
def tg(t): return 'no target' if t is None else f'1:{t:g}'
def rstats(df):
    if len(df) < 2: return None
    R = df.R.values; w = R > 0; cum = np.cumsum(R); dd = np.max(np.maximum.accumulate(np.r_[0, cum])[1:] - cum)
    mo = df.groupby(df.t.dt.to_period('M')).R.sum()
    o = df[df.period == 'old'].R; n = df[df.period == 'new'].R
    ao = o.mean() if len(o) else None; an = n.mean() if len(n) else None
    both = 'unclear' if (len(o) < 30 or len(n) < 15) else ('held' if ao > 0.05 and an > 0.05 else 'failed' if (ao <= 0 or an <= 0) else 'unclear')
    return dict(n=int(len(R)), tpm=round(len(R) / MO, 2), wr=round(w.mean(), 3), aw=round(R[w].mean(), 2) if w.any() else None, al=round(R[~w].mean(), 2) if (~w).any() else None,
                av=round(R.mean(), 3), mx=round(R.max(), 2), mw=streak(w), ml=streak(~w), pf=round(R[w].sum() / -R[~w].sum(), 2) if (~w).any() else None,
                t=round(R.mean() / R.std(ddof=1) * np.sqrt(len(R)), 2), mpos=round((mo > 0).mean(), 2), dd=round(dd, 1), both=both,
                av_old=round(ao, 2) if ao is not None else None, av_new=round(an, 2) if an is not None else None)
SET = {'A': dict(code='FVA.A', setup='A · FVA Box Fail', side='Long', session='Any session', base=dict(etypes={'FailC'}, side='long'),
                 stops=['atr1', 'atr15', 'datr', 'fix', 'box', 'swing'], fin=('atr1', 'XH', 6)),
       'B': dict(code='FVA.B', setup='B · Asia Flip Zone Fail', side='Both', session='Asia 18:00–02:00', base=dict(etypes={'Fail+C'}, sess={'Asia 18-02'}),
                 stops=['fix', 'box', 'atr1', 'datr'], fin=('fix', 'XSA', 1.5))}
rows = []
for k, S in SET.items():
    for stp in S['stops']:
        for ex in ['XH', 'X0', 'XN2W', 'XSA']:
            for t in [1, 1.5, 2, 3, 4, 6, None]:
                df, _, _ = run(L, **S['base'], stop=stp, rk=t, ex=ex)
                st = rstats(df)
                if st is None: continue
                fin = (stp, ex, t) == S['fin']
                rows.append(dict(fva=True, code=S['code'] + ('' if fin else '.v'), setup=S['setup'], filter='FINAL rules', side=S['side'], session=S['session'],
                                 stop=STL[stp], exitrule=EXL[ex], target=tg(t), final='★ final' if fin else '', **st))
    print(k, 'grid done', flush=True)
# filter steps + random for the final combo
for k, S in SET.items():
    stp, ex, t = S['fin']
    wide = dict(etypes=S['base']['etypes'])
    df, _, _ = run(L, **wide, stop=stp, rk=t, ex=ex)
    rows.append(dict(fva=True, code=S['code'] + '.wide', setup=S['setup'], filter='no filter (long + short, all sessions)', side='Both', session='Any session',
                     stop=STL[stp], exitrule=EXL[ex], target=tg(t), final='', **rstats(df)))
    rng = np.random.default_rng(5); vals = []
    for C in [old] + news:
        n = len(C['c']); J = rng.choice(np.arange(20, n - 1), size=n // 3, replace=False)
        ss = [dict(etype='RND', long=(True if k == 'A' else bool(rng.random() < .5)), t=C['sig'].index[j], ep=C['c'][j], sl=np.nan, swing=np.nan, tgt=None, mkt=True) for j in J]
        C2 = dict(C, ss=ss)
        kw = dict(etypes={'RND'}, side='long') if k == 'A' else dict(etypes={'RND'}, sess={'Asia 18-02'})
        vals.append(one_at_a_time(trades(C2, **kw, stop=stp, rk=t, ex=ex)).assign(period='old' if C is old else 'new'))
    rows.append(dict(fva=True, code=S['code'] + '.rnd', setup=S['setup'], filter='RANDOM entries (control: do not trade)', side=S['side'], session=S['session'],
                     stop=STL[stp], exitrule=EXL[ex], target=tg(t), final='', **rstats(pd.concat(vals))))
json.dump(rows, open('/home/claude/fva/final/fva.json', 'w'), ensure_ascii=False)
print(len(rows)); print([r for r in rows if r['final']])
