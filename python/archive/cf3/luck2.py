import sys, numpy as np, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, '/home/claude/mmmlab')
from mmmlab import propsim as PS
days = pd.bdate_range('2024-01-02', periods=500)
def one(a):
    ev, n, seed, tpd = a
    p = (1 + ev) / 3; rng = np.random.default_rng(seed)
    te = np.repeat(days.values, tpd); r = np.where(rng.random(len(te)) < p, 2.0, -1.0)
    out = PS.slots(pd.DataFrame({'te': te, 'r': r}), risk_usd=500, n=n, eval_cost=25, activation=79, cap=2000, max_pays=6)
    return out['net'], out['paid']
if __name__ == '__main__':
    with Pool(8) as P:
        for ev in (-0.05, -0.15, -0.30):
            for n, tpd in ((1, 1), (20, 1), (20, 3)):
                R = np.array(P.map(one, [(ev, n, s, tpd) for s in range(300)]))
                print(f'avg RR {ev:+.2f}  accounts {n:2d}  trades/day {tpd}: median net ${np.median(R[:,0]):,.0f}  share net>0 {(R[:,0]>0).mean():.0%}  top 1% paid ${np.percentile(R[:,1],99):,.0f}', flush=True)
