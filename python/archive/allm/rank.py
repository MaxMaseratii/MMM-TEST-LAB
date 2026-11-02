import pickle, json, numpy as np, pandas as pd, glob
import grid
D = pd.read_parquet('grid_all.parquet')
D.loc[D.n1 < 10, 't1'] = np.nan; D.loc[D.n2 < 10, 't2'] = np.nan
sig = pd.concat([pd.read_parquet(f) for f in glob.glob('sig_*_*.parquet')], ignore_index=True)
TF = sig.groupby('strat').tf.agg(lambda x: x.mode().iloc[0]).to_dict()
NRR = sig.groupby('strat').nrr.agg(lambda x: x.mode().iloc[0] if x.notna().any() else np.nan).to_dict()
for k in ('1m', '5m', '15m', '1h', '4h'): TF['RANDOM ' + k] = k
def tidx(r):
    if r != r: return 6
    return int(np.argmin(np.abs(grid.TGT - r)))
N1, N2 = 30, 20
D['ok'] = (D.n1 >= N1) & (D.n2 >= N2)
D['pass'] = D.ok & (D.t1 >= 2) & (D.t2 >= 2)
D['mint'] = np.where(D.ok, np.fmin(D.t1, D.t2), np.nan)
out = []
for (mk, s, sd), g in D.groupby(['market', 'strat', 'side']):
    tf = TF.get(s, '')
    r = dict(market=mk, strat=s, tf=tf, side=['BULL', 'BEAR'][sd])
    nat = g[(g.e == 0) & (g.st == 0) & (g.t == tidx(NRR.get(s, np.nan))) & (g.x == 0)]
    if len(nat):
        x = nat.iloc[0]; r.update(nat_n1=x.n1, nat_avg1=x.avg1, nat_t1=x.t1, nat_n2=x.n2, nat_avg2=x.avg2, nat_t2=x.t2, nat_wr1=x.wr1, nat_wr2=x.wr2)
    fx = g[(g.e == 1) & (g.st == 1) & (g.t == 2) & (g.x == 0)]
    if len(fx):
        x = fx.iloc[0]; r.update(fx_n1=x.n1, fx_avg1=x.avg1, fx_t1=x.t1, fx_n2=x.n2, fx_avg2=x.avg2, fx_t2=x.t2)
    ok = g[g.ok]
    r['combos'] = len(ok); r['passes'] = int(g['pass'].sum())
    if len(ok):
        b = ok.sort_values('mint', ascending=False).iloc[0]
        r.update(b_e=int(b.e), b_st=int(b.st), b_t=int(b.t), b_x=int(b.x), b_n1=b.n1, b_wr1=b.wr1, b_pf1=b.pf1, b_avg1=b.avg1, b_t1=b.t1,
                 b_n2=b.n2, b_wr2=b.wr2, b_pf2=b.pf2, b_avg2=b.avg2, b_t2=b.t2)
        w = ok.sort_values('t1', ascending=False).head(20)
        r.update(wf_avg1=w.avg1.mean(), wf_avg2=w.avg2.mean(), wf_pos=(w.avg2 > 0).mean())
    out.append(r)
R = pd.DataFrame(out)
# luck: pass rate of the RANDOM grid of the same market / tf / side
rnd = R[R.strat.str.startswith('RANDOM')].set_index(['market', 'tf', 'side'])
R['luck_rate'] = [rnd.passes.get((a, b, c), np.nan) / max(rnd.combos.get((a, b, c), 1), 1) if (a, b, c) in rnd.index else np.nan for a, b, c in zip(R.market, R.tf, R.side)]
R['luck'] = R.luck_rate * R.combos
R.to_parquet('rank_all.parquet')
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 400)
print(R[['market', 'strat', 'side', 'combos', 'passes', 'luck', 'nat_avg1', 'nat_avg2', 'b_avg1', 'b_avg2', 'b_t1', 'b_t2', 'wf_avg2']].round(3).to_string())
