import pandas as pd, numpy as np
A = pd.read_parquet('xb_filter_trades.parquet')
DIMS = ['loc', 'xbdir', 'lastbrk', 'lastkind', 'infva']
def ms(r): 
    r = np.asarray(r, float); n = len(r)
    return n, (r.mean() if n else np.nan), (r.std(ddof=1) if n > 1 else np.nan)
rows = []
for (rule, strat), g in A.groupby(['rule', 'strat']):
    for h in ['1h', '4h', 'D']:
        for dim in DIMS:
            col = f'{h}|{dim}'
            for val in g[col].unique():
                if val == 'n/a': continue
                r = dict(rule=rule, strat=strat, htf=h, dim=dim, val=val)
                for per in (0, 1):
                    gp = g[g.per == per]; k = gp[col] == val
                    nk, mk, sk = ms(gp.R[k]); nd, md, sd = ms(gp.R[~k]); nb, mb, sb = ms(gp.R)
                    r[f'n{per}'] = nk; r[f'keep{per}'] = mk; r[f'drop{per}'] = md; r[f'base{per}'] = mb
                    r[f'tk{per}'] = mk / sk * np.sqrt(nk) if nk > 2 and sk > 0 else np.nan
                    r[f'tdiff{per}'] = (mk - md) / np.sqrt(sk**2 / nk + sd**2 / nd) if nk > 2 and nd > 2 else np.nan
                    r[f'share{per}'] = nk / nb if nb else np.nan
                rows.append(r)
F = pd.DataFrame(rows); F.to_parquet('xb_filter_tab.parquet')
F['better_both'] = (F.keep0 > F.base0) & (F.keep1 > F.base1)
F['strong'] = F.better_both & (F.tdiff0 >= 2) & (F.tdiff1 >= 2) & (F.n0 >= 30) & (F.n1 >= 20)
F['pass_kept'] = (F.tk0 >= 2) & (F.tk1 >= 2) & (F.n0 >= 30) & (F.n1 >= 20)
B = F[(F.rule == 'BOOK') & (F.n0 >= 30) & (F.n1 >= 15)]
P = B.groupby(['htf', 'dim', 'val']).agg(strats=('strat', 'size'), better_both=('better_both', 'mean'), strong=('strong', 'sum'),
        d0=('keep0', lambda s: np.nan), mean_gain0=('keep0', 'mean'), mean_base0=('base0', 'mean'), mean_gain1=('keep1', 'mean'), mean_base1=('base1', 'mean'),
        share=('share0', 'mean')).reset_index()
P['gain0'] = P.mean_gain0 - P.mean_base0; P['gain1'] = P.mean_gain1 - P.mean_base1
pd.set_option('display.width', 250)
print(P.drop(columns=['d0']).sort_values(['htf', 'dim', 'val']).round(3).to_string(index=False))
print('\nSTRONG (kept beats base both periods, difference t>=2 both):')
print(F[F.strong].sort_values('tdiff1', ascending=False)[['rule', 'strat', 'htf', 'dim', 'val', 'n0', 'n1', 'base0', 'keep0', 'base1', 'keep1', 'tdiff0', 'tdiff1', 'tk0', 'tk1']].round(3).to_string(index=False))
