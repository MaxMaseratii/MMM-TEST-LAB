"""SESSIONS: initial balance and Tokyo range setups (from the IB strategy check, Nov 2 2026).
ib_signals(d, tick, cutoff=900, closeOut=False)  NY IB = 9:30-10:29 high / low / mid; trades 10:30 -> cutoff (minutes, 900 = 15:00).
    FA failed auction (outside the IB, close back in; stop beyond the swing; tA = IB mid, tB = far side).
    TC trend continuation (IB trend, pullback to mid, close back on the trend side in color; tA = IB high / low).
asia_signals(d, tick)  Tokyo: range 18:00-19:59, trades 20:00-02:00. AF sweep-fade, AB breakout-retest.
Each signal: dict(day, kind, s, i, ep, stop, tA, tB, rng, vwOK, jEnd, w0, mn, trend, ex, lvl).
sim(...) here is the simple python grader used by the original test; grade.sim is the fast numba one."""
import numpy as np, pandas as pd


def days_of(d, t0, t1, cross=False):
    """groups of bar indices per session: [t0, t1) minutes; cross=True for an evening session that runs past midnight."""
    mn = d.index.hour * 60 + d.index.minute
    if not cross:
        key = d.index.normalize()
        m = (mn >= t0) & (mn < t1)
    else:
        key = (d.index - pd.Timedelta(hours=12)).normalize()     # 18:00 evening + next morning -> same key
        m = (mn >= t0) | (mn < t1)
    idx = np.where(m)[0]
    out = {}
    for k, i in zip(key[idx], idx):
        out.setdefault(k, []).append(i)
    return out


def sim(o, h, l, c, i, s, ep, stop, tgt, jEnd, cost):
    """entry at close of i (ep), exit stop / target / at close of jEnd. Returns R."""
    risk = s * (ep - stop)
    if risk <= 0: return np.nan
    for j in range(i + 1, jEnd + 1):
        if (s == 1 and l[j] <= stop) or (s == -1 and h[j] >= stop):
            px = min(o[j], stop) if s == 1 else max(o[j], stop)
            return (s * (px - ep) - cost) / risk
        if tgt is not None and ((s == 1 and h[j] >= tgt) or (s == -1 and l[j] <= tgt)):
            return (s * (tgt - ep) - cost) / risk
    return (s * (c[jEnd] - ep) - cost) / risk


def ib_signals(d, tick, cutoff=900, closeOut=False):
    o, h, l, c, v = (d[k].values for k in ('open', 'high', 'low', 'close', 'volume'))
    mn = (d.index.hour * 60 + d.index.minute).values
    sig = []
    for day, ix in days_of(d, 570, 960).items():
        ix = np.array(ix)
        ibm = mn[ix] < 630
        if ibm.sum() < 3 or (~ibm).sum() < 3: continue
        ib = ix[ibm]; rest = ix[(~ibm) & (mn[ix] < cutoff)]
        if len(rest) < 2: continue
        IBH = h[ib].max(); IBL = l[ib].min(); MID = (IBH + IBL) / 2; rng = IBH - IBL
        if rng <= 0: continue
        tp = (h[ix] + l[ix] + c[ix]) / 3; cv = np.cumsum(tp * v[ix]); cvv = np.cumsum(v[ix])
        vw = dict(zip(ix, np.where(cvv > 0, cv / np.maximum(cvv, 1e-9), np.nan)))
        trend = 1 if c[ib[-1]] > o[ib[0]] else -1
        jEnd = ix[mn[ix] < 960][-1]
        # failed auction
        for s in (1, -1):
            edge = IBL if s == 1 else IBH
            out = False; ex = np.nan
            for j in rest:
                beyond = (l[j] < edge) if s == 1 else (h[j] > edge)
                closedOut = (c[j] < edge) if s == 1 else (c[j] > edge)
                if not out and (closedOut if closeOut else beyond):
                    out = True
                if out:
                    ex = np.nanmin([ex, l[j]]) if s == 1 else np.nanmax([ex, h[j]])
                    if (s == 1 and c[j] > edge) or (s == -1 and c[j] < edge):
                        stop = ex - tick if s == 1 else ex + tick
                        sig.append(dict(day=day, kind='FA', s=s, i=j, ep=c[j], stop=stop, tA=MID, tB=IBH if s == 1 else IBL, rng=rng, vwOK=abs(vw[j] - MID) <= 0.15 * rng, jEnd=jEnd, w0=rest[0], mn=mn[j], trend=trend, ex=ex, lvl=edge))
                        break
        # trend continuation
        s = trend; touched = False; ex = np.nan
        for j in rest:
            if (s == 1 and c[j] < IBL) or (s == -1 and c[j] > IBH): break      # trend failed
            if not touched and ((s == 1 and l[j] <= MID) or (s == -1 and h[j] >= MID)):
                touched = True
            if touched:
                ex = np.nanmin([ex, l[j]]) if s == 1 else np.nanmax([ex, h[j]])
                if (s == 1 and c[j] > MID and c[j] > o[j]) or (s == -1 and c[j] < MID and c[j] < o[j]):
                    stop = ex - tick if s == 1 else ex + tick
                    sig.append(dict(day=day, kind='TC', s=s, i=j, ep=c[j], stop=stop, tA=IBH if s == 1 else IBL, tB=None, rng=rng, vwOK=abs(vw[j] - MID) <= 0.15 * rng, jEnd=jEnd, w0=rest[0], mn=mn[j], trend=trend, ex=ex, lvl=MID))
                    break
    return sig


def asia_signals(d, tick):
    o, h, l, c, v = (d[k].values for k in ('open', 'high', 'low', 'close', 'volume'))
    mn = (d.index.hour * 60 + d.index.minute).values
    sig = []
    for day, ix in days_of(d, 1080, 120, cross=True).items():
        ix = np.array(ix)
        pre = ix[(mn[ix] >= 1080) & (mn[ix] < 1200)]; rest = ix[(mn[ix] >= 1200) | (mn[ix] < 120)]
        if len(pre) < 3 or len(rest) < 3: continue
        RH = h[pre].max(); RL = l[pre].min(); MID = (RH + RL) / 2; rng = RH - RL
        if rng <= 0: continue
        jEnd = rest[-1]
        for s in (1, -1):
            edge = RL if s == 1 else RH
            # sweep-fade
            out = False; ex = np.nan
            for j in rest:
                if not out and ((s == 1 and l[j] < edge) or (s == -1 and h[j] > edge)): out = True
                if out:
                    ex = np.nanmin([ex, l[j]]) if s == 1 else np.nanmax([ex, h[j]])
                    if (s == 1 and c[j] > edge) or (s == -1 and c[j] < edge):
                        sig.append(dict(day=day, kind='AF', s=s, i=j, ep=c[j], stop=ex - tick if s == 1 else ex + tick, tA=MID, tB=RH if s == 1 else RL, rng=rng, vwOK=True, jEnd=jEnd, w0=rest[0], mn=mn[j], trend=0))
                        break
            # breakout-retest (s = breakout direction)
            bedge = RH if s == 1 else RL
            bo = False; touched = False; ex = np.nan
            for j in rest:
                if not bo:
                    if (s == 1 and c[j] > bedge) or (s == -1 and c[j] < bedge): bo = True
                    continue
                if (s == 1 and c[j] < RL) or (s == -1 and c[j] > RH): break
                if not touched and ((s == 1 and l[j] <= bedge) or (s == -1 and h[j] >= bedge)): touched = True
                if touched:
                    ex = np.nanmin([ex, l[j]]) if s == 1 else np.nanmax([ex, h[j]])
                    if (s == 1 and c[j] > bedge and c[j] > o[j]) or (s == -1 and c[j] < bedge and c[j] < o[j]):
                        sig.append(dict(day=day, kind='AB', s=s, i=j, ep=c[j], stop=ex - tick if s == 1 else ex + tick, tA=None, tB=None, rng=rng, vwOK=True, jEnd=jEnd, w0=rest[0], mn=mn[j], trend=0))
                        break
    return sig
