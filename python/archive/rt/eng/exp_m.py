"""HTF signal, LTF entry ('magnifier').
An HTF MMCB candle closes. During the NEXT HTF candle, price pulls back to a level of the HTF candle
(P / MP / BAL / MD / open). Then on the LTF we wait for a trigger and enter at its close.
Triggers: T0 = plain limit at the level (no LTF) · T1 = first LTF body close with the trade
          T2 = LTF rejection (sweeps the prior LTF candle's other side, closes in the trade half)
          T3 = LTF GMC (3 LTF candles with a gap, after the touch).
Stops: trigger candle extreme · LTF swing since the touch · HTF protected extreme · fixed 50.
Targets: the HTF target (bull: HTF candle high) · 2R · 3R. Time exit: close of the next HTF candle (W1) or the one after (W2).
A trade is MISSED if the HTF target is taken before the trigger, CANCELLED if the HTF protected extreme breaks first."""
import sys, numpy as np, pandas as pd, numba as nb, time
sys.path.insert(0, '/home/claude/rt/eng')
from core import *
import data as D
OUT = '/home/claude/rt/out'

@nb.njit(cache=True)
def mag(lo_, lh, ll, lc, lLast, rO, rH, rL, rC,
        js_a, js_b, js_e, side, L, tgt, prot, trig, smode, cost, tick, fixed, lflip, ltn):
    n = len(js_a)
    res = np.full((n, 3), np.nan)   # R at target TGT / 2R / 3R
    rr0 = np.full(n, np.nan)
    stat = np.zeros(n, np.int64)    # 0 no touch, 1 missed (target first), 2 cancelled (protected first), 3 no trigger, 4 traded, 5 stop too small/invalid
    for r in range(n):
        s = side[r]; a = js_a[r]; b = js_b[r]; bE = js_e[r]
        touch = -1; swing = 0.0; k = -1
        for i in range(a, b + 1):
            # this LTF bar
            if s == 1:
                if touch < 0:
                    if lh[i] > tgt[r] and ll[i] > L[r] - tick:
                        stat[r] = 1; break
                    if ll[i] <= L[r] - tick:
                        touch = i; swing = ll[i]
                        if ll[i] < prot[r]:
                            stat[r] = 2; break
                    else:
                        continue
                else:
                    if ll[i] < prot[r]:
                        stat[r] = 2; break
                    if lh[i] > tgt[r] and i > touch:
                        stat[r] = 1; break
                    swing = min(swing, ll[i])
            else:
                if touch < 0:
                    if ll[i] < tgt[r] and lh[i] < L[r] + tick:
                        stat[r] = 1; break
                    if lh[i] >= L[r] + tick:
                        touch = i; swing = lh[i]
                        if lh[i] > prot[r]:
                            stat[r] = 2; break
                    else:
                        continue
                else:
                    if lh[i] > prot[r]:
                        stat[r] = 2; break
                    if ll[i] < tgt[r] and i > touch:
                        stat[r] = 1; break
                    swing = max(swing, lh[i])
            # trigger check at the close of bar i
            t = trig[r]; ok = False
            if t == 0:
                ok = True
            elif i >= 1:
                rg = lh[i] - ll[i]
                ps = (lc[i] - ll[i]) / rg if rg > 0 else 0.5
                if t == 1:
                    ok = (lc[i] > lh[i - 1]) if s == 1 else (lc[i] < ll[i - 1])
                elif t == 2:
                    ok = (ll[i] < ll[i - 1] and ps >= 0.5) if s == 1 else (lh[i] > lh[i - 1] and ps <= 0.5)
                elif t == 4:
                    ok = lflip[i] == s
                elif t == 3 and i - 2 >= touch:
                    ok = (lc[i - 1] > lh[i - 2] and ll[i] > lh[i - 2]) if s == 1 else (lc[i - 1] < ll[i - 2] and lh[i] < ll[i - 2])
            if ok:
                k = i; break
        if k < 0:
            if stat[r] == 0 and touch >= 0:
                stat[r] = 3
            continue
        sgn = 1.0 if s == 1 else -1.0
        if trig[r] == 0:
            e = L[r]
            if s == 1 and lo_[touch] < L[r]: e = min(L[r], lo_[touch])
            if s == -1 and lo_[touch] > L[r]: e = max(L[r], lo_[touch])
        else:
            e = lc[k]
        sm = smode[r]
        if sm == 0:
            if trig[r] == 0: stat[r] = 5; continue
            stp = (min(ll[k], ll[k - 1]) - tick) if s == 1 else (max(lh[k], lh[k - 1]) + tick)
            if trig[r] == 3:
                stp = (min(ll[k], ll[k - 1], ll[k - 2]) - tick) if s == 1 else (max(lh[k], lh[k - 1], lh[k - 2]) + tick)
            if trig[r] == 1:
                stp = (ll[k] - tick) if s == 1 else (lh[k] + tick)
            if trig[r] == 4:
                stp = (ltn[k] - tick) if s == 1 else (ltn[k] + tick)
        elif sm == 1:
            if trig[r] == 0: stat[r] = 5; continue
            stp = swing - tick if s == 1 else swing + tick
        elif sm == 2:
            stp = prot[r] - tick if s == 1 else prot[r] + tick
        else:
            stp = e - sgn * fixed
        d = sgn * (e - stp)
        if d < 2.0:
            stat[r] = 5; continue
        stat[r] = 4
        rr0[r] = sgn * (tgt[r] - e) / d
        tp = np.array([tgt[r], e + sgn * 2 * d, e + sgn * 3 * d])
        # outcome on the replay bars after the entry bar (limit: after the touch bar, stop checked on it)
        st0 = lLast[k] + 1
        endI = lLast[bE]
        done = np.zeros(3, np.bool_)
        if trig[r] == 0:
            # fill bar: stop check only (safe side)
            if (s == 1 and ll[k] <= stp) or (s == -1 and lh[k] >= stp):
                for q in range(3):
                    res[r, q] = -1.0 - cost / d
                continue
        stopped = False
        for i in range(st0, endI + 1):
            if s == 1:
                if rL[i] <= stp:
                    px = min(rO[i], stp)
                    for q in range(3):
                        if not done[q]:
                            res[r, q] = (px - e) / d - cost / d; done[q] = True
                    stopped = True; break
                for q in range(3):
                    if not done[q] and sgn * (tp[q] - e) > 0 and rH[i] >= tp[q]:
                        res[r, q] = (tp[q] - e) / d - cost / d; done[q] = True
            else:
                if rH[i] >= stp:
                    px = max(rO[i], stp)
                    for q in range(3):
                        if not done[q]:
                            res[r, q] = (e - px) / d - cost / d; done[q] = True
                    stopped = True; break
                for q in range(3):
                    if not done[q] and sgn * (tp[q] - e) > 0 and rL[i] <= tp[q]:
                        res[r, q] = (e - tp[q]) / d - cost / d; done[q] = True
            if done[0] and done[1] and done[2]:
                break
        for q in range(3):
            if not done[q]:
                if q == 0 and sgn * (tp[0] - e) <= 0:
                    res[r, q] = np.nan   # target already behind the entry
                else:
                    res[r, q] = sgn * (rC[min(endI, len(rC) - 1)] - e) / d - cost / d
    return res, rr0, stat

LEV = [('P 87.5', .875), ('MP 75', .75), ('BAL 50', .5), ('MD 25', .25), ('O open', 'O')]
TRG = ['T0 limit at the level', 'T1 LTF body close', 'T2 LTF rejection candle', 'T3 LTF GMC', 'T4 LTF flip (CDLc / CDSc)']
SMN = ['trigger candle (T4: new LTF T1 PO4)', 'LTF swing since touch', 'HTF protected extreme', 'fixed 50']

def ltf_flips(Lb):
    """compact MMM candle engine (c) on the LTF: flip events (+1 CDL / -1 CDS) and the new T1 price."""
    o, h, l, c = Lb.open.values, Lb.high.values, Lb.low.values, Lb.close.values
    n = len(c); fl = np.zeros(n, np.int64); tnA = np.full(n, np.nan)
    side = 0; tn = pb = rs = np.nan
    for i in range(1, n):
        bu = c[i] > h[i - 1]; be = c[i] < l[i - 1]; done = False
        if side == 1:
            if c[i] < tn:
                side = -1; tn = o[i] if np.isnan(pb) else pb; pb = rs = np.nan; done = True; fl[i] = -1
            elif not np.isnan(pb) and c[i] > pb:
                tn = o[i] if np.isnan(rs) else rs; pb = rs = np.nan; done = True
        elif side == -1:
            if c[i] > tn:
                side = 1; tn = o[i] if np.isnan(pb) else pb; pb = rs = np.nan; done = True; fl[i] = 1
            elif not np.isnan(pb) and c[i] < pb:
                tn = o[i] if np.isnan(rs) else rs; pb = rs = np.nan; done = True
        elif bu or be:
            side = 1 if bu else -1; tn = o[i]; done = True
        if not done:
            if side == 1:
                if not np.isnan(rs) and c[i] < rs: rs = np.nan
                if be and np.isnan(pb): pb = o[i]
                elif bu and not np.isnan(pb) and np.isnan(rs): rs = o[i]
            elif side == -1:
                if not np.isnan(rs) and c[i] > rs: rs = np.nan
                if bu and np.isnan(pb): pb = o[i]
                elif be and not np.isnan(pb) and np.isnan(rs): rs = o[i]
        tnA[i] = tn
    return fl, tnA

def ltf_index(htf, ltf):
    """LTF bars of the next HTF candle (W1) and the one after (W2)."""
    ht = htf.index.values; lt = ltf.index.values
    first = np.searchsorted(lt, ht, 'left')
    nxt = np.r_[ht[1:], np.datetime64('2100-01-01')]
    last = np.searchsorted(lt, nxt, 'left') - 1
    return first, last

def run(period):
    t0 = time.time()
    if period == 'old':
        m1, bars = D.old(); rep = m1
        combos = [('D', ['15m', '5m', '1m']), ('4h', ['15m', '5m', '1m']), ('1h', ['5m', '1m']), ('15m', ['1m'])]
    elif period == 'fresh10':
        rep, bars, dd = D.fresh10(); m1 = rep
        combos = [('D', ['15m']), ('4h', ['15m']), ('1h', ['15m'])]
    else:
        m1, m5, bars, fpd, dd = D.fresh(); rep = m5
        combos = [('D', ['15m', '5m']), ('4h', ['15m', '5m']), ('1h', ['5m'])]
    allrec = []
    for htf, ltfs in combos:
        H = bars[htf]
        ty, pos, *_ = mmcb(H)
        o, h, l, c = H.open.values, H.high.values, H.low.values, H.close.values
        sess = session(H.index) if htf not in ('4h', 'D') else np.full(len(H), 3)
        for lt in ltfs:
            Lb = m1 if lt == '1m' else (bars[lt] if lt in bars else resample(m1, lt))
            if period == 'fresh':
                Lb = Lb[Lb.index >= rep.index[0]]
            fI, lI = ltf_index(H, Lb)
            lfl, ltnA = ltf_flips(Lb)
            _, rLast, _ = map_replay(Lb, rep)
            if lt == '1m':
                rLast = np.arange(len(Lb))
            js = np.where(ty >= 0)[0]
            js = js[(js > 20) & (js < len(H) - 3)]
            a1 = fI[js + 1]; b1 = lI[js + 1]; b2 = lI[js + 2]
            ok = (b1 >= a1) & (a1 < len(Lb)) & (b2 < len(Lb))
            js, a1, b1, b2 = js[ok], a1[ok], b1[ok], b2[ok]
            s = TSIDE[ty[js]]
            rg = (h - l)[js]
            rows = []
            for li, (ln, f) in enumerate(LEV):
                Lv = o[js] if f == 'O' else np.where(s == 1, l[js] + f * rg, h[js] - f * rg)
                valid = s * (c[js] - Lv) > 0
                for ti in range(5):
                    for si in range(4):
                        if ti == 0 and si < 2:
                            continue
                        for wi, bE in ((0, b1), (1, b2)):
                            m = valid
                            rows.append(pd.DataFrame(dict(j=js[m], a=a1[m], b=b1[m], e=bE[m], side=s[m], L=Lv[m],
                                                          tgt=np.where(s == 1, h[js], l[js])[m], prot=np.where(s == 1, l[js], h[js])[m],
                                                          trig=ti, smode=si, lev=li, win=wi, ty=ty[js][m], sess=sess[js][m])))
            R = pd.concat(rows, ignore_index=True)
            res, rr0, stat = mag(Lb.open.values, Lb.high.values, Lb.low.values, Lb.close.values, rLast,
                                 rep.open.values, rep.high.values, rep.low.values, rep.close.values,
                                 R.a.values.astype(np.int64), R.b.values.astype(np.int64), R.e.values.astype(np.int64),
                                 R.side.values.astype(np.int64), R.L.values, R.tgt.values, R.prot.values,
                                 R.trig.values.astype(np.int64), R.smode.values.astype(np.int64), 1.0, TICK, 50.0, lfl, ltnA)
            R['R_tgt'], R['R_2R'], R['R_3R'], R['rr0'], R['stat'] = res[:, 0], res[:, 1], res[:, 2], rr0, stat
            R['htf'] = htf; R['ltf'] = lt; R['period'] = period
            R.drop(columns=['a', 'b', 'e', 'L', 'tgt', 'prot']).to_parquet(f'{OUT}/M_{period}_{htf}_{lt}.parquet')
            print(period, htf, lt, len(R), f'{time.time() - t0:.0f}s', flush=True)

if __name__ == '__main__':
    run(sys.argv[1])
