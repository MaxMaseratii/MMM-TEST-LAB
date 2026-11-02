"""PROPSIM: what a payout claim looks like when one trader runs many prop accounts (Nov 2 2026).

slots(T, ...) runs `n` accounts that all copy the SAME trades (a trade copier), from the first trade to the last:
  - each slot starts as an evaluation (cost `eval_cost`); pass = +target before the trailing drawdown, a daily loss of `dloss` ends the day;
  - a passed slot pays `activation` and becomes funded: trailing drawdown from the peak (end of day), stops trailing at start + `lock`;
    once the balance is `buffer` above start, every `every` trading days the trader withdraws what is above the buffer
    (min `min_pay`, 100% of the first `full_split` dollars, then `split`);
  - a blown slot (eval or funded) is replaced at once by a new evaluation (cost again) - "burn and rebuy".
Defaults are an ASSUMED generic 50k account (target $3,000, $2,500 trailing drawdown, $1,000 daily loss), not any one firm's exact rules.
Returns totals: evaluations bought, $ spent, passes, payouts ($ and count), the best month of payouts (what gets posted), net.
Run it on the real trades and on their random twins: the random twins show what "payouts" look like with NO edge."""
import numpy as np, pandas as pd


def slots(T, risk_usd=500.0, n=20, eval_cost=100.0, activation=0.0, target=3000.0, trail=2500.0, dloss=1000.0,
          buffer=2600.0, lock=100.0, min_pay=500.0, every=8, full_split=25000.0, split=0.9, col='r', stagger=0, cap=None, max_pays=None):
    """T: trades in time order with te (entry time) and the R column; every slot takes every trade (copier).
    stagger: slot i is bought on trading day i * stagger (0 = all bought on day one)."""
    T = T.sort_values('te')
    day = pd.to_datetime(T.te).dt.normalize().values; R = T[col].values.astype(float)
    S = [dict(st='eval', bal=0.0, peak=0.0, paid=0.0, last=None, days=0, start=i * stagger) for i in range(n)]
    dlist = np.unique(day); dpos = {x: q for q, x in enumerate(dlist)}
    out = dict(evals=n, spent=n * eval_cost, passes=0, funded_blown=0, eval_blown=0, payouts=0, paid=0.0, pay_months={})
    k = 0; N = len(R)
    while k < N:
        d = day[k]; j = k
        while j < N and day[j] == d: j += 1
        for s in S:
            if dpos[d] < s['start']: continue
            dsum = 0.0
            for q in range(k, j):
                if dsum <= -dloss: break
                u = R[q] * risk_usd; dsum += u; s['bal'] += u
                if s['st'] == 'eval' and s['bal'] >= target:
                    s.update(st='funded', bal=0.0, peak=0.0, paid=0.0, last=None, days=0, npay=0); out['passes'] += 1; out['spent'] += activation
                    break                                     # rest of the day starts the funded account tomorrow
            # end of day
            if s['st'] == 'eval':
                s['peak'] = max(s['peak'], s['bal'])
                if s['bal'] <= s['peak'] - trail:
                    out['eval_blown'] += 1; out['evals'] += 1; out['spent'] += eval_cost
                    s.update(st='eval', bal=0.0, peak=0.0, start=0)
            else:
                s['days'] += 1
                s['peak'] = max(s['peak'], s['bal'])
                floor = min(s['peak'] - trail, lock)
                if s['bal'] <= floor:
                    out['funded_blown'] += 1; out['evals'] += 1; out['spent'] += eval_cost
                    s.update(st='eval', bal=0.0, peak=0.0, paid=0.0, last=None, days=0, start=0)
                    continue
                if s['bal'] - buffer >= min_pay and (s['last'] is None or s['days'] - s['last'] >= every):
                    amt = s['bal'] - buffer if cap is None else min(s['bal'] - buffer, cap)
                    tot = s['paid'] + amt
                    net = min(amt, max(0.0, full_split - s['paid'])) + split * max(0.0, tot - max(full_split, s['paid']))
                    s['paid'] = tot; s['bal'] -= amt; s['last'] = s['days']; s['npay'] = s.get('npay', 0) + 1
                    out['payouts'] += 1; out['paid'] += net
                    if max_pays is not None and s['npay'] >= max_pays:          # account retired after its last allowed payout -> buy a new one
                        out['evals'] += 1; out['spent'] += eval_cost; s.update(st='eval', bal=0.0, peak=0.0, paid=0.0, last=None, days=0, start=0, npay=0)
                    mo = str(pd.Timestamp(d).to_period('M')); out['pay_months'][mo] = out['pay_months'].get(mo, 0.0) + net
        k = j
    pm = out.pop('pay_months')
    out['best_month'] = max(pm.values()) if pm else 0.0
    out['months'] = len(set(str(pd.Timestamp(x).to_period('M')) for x in day)) if N else 0
    out['net'] = out['paid'] - out['spent']
    return out


def compare(T, **kw):
    """same accounts on the real trades and on the random twins (column r_rand)."""
    a = slots(T, col='r', **kw)
    b = slots(T.assign(r_rand=T.r_rand.values), col='r_rand', **kw) if 'r_rand' in T else None
    return a, b
