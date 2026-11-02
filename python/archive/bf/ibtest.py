"""Test of the 'boring levels strategy' from the video (Nov 2 2026).
NY INITIAL BALANCE (IB) = 9:30-10:29 ET high / low / mid. Trades 10:30 -> cutoff (15:00, no power hour; variant 12:00).
  FA  failed auction: price goes outside the IB (wick, or a close outside = 'close' variant), then a candle CLOSES back inside
      -> trade back in (long after a failed break of IB low). Stop beyond the excursion extreme. Target IB mid (her rule) + variants.
  TC  trend continuation: IB direction = IB close vs 9:30 open. Price comes back to IB mid (touch), then a candle closes back on the
      trend side of mid in the trend color -> trade with the trend. Stop beyond the pullback extreme. Target IB high / low (her rule).
      Filter variant: NY anchored VWAP (from 9:30) within 15% of the IB range of IB mid (her confluence).
ASIA (Tokyo) range = 18:00-19:59 ET high / low. Trades 20:00 -> 02:00.
  AF  sweep-fade: wick beyond the range, close back inside -> fade. Stop beyond the sweep. Target opposite side / mid / R.
  AB  breakout-retest: close outside the range, then a pullback touches the range edge and a candle closes back outside in
      the breakout color -> continuation. Stop beyond the pullback. Target 2R / 3R / 4R.
One signal per setup per side per day. All exits stop-first, end of window = exit at the close. Cost per trade.
Controls: the same trades at a random time in the same window and day (same side, stop distance and target in R)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/pp')
import ppdata

SPEC = ppdata.SPEC


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


EXTRA = ('conf', 'confs', 'lvt', 'trig', 'fresh', 'win', 'grp', 'inVA')
TG = ['her target', 'other side', '1R', '2R', '3R', '4R']
STOPS = ['structure (swing)', 'fixed 1:2 (NQ 50 / ES 20 / GC 12)']


def grade(d, sig, sp, rng_seed=1):
    o, h, l, c = (d[k].values for k in ('open', 'high', 'low', 'close'))
    mn = (d.index.hour * 60 + d.index.minute).values
    rg = np.random.default_rng(rng_seed)
    rows = []
    for q in sig:
        i, s, ep = q['i'], q['s'], q['ep']
        for st in (0, 1):
            stop = q['stop'] if st == 0 else ep - s * sp['stop']
            risk = s * (ep - stop)
            if risk < 0.08 * sp['stop'] or risk <= 0: continue
            for ti, tn in enumerate(TG):
                if st == 1 and tn != '2R': continue
                if tn == 'her target':
                    tgt = q['tA']
                    if tgt is None: continue
                elif tn == 'other side': tgt = q['tB']
                else: tgt = ep + s * float(tn[0]) * risk
                if tgt is not None and s * (tgt - ep) <= 0: continue
                r = sim(o, h, l, c, i, s, ep, stop, tgt, q['jEnd'], sp['cost'])
                jx = q['jEnd']
                if isinstance(r, tuple): r, jx = r
                # random control: random bar in the same session window of the same day, same side, same stop size and target in R
                cand = np.arange(q['w0'], q['jEnd'] - 5)
                j = int(rg.choice(cand)) if len(cand) else i
                rep = c[j]; rstop = rep - s * risk
                rtg = None if tgt is None else rep + s * (s * (tgt - ep))
                rr = sim(o, h, l, c, j, s, rep, rstop, rtg, q['jEnd'], sp['cost'])
                if isinstance(rr, tuple): rr = rr[0]
                rows.append(dict(te=d.index[i], tx=d.index[jx], kind=q['kind'], day=q['day'], s=s, mn=q['mn'], vwOK=q['vwOK'], stop=STOPS[st], target=tn, r=r, rr=rr, risk=risk, rng=q['rng'],
                                 aligned=(q['s'] == q['trend']) if q['kind'] == 'FA' else True, **{k: q[k] for k in EXTRA if k in q}))
    return rows


def run():
    allrows = []
    for m, srcs, tfs in (('NQ', ['NQ', 'MNQ'], [1, 5]), ('ES', ['MES'], [1, 5]), ('GC', ['MGC'], [5])):
        sp = SPEC[m]
        for src in srcs:
            for tf in tfs:
                d = ppdata.bars_one(src, tf)
                if src == 'NQ': d = d[d.index < pd.Timestamp('2025-11-30')]
                if len(d) < 1000: continue
                if m == 'NQ':
                    per = 'P1' if src == 'NQ' else 'P2'
                    perf = lambda day, per=per: per
                else:
                    days = np.sort(d.index.normalize().unique()); cut = days[len(days) // 2]
                    perf = lambda day, cut=cut: 'P1' if day < cut else 'P2'
                for kind, sig in (('IB', ib_signals(d, sp['tick'])), ('IBc', ib_signals(d, sp['tick'], closeOut=True)), ('IB12', ib_signals(d, sp['tick'], cutoff=720)), ('ASIA', asia_signals(d, sp['tick']))):
                    rows = grade(d, sig, sp)
                    for r_ in rows:
                        r_.update(m=m, tf=tf, src=src, variant=kind, per=perf(r_['day']))
                    allrows += rows
                    print(m, src, tf, kind, len(sig), flush=True)
    D = pd.DataFrame(allrows)
    D.to_parquet('ibtest.parquet')
    return D


if __name__ == '__main__':
    run()
