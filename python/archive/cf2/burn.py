"""Account-burn simulation for every strategy's headline rule: 1 account vs 20 copied accounts (staggered 5 days), eval $100 vs $300,
real trades vs their random twins. Output burn.json"""
import sys, json, glob, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/mmmlab')
from mmmlab import propsim as PS, money as MO


def run(label, z, risk, maxloss, strat, m, tf):
    out = []
    for p in ('P1', 'P2'):
        x = z[z.per == p][['te', 'tx', 'r', 'r_rand']].dropna()
        if len(x) < 10: continue
        A = MO.account(x, risk_usd=risk, max_losses=maxloss)
        yrs = max((pd.to_datetime(A.te).max() - pd.to_datetime(A.te).min()).days / 365.25, 1 / 12)
        for n in (1, 20):
            for cost in (100, 300):
                a = PS.slots(A, risk_usd=risk, n=n, col='r', stagger=5, eval_cost=cost)
                b = PS.slots(A, risk_usd=risk, n=n, col='r_rand', stagger=5, eval_cost=cost)
                out.append(dict(strat=strat, rule=label, m=m, tf=tf, per=p, n=n, cost=cost, risk=risk, trades=len(A), years=round(yrs, 2),
                                avgR=round(float(A.r.mean()), 3), avgRand=round(float(A.r_rand.mean()), 3),
                                **{'r_' + k: round(float(v), 1) for k, v in a.items()}, **{'x_' + k: round(float(v), 1) for k, v in b.items()}))
    return out


if __name__ == '__main__':
    src = sys.argv[1]; cfg = json.load(open(sys.argv[2]))   # list of [strat, label, m, tf, risk, maxloss, filters{col: value or [values]}]
    T = pd.concat([pd.read_parquet(f) for f in glob.glob(src)], ignore_index=True)
    rows = []
    for strat, label, m, tf, risk, ml, flt in cfg:
        z = T[(T.strat == strat) & (T.m == m) & (T.tf == tf)]
        for k, v in flt.items():
            if k == 'tagstart': z = z[z.tag.str.startswith(v)]
            else: z = z[z[k].isin(v if isinstance(v, list) else [v])]
        if not len(z): print('EMPTY', strat, label); continue
        rows += run(label, z, risk, ml, strat, m, tf)
        print(strat, label, len(z), flush=True)
    json.dump(rows, open(sys.argv[3], 'w'))
