"""MONEY: dollars per month and prop evaluations, with honest daily rules.

account(T, risk_usd=200, max_losses=2, max_trades=None, one_at_a_time=True)
    takes trades in time order; skips a trade while another is still open; stops the day after `max_losses` losers
    (a loss counts only once that trade has CLOSED - no looking ahead). Needs columns te, tx, r.
monthly(T, risk_usd)  -> $ per month, best / worst month, green-month share.
prop(T, risk_usd)     50k evaluation started on the first trade of each month: pass = +$3,000 before a $2,000 trailing
                      end-of-day drawdown; a $1,000 losing day stops that day. Returns the list of 'pass' / 'fail' / 'open'."""
import numpy as np, pandas as pd


def account(T, risk_usd=200.0, max_losses=2, max_trades=None, one_at_a_time=True):
    T = T.sort_values(['te', 'tx']).reset_index(drop=True)
    keep = []; los = {}; cnt = {}; busy = pd.Timestamp(0)
    for k, (te, tx, r) in enumerate(zip(T.te, T.tx, T.r)):
        dd = (pd.Timestamp(te) + pd.Timedelta(hours=6)).normalize()
        if one_at_a_time and te < busy: continue
        if max_losses is not None and los.get(dd, 0) >= max_losses: continue
        if max_trades is not None and cnt.get(dd, 0) >= max_trades: continue
        keep.append(k); busy = tx; cnt[dd] = cnt.get(dd, 0) + 1
        if r <= 0: los[dd] = los.get(dd, 0) + 1
    A = T.iloc[keep].copy(); A['usd'] = A.r * risk_usd
    return A


def monthly(A):
    mo = pd.to_datetime(A.te).dt.to_period('M'); pm = A.usd.groupby(mo).sum()
    return dict(trades=len(A), months=len(pm), per_month=pm.mean() if len(pm) else np.nan, best=pm.max(), worst=pm.min(), green=(pm > 0).mean())


def prop(A, target=3000.0, trail=2000.0, dloss=1000.0):
    A = A.copy(); A['day'] = pd.to_datetime(A.te).dt.date; A['mon'] = pd.to_datetime(A.te).dt.to_period('M')
    res = []
    for mo in A.mon.unique():
        S = A[A.te >= A[A.mon == mo].te.min()]
        bal = 0.0; peak = 0.0; out = 'open'
        for dd, g in S.groupby('day', sort=True):
            dsum = 0.0
            for u in g.usd.values:
                if dsum <= -dloss: break
                dsum += u; bal += u
                if bal >= target: out = 'pass'; break
            if out == 'pass': break
            peak = max(peak, bal)
            if bal <= peak - trail: out = 'fail'; break
        res.append(out)
    return res
