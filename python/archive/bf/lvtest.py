"""Her LEVELS, coded (Nov 2 2026). Adds to ibtest.py (IB + Tokyo setups).
Levels (all known before they are used):
  PD    previous trading day (18:00-17:00) high / low
  LON   London 02:00-08:00 ET high / low (NY window only, after 08:00)
  NYVP  previous session volume profile: NQ / ES = NY 09:30-16:00, gold = full 18:00-17:00 session. POC / VAH / VAL (70% value area)
  WKVP  previous week volume profile (Sun 18:00 -> Fri 17:00). POC / VAH / VAL
  Z30 / Z60  supply / demand zones on 30m / 60m: an aggressive displacement candle (body >= 1.0 ATR(14), close beyond the prior candle's
        high / low = 'loose'; body >= 1.5 ATR + the 3 candles before are a tight range (<= 2 ATR) = 'strict'). Zone = the candle to the left,
        body high to body low. Demand under a bull displacement, supply over a bear one. Alive until a close beyond its far side on its own chart
        (max 20 trading days).
  VWAP  NY anchored VWAP (09:30) / weekly VWAP (Sun 18:00) / Asia VWAP (18:00)
Volume profile = each finest bar's volume spread evenly over its high-low range in rows (NQ 2 pts, ES / gold 0.5).
Trades:
  LV   NY 09:30-15:00 level reaction: price comes to a level from one side (touch within 0.05 x stop), then within 12 candles a candle closes back
       on the approach side ('close' = in color, 'aggr' = in color AND beyond the prior candle's high / low = her 'aggressive buy up').
       Stop beyond the swing since the touch. Targets: next level ('look left', at least 1R away) / 1R-4R / hold to 16:00 / fixed 1:2.
  LVA  the same in Asia 20:00-02:00 with the previous session / week levels. inVA = Asia opened inside the previous session value area (her rule).
  AV   Asia: close outside the 18:00-20:00 range, pullback to the Asia VWAP, rejection candle -> continuation (her NQ / gold examples).
  IB / ASIA  ibtest setups, now tagged with level confluence: conf = number of other level families within tol (0.2 x stop) of the swing
       (FA, AF), of IB mid (TC) or of the range edge (AB)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/pp'); sys.path.insert(0, '/home/claude/allm')
import ppdata, mdata, ibtest as IB
from numba import njit


@njit(cache=True)
def _nsim(o, h, l, c, i, s, ep, stop, tgt, jEnd, cost):
    risk = s * (ep - stop)
    if risk <= 0: return np.nan, i
    for j in range(i + 1, jEnd + 1):
        if (s == 1 and l[j] <= stop) or (s == -1 and h[j] >= stop):
            px = min(o[j], stop) if s == 1 else max(o[j], stop)
            return (s * (px - ep) - cost) / risk, j
        if tgt == tgt and ((s == 1 and h[j] >= tgt) or (s == -1 and l[j] <= tgt)):
            return (s * (tgt - ep) - cost) / risk, j
    return (s * (c[jEnd] - ep) - cost) / risk, jEnd


def _sim(o, h, l, c, i, s, ep, stop, tgt, jEnd, cost):
    return _nsim(o, h, l, c, int(i), int(s), float(ep), float(stop), np.nan if tgt is None else float(tgt), int(jEnd), float(cost))


IB.sim = _sim

BIN = {'NQ': 2.0, 'ES': 0.5, 'GC': 0.5}
NQCUT = pd.Timestamp('2025-11-30 18:00')


def vp(lo, hi, vol, b):
    if len(lo) == 0 or np.nansum(vol) <= 0: return (np.nan,) * 3
    p0 = np.floor(lo.min() / b) * b
    nb = int((hi.max() - p0) / b) + 1
    i0 = np.clip(((lo - p0) / b).astype(np.int64), 0, nb - 1); i1 = np.clip(((hi - p0) / b).astype(np.int64), 0, nb - 1)
    w = vol / (i1 - i0 + 1)
    df = np.zeros(nb + 1); np.add.at(df, i0, w); np.add.at(df, i1 + 1, -w)
    hs = np.cumsum(df)[:nb]
    pc = int(np.argmax(hs)); tot = hs.sum(); a = b_ = pc; acc = hs[pc]
    while acc < 0.7 * tot and (a > 0 or b_ < nb - 1):
        up = hs[b_ + 1] if b_ < nb - 1 else -1; dn = hs[a - 1] if a > 0 else -1
        if up >= dn: b_ += 1; acc += up
        else: a -= 1; acc += dn
    return p0 + (pc + 0.5) * b, p0 + (b_ + 1) * b, p0 + a * b       # POC, VAH, VAL


def day_levels(src, m):
    f = mdata.fine(src); f = f[f.index <= ppdata.END]
    if src == 'NQ': f = f[f.index < NQCUT]
    sd = mdata.sday(f.index); mn = f.index.hour * 60 + f.index.minute
    lo, hi, v = f.low.values, f.high.values, f.volume.values.astype(float)
    b = BIN[m]
    days = np.sort(sd.unique())
    rows = {}
    g = pd.Series(np.arange(len(f))).groupby(sd.values)
    for dd, ix in g:
        ix = ix.values
        mm = mn[ix]
        ny = ix[(mm >= 570) & (mm < 960)]
        lon = ix[(mm >= 120) & (mm < 480)]
        sess = ix if m == 'GC' else ny
        P = vp(lo[sess], hi[sess], v[sess], b)
        rows[dd] = dict(H=hi[ix].max(), L=lo[ix].min(), POC=P[0], VAH=P[1], VAL=P[2],
                        lonH=hi[lon].max() if len(lon) else np.nan, lonL=lo[lon].min() if len(lon) else np.nan)
    DL = pd.DataFrame(rows).T.astype(float); DL.index = pd.DatetimeIndex(DL.index); DL = DL.sort_index()
    wk = pd.DatetimeIndex(sd).to_period('W-FRI')
    W = {}
    for k, ix in pd.Series(np.arange(len(f))).groupby(wk.values):
        ix = ix.values; W[k] = vp(lo[ix], hi[ix], v[ix], b)
    DL['wk'] = pd.DatetimeIndex(DL.index).to_period('W-FRI')
    prevW = {k: W.get(k - 1, (np.nan,) * 3) for k in DL.wk.unique()}
    DL['wPOC'] = [prevW[k][0] for k in DL.wk]; DL['wVAH'] = [prevW[k][1] for k in DL.wk]; DL['wVAL'] = [prevW[k][2] for k in DL.wk]
    for col in ('H', 'L', 'POC', 'VAH', 'VAL'):
        DL['p' + col] = DL[col].shift(1)
    return DL


def zones(src, m, tf):
    z = ppdata.bars_one(src, tf)
    if src == 'NQ': z = z[z.index < NQCUT]
    o, h, l, c = (z[k].values for k in ('open', 'high', 'low', 'close'))
    cp = np.r_[np.nan, c[:-1]]
    tr = np.nanmax(np.c_[h - l, np.abs(h - cp), np.abs(l - cp)], axis=1)
    atr = pd.Series(tr).rolling(14).mean().values
    tick = ppdata.SPEC[m]['tick']
    sd = mdata.sday(z.index); dpos = pd.Series(np.arange(len(sd.unique())), index=np.sort(sd.unique()))[sd].values
    out = []
    n = len(c)
    for j in range(4, n):
        a = atr[j - 1]
        if not np.isfinite(a) or a <= 0: continue
        body = c[j] - o[j]
        for s in (1, -1):
            if s * body < 1.0 * a: continue
            if not ((s == 1 and c[j] > h[j - 1]) or (s == -1 and c[j] < l[j - 1])): continue
            strict = s * body >= 1.5 * a and (h[j - 3:j].max() - l[j - 3:j].min()) <= 2.0 * a
            top = max(o[j - 1], c[j - 1]); bot = min(o[j - 1], c[j - 1])
            if top - bot < 2 * tick: top, bot = h[j - 1], l[j - 1]
            # dead: first close beyond the far side on this chart, max 20 trading days
            kmax = min(n, j + 1 + 20 * (1440 // tf))
            seg = c[j + 1:kmax]
            br = np.where(seg < bot)[0] if s == 1 else np.where(seg > top)[0]
            kd = j + 1 + br[0] if len(br) else kmax - 1
            kd = min(kd, int(np.searchsorted(dpos, dpos[j] + 20)) if dpos[j] + 20 <= dpos[-1] else n - 1)
            out.append((z.index[j] + pd.Timedelta(minutes=tf), z.index[min(kd, n - 1)] + pd.Timedelta(minutes=tf), top, bot, s, tf, strict))
    return pd.DataFrame(out, columns=['tA', 'tD', 'top', 'bot', 's', 'tf', 'strict'])


def vwap_anchor(d, anchor_mask):
    """running VWAP that restarts at each True in anchor_mask"""
    tp = ((d.high + d.low + d.close) / 3).values; v = d.volume.values.astype(float)
    grp = np.cumsum(anchor_mask)
    pv = pd.Series(tp * v).groupby(grp).cumsum().values; vv = pd.Series(v).groupby(grp).cumsum().values
    return np.where(vv > 0, pv / np.maximum(vv, 1e-9), tp)


def react(o, h, l, c, ks, L, s, eps, far=None, maxw=12):
    """ks: consecutive window bar indices. Long at support L (s=1): touch = low <= L+eps with the prior close above L (approach from above).
    Episode = up to maxw candles from the touch. Trigger 'close' = a candle in trade color closing back beyond L; 'aggr' = also beyond the
    prior candle's high / low. Returns {trig: (j, swing extreme, touch bar)}, first of each. A zone dies on a close beyond its far side."""
    if s == 1: cand = np.where((l[ks] <= L + eps) & (c[ks - 1] > L))[0]
    else: cand = np.where((h[ks] >= L - eps) & (c[ks - 1] < L))[0]
    res = {}; pn = 0
    for p in cand:
        if p < pn: continue
        k0 = ks[p]; ex = l[k0] if s == 1 else h[k0]; endp = min(len(ks), p + maxw); q = p
        while q < endp:
            j = ks[q]
            ex = min(ex, l[j]) if s == 1 else max(ex, h[j])
            if far is not None and ((s == 1 and c[j] < far) or (s == -1 and c[j] > far)): return res
            if ((s == 1 and c[j] > o[j] and c[j] > L) or (s == -1 and c[j] < o[j] and c[j] < L)):
                if 'close' not in res: res['close'] = (j, ex, k0)
                if 'aggr' not in res and ((s == 1 and c[j] > h[j - 1]) or (s == -1 and c[j] < l[j - 1])): res['aggr'] = (j, ex, k0)
                if len(res) == 2: return res
            q += 1
        pn = q
    return res


class Lv:
    """level set for one day / window: static lines + zones + dynamic VWAPs"""
    def __init__(self, lines, zs, vws, tol):
        self.lines = lines          # list of (name, fam, price)
        self.zs = zs                # DataFrame rows of active zones with kA, kD
        self.vws = vws              # list of (name, array)
        self.tol = tol

    def near(self, lo, hi, j, own):
        """families with a level within tol of [lo, hi] at bar j (own family excluded)"""
        t = self.tol; f = set()
        for nm, fam, p in self.lines:
            if fam != own and np.isfinite(p) and p >= lo - t and p <= hi + t: f.add(fam)
        for r in self.zs.itertuples():
            fam = f'Z{r.tf}'
            if fam != own and r.kA <= j < r.kD and r.top >= lo - t and r.bot <= hi + t: f.add(fam)
        for nm, arr in self.vws:
            if nm != own and np.isfinite(arr[j]) and lo - t <= arr[j] <= hi + t: f.add(nm)
        return f

    def target(self, ep, s, risk, j):
        ps = [p for _, _, p in self.lines if np.isfinite(p)]
        for r in self.zs.itertuples():
            if r.kA <= j < r.kD: ps += [r.top, r.bot]
        ps = np.array(ps)
        ok = ps[s * (ps - ep) >= risk] if len(ps) else ps
        if len(ok) == 0: return None
        return float(ok[np.argmin(np.abs(ok - ep))])


def run_src(m, src, tf, DL, ZZ):
    sp = ppdata.SPEC[m]; tick = sp['tick']; tol = 0.2 * sp['stop']; eps = 0.05 * sp['stop']
    d = ppdata.bars_one(src, tf)
    if src == 'NQ': d = d[d.index < NQCUT]
    o, h, l, c = (d[k].values for k in ('open', 'high', 'low', 'close'))
    idx = d.index; mn = (idx.hour * 60 + idx.minute).values; n = len(c)
    sd = mdata.sday(idx)
    dts = sd.values
    newday = np.r_[True, dts[1:] != dts[:-1]]
    vwA = vwap_anchor(d, newday)                       # session VWAP from 18:00 = Asia VWAP
    wk = pd.DatetimeIndex(sd).to_period('W-FRI'); neww = np.r_[True, wk[1:] != wk[:-1]]
    vwW = vwap_anchor(d, neww)
    # NY anchored VWAP: restart at 09:30 each day
    a930 = (mn >= 570) & np.r_[True, (mn[:-1] < 570) | newday[1:]]
    vwNY = np.where((mn >= 570) & (mn < 960), vwap_anchor(d, a930), np.nan)
    Z = ZZ.copy()
    Z['kA'] = np.searchsorted(idx.values, Z.tA.values); Z['kD'] = np.searchsorted(idx.values, Z.tD.values)
    Z = Z[Z.kD > Z.kA]
    sig = []
    pos = pd.Series(np.arange(n)).groupby(dts)
    for dd, ix in pos:
        ix = ix.values
        if dd not in DL.index: continue
        r = DL.loc[dd]
        base = [('pdH', 'PD', r.pH), ('pdL', 'PD', r.pL), ('pVAH', 'NYVP', r.pVAH), ('pVAL', 'NYVP', r.pVAL), ('pPOC', 'NYVP', r.pPOC),
                ('wVAH', 'WKVP', r.wVAH), ('wVAL', 'WKVP', r.wVAL), ('wPOC', 'WKVP', r.wPOC)]
        for win in ('NY', 'ASIA'):
            if win == 'NY':
                ks = ix[(mn[ix] >= 570) & (mn[ix] < 900)]; endk = ix[(mn[ix] < 960) & (mn[ix] >= 570)]
                lines = base + [('lonH', 'LON', r.lonH), ('lonL', 'LON', r.lonL)]
                vws = [('VWAP', vwNY), ('WVWAP', vwW)]
            else:
                ks = ix[(mn[ix] >= 1200) & (mn[ix] < 1440)]; nxt = ix[(mn[ix] < 120)]
                ks = np.r_[ks, nxt]; endk = ks
                lines = base
                vws = [('VWAP', vwA), ('WVWAP', vwW)]
            if len(ks) < 5 or ks[0] < 1: continue
            jEnd = endk[-1]
            z = Z[(Z.kA <= ks[-1]) & (Z.kD > ks[0]) & ((Z.top - c[ks[0]]).abs() < 6 * sp['stop']) & ((Z.bot - c[ks[0]]).abs() < 6 * sp['stop'])]
            LS = Lv(lines, z, vws, tol)
            inVA = bool(np.isfinite(r.pVAL) and r.pVAL <= o[ks[0]] <= r.pVAH)
            todo = [(nm, fam, p, s, None, None) for nm, fam, p in lines if np.isfinite(p) for s in (1, -1)]
            for zr in z.itertuples():
                todo.append(((('D' if zr.s == 1 else 'S') + str(zr.tf) + ('s' if zr.strict else 'l')), f'Z{zr.tf}', zr.top if zr.s == 1 else zr.bot, zr.s,
                             zr.bot if zr.s == 1 else zr.top, zr))
            for nm, fam, L, s, far, zr in todo:
                kk = ks if zr is None else ks[(ks >= zr.kA) & (ks < zr.kD)]
                if len(kk) < 2: continue
                res = react(o, h, l, c, kk, L, s, eps, far)
                for trig, (j, ex, k0) in res.items():
                    stop = ex - tick if s == 1 else ex + tick
                    risk = s * (c[j] - stop)
                    if risk <= 0: continue
                    lo_, hi_ = (L, L) if zr is None else (zr.bot, zr.top)
                    cf = LS.near(lo_, hi_, j, fam)
                    fresh = True
                    if zr is not None:
                        pre = slice(zr.kA, k0)
                        fresh = not (np.any(l[pre] <= zr.top) if s == 1 else np.any(h[pre] >= zr.bot))
                    sig.append(dict(day=dd, kind='LV' if win == 'NY' else 'LVA', s=s, i=j, ep=c[j], stop=stop, tA=LS.target(c[j], s, risk, j), tB=None, rng=0.0,
                                    vwOK='VWAP' in cf, jEnd=jEnd, w0=ks[0], mn=mn[j], trend=0, conf=len(cf), confs=','.join(sorted(cf)), lvt=nm, trig=trig,
                                    fresh=fresh, win=win, grp=fam, inVA=inVA))
            if win == 'ASIA':
                # Asia VWAP retest after a range break (AV)
                pre = ix[(mn[ix] >= 1080) & (mn[ix] < 1200)]
                if len(pre) < 3: continue
                RH, RL = h[pre].max(), l[pre].min()
                for s in (1, -1):
                    bo = False; touched = False; ex = np.nan
                    for j in ks:
                        if not bo:
                            if (s == 1 and c[j] > RH) or (s == -1 and c[j] < RL): bo = True
                            continue
                        vw = vwA[j]
                        if not touched and ((s == 1 and l[j] <= vw) or (s == -1 and h[j] >= vw)): touched = True; ex = l[j] if s == 1 else h[j]
                        if touched:
                            ex = min(ex, l[j]) if s == 1 else max(ex, h[j])
                            if (s == 1 and c[j] > vw and c[j] > o[j]) or (s == -1 and c[j] < vw and c[j] < o[j]):
                                stop = ex - tick if s == 1 else ex + tick; risk = s * (c[j] - stop)
                                if risk > 0:
                                    cf = LS.near(vw, vw, j, 'VWAP')
                                    sig.append(dict(day=dd, kind='AV', s=s, i=j, ep=c[j], stop=stop, tA=LS.target(c[j], s, risk, j), tB=None, rng=RH - RL, vwOK=True, jEnd=jEnd,
                                                    w0=ks[0], mn=mn[j], trend=0, conf=len(cf), confs=','.join(sorted(cf)), lvt='AsiaVWAP', trig='close', fresh=True, win='ASIA', grp='VWAP', inVA=inVA))
                                break
    # IB / Tokyo setups tagged with level confluence
    ibs = IB.ib_signals(d, tick); asi = IB.asia_signals(d, tick)
    lvcache = {}
    def LSfor(dd, win, j):
        key = (dd, win)
        if key not in lvcache:
            if dd not in DL.index: lvcache[key] = None
            else:
                r = DL.loc[dd]
                lines = [('pdH', 'PD', r.pH), ('pdL', 'PD', r.pL), ('pVAH', 'NYVP', r.pVAH), ('pVAL', 'NYVP', r.pVAL), ('pPOC', 'NYVP', r.pPOC),
                         ('wVAH', 'WKVP', r.wVAH), ('wVAL', 'WKVP', r.wVAL), ('wPOC', 'WKVP', r.wPOC)]
                if win == 'NY': lines += [('lonH', 'LON', r.lonH), ('lonL', 'LON', r.lonL)]
                lvcache[key] = Lv(lines, Z[(Z.kA <= j + 400) & (Z.kD > j - 400)], [('VWAP', vwNY if win == 'NY' else vwA), ('WVWAP', vwW)], tol)
        return lvcache[key]
    for q in ibs:
        j = q['i']; LS = LSfor(dts[j], 'NY', j)
        if LS is None: q.update(conf=0, confs=''); continue
        if q['kind'] == 'FA': cf = LS.near(q['ex'], q['ex'], j, 'VWAP')
        else: cf = LS.near(q['lvl'], q['lvl'], j, 'VWAP')
        q.update(conf=len(cf), confs=','.join(sorted(cf)))
    for q in asi:
        j = q['i']; LS = LSfor(dts[j], 'ASIA', j)
        if LS is None: q.update(conf=0, confs=''); continue
        ex = q['stop'] + tick if q['s'] == 1 else q['stop'] - tick
        if q['kind'] == 'AF': cf = LS.near(ex, ex, j, '')
        else:
            pre_lv = q['ep']   # AB: retest near range edge; use VWAP at entry vs the pullback extreme
            cf = LS.near(ex, ex, j, '')
        q.update(conf=len(cf), confs=','.join(sorted(cf)), vwOK='VWAP' in cf)
    return d, sig, ibs, asi


def run():
    allrows = []
    for m, srcs, tfs in (('NQ', ['NQ', 'MNQ'], [1, 5]), ('ES', ['MES'], [1, 5]), ('GC', ['MGC'], [5])):
        sp = ppdata.SPEC[m]
        for src in srcs:
            DL = day_levels(src, m)
            ZZ = pd.concat([zones(src, m, 30), zones(src, m, 60)], ignore_index=True)
            print(m, src, 'days', len(DL), 'zones', len(ZZ), 'strict', int(ZZ.strict.sum()), flush=True)
            for tf in tfs:
                d, sig, ibs, asi = run_src(m, src, tf, DL, ZZ)
                if len(d) < 1000: continue
                if m == 'NQ':
                    per = 'P1' if src == 'NQ' else 'P2'; perf = lambda day, per=per: per
                else:
                    days = np.sort(d.index.normalize().unique()); cut = days[len(days) // 2]
                    perf = lambda day, cut=cut: 'P1' if pd.Timestamp(day) < cut else 'P2'
                for var, S in (('LEVELS', sig), ('IB', ibs), ('ASIA', asi)):
                    rows = IB.grade(d, S, sp)
                    for r_ in rows: r_.update(m=m, tf=tf, src=src, variant=var, per=perf(r_['day']))
                    allrows += rows
                    print(m, src, tf, var, len(S), flush=True)
    D = pd.DataFrame(allrows)
    D['day'] = pd.to_datetime(D['day'])
    D.to_parquet('lvtest.parquet')
    return D


if __name__ == '__main__':
    run()
