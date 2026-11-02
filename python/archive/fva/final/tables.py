import sys; sys.path.insert(0, '/home/claude/fva/final')
from fva_final import *
L = load_all('1h'); old, news, mo_o, mo_n = L; MO = mo_o + mo_n
print('months', round(mo_o, 1), round(mo_n, 1))
def row(kw, label=None):
    df, _, _ = run(L, **kw)
    s = stats(df, MO); sn = stats(df[df.period == 'new'], mo_n); so = stats(df[df.period == 'old'], mo_o)
    s['t 2022-25'] = so.get('t-score'); s['2026 trades'] = sn.get('Trades', 0); s['2026 $'] = df[df.period == 'new'].usd.sum()
    s['$/mo @DD$1000'] = s['$/Month'] / s['MaxDD$'] * 1000 if s.get('MaxDD$') else np.nan
    return s, df
OUT = {}
TG = [1, 1.5, 2, 3, 4, 6, None]
def tg_name(t): return 'no target' if t is None else f'1:{t:g}'
for setup, base, stops, exits in [
        ('A', dict(etypes={'FailC'}, side='long'), ['atr1', 'fix'], ['XH', 'X0', 'XN2W']),
        ('B', dict(etypes={'Fail+C'}, sess={'Asia 18-02'}), ['fix', 'box'], ['XSA', 'X0', 'XN2W'])]:
    rows = []
    for stp in stops:
        for ex in exits:
            for t in TG:
                s, _ = row(dict(base, stop=stp, rk=t, ex=ex))
                rows.append(dict(Stop=stp, Exit=ex, Target=tg_name(t), **s))
    OUT[setup] = pd.DataFrame(rows)
# steps
steps = {'A': [('1 · every FVA box fail (long + short, all sessions)', dict(etypes={'FailC'})),
               ('2 · + long only (FINAL)', dict(etypes={'FailC'}, side='long'))],
         'B': [('1 · every flip-zone fail (long + short, all sessions)', dict(etypes={'Fail+C'})),
               ('2 · + Asia 18:00–02:00 only (FINAL)', dict(etypes={'Fail+C'}, sess={'Asia 18-02'}))]}
fin = {'A': dict(stop='atr1', rk=6, ex='XH'), 'B': dict(stop='fix', rk=1.5, ex='XSA')}
SR = []
for k, lst in steps.items():
    for lab, kw in lst:
        s, _ = row(dict(kw, **fin[k])); SR.append(dict(Setup=k, Step=lab, **s))
OUT['steps'] = pd.DataFrame(SR)
# finals + trade lists + random baselines
FIN = []
for k in 'AB':
    kw = dict(etypes={'FailC'}, side='long') if k == 'A' else dict(etypes={'Fail+C'}, sess={'Asia 18-02'})
    s, df = row(dict(kw, **fin[k])); df.to_csv(f'/home/claude/fva/final/trades_{k}.csv', index=False)
    s['Setup'] = k
    s['avg win RR'] = df[df.R > 0].R.mean(); s['avg loss RR'] = df[df.R <= 0].R.mean()
    s['years'] = ' | '.join(f"{y}: {g.R.mean():+.2f} ({len(g)})" for y, g in df.groupby(df.t.dt.year))
    s['exits'] = df.how.value_counts().to_dict()
    FIN.append(s)
OUT['final'] = pd.DataFrame(FIN)
# random baseline: random closes, same side / session / stop / target / exit
rng = np.random.default_rng(5)
RB = []
for k in 'AB':
    vals = []
    for C in [old] + news:
        n = len(C['c']); J = rng.choice(np.arange(20, n - 1), size=n // 3, replace=False)
        ss = []
        for j in J:
            lg = True if k == 'A' else bool(rng.random() < .5)
            ss.append(dict(etype='RND', long=lg, t=C['sig'].index[j], ep=C['c'][j], sl=np.nan, swing=np.nan, tgt=None, mkt=True))
        C2 = dict(C, ss=ss)
        kw = dict(etypes={'RND'}, side='long') if k == 'A' else dict(etypes={'RND'}, sess={'Asia 18-02'})
        vals.append(one_at_a_time(trades(C2, **kw, **fin[k])))
    df = pd.concat(vals); RB.append(dict(Setup=k, **stats(df, MO)))
OUT['random'] = pd.DataFrame(RB)
pd.to_pickle(OUT, '/home/claude/fva/final/tables.pkl')
pd.set_option('display.width', 320); pd.set_option('display.max_columns', 40); pd.set_option('display.max_rows', 200)
for k, v in OUT.items():
    print('\n==', k); print(v.round(2).to_string(index=False))
