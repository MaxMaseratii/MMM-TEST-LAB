"""Driver: Body Flip signals -> full grid (B/E) + random controls, every market x timeframe, two periods."""
import sys, time, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/pp')
import ppdata, bfeng, bfgrid
from bfgrid import NE, NST, NT, NX, NH

TFS = [1, 2, 3, 5, 10, 15, 30, 60]
SLOTS = ['all hours', '09:45-12:00', 'C 08:35-09:45', 'A 09:45-11:00', 'Asia 18:00-02:00', 'London 02:00-08:00', 'NY AM 08:00-12:00', 'PM 12:00-17:00',
         'C2 50-75% of C1', 'C2 75-100%', 'C2 100-150%', 'C2 150%+', 'C2 delta with', 'C2 delta against', 'C2 delta 50%+ of C1, with',
         'no C1 reset', '1+ C1 resets', 'beat a bigger C1 (BIG)', 'HTF trend with', 'HTF trend against']
NSL = len(SLOTS)
WIN = [(0, 1440), (585, 720), (515, 585), (585, 660), (1080, 120), (120, 480), (480, 720), (720, 1020)]


def in_win(m, a, b):
    return (m >= a) & (m < b) if a < b else (m >= a) | (m < b)


def bar_arrays(d, S):
    n = len(d)
    flipUp = np.zeros(n, np.bool_); flipDn = np.zeros(n, np.bool_)
    flipUp[S['fI'][S['fS'] == 1]] = True; flipDn[S['fI'][S['fS'] == -1]] = True
    o, h, l, c = S['o'], S['h'], S['l'], S['c']
    hp = np.r_[np.nan, h[:-1]]; lp = np.r_[np.nan, l[:-1]]
    buX = (c > hp) & (c > o); beX = (c < lp) & (c < o)
    mn = d.index.hour.values * 60 + d.index.minute.values
    mp = np.r_[mn[0], mn[:-1]]
    sess = np.zeros(n, np.bool_)
    for T in (120, 480, 570):
        sess |= (mn >= T) & ((mp < T) | (mp > mn))
    sess[0] = False
    return flipUp, flipDn, buX, beX, sess, mn


def htf_trend(src, htf, d, kw):
    H = ppdata.bars_one(src, htf)
    SH = bfeng.signals(H, **kw)
    endH = (H.index + pd.Timedelta(minutes=htf)).values
    endC = (d.index + pd.Timedelta(minutes=int(round((d.index[1] - d.index[0]).total_seconds() / 60)) if len(d) > 1 else 1)).values
    k = np.searchsorted(endH, endC, 'right') - 1
    return np.where(k >= 0, SH['trend'][np.clip(k, 0, None)], 0)


def masks(d, S, tf, kw):
    fI = S['fI']; s = S['fS'].astype(int)
    mn = d.index.hour.values[fI] * 60 + d.index.minute.values[fI]
    m = np.zeros(len(fI), np.int64)
    for k, (a, b) in enumerate(WIN):
        m |= (in_win(mn, a, b).astype(np.int64) << k)
    pct = S['fB2'] / np.maximum(S['fB1'], 1e-9) * 100
    for k, (a, b) in enumerate([(50, 75), (75, 100), (100, 150), (150, 1e9)]):
        m |= (((pct >= a) & (pct < b)).astype(np.int64) << (8 + k))
    d1, d2 = S['fD1'], S['fD2']
    has = ~np.isnan(d2)
    m |= ((has & (d2 * s > 0)).astype(np.int64) << 12)
    m |= ((has & (d2 * s <= 0)).astype(np.int64) << 13)
    m |= ((has & ~np.isnan(d1) & (d2 * s > 0) & (np.abs(d2) >= 0.5 * np.abs(d1))).astype(np.int64) << 14)
    m |= ((S['fRes'] == 0).astype(np.int64) << 15)
    m |= ((S['fRes'] >= 1).astype(np.int64) << 16)
    m |= ((S['fBig'] == 1).astype(np.int64) << 17)
    htf = 15 if tf <= 5 else 60 if tf <= 30 else None
    if htf:
        ht = htf_trend(d.src.iloc[0], htf, d, kw)[fI]
        m |= ((ht == s).astype(np.int64) << 18)
        m |= (((ht != s) & (ht != 0)).astype(np.int64) << 19)
    return m


def stats_rows(acc, m, tf, kind, slots):
    """acc[side, per, slot, e, st, t, x, h, 6] -> DataFrame rows for long / short / both."""
    out = []
    for sname, A in (('long', acc[1]), ('short', acc[0]), ('both', acc[0] + acc[1])):
        for p in (0, 1):
            pass
        n = A[..., 0]; w = A[..., 1]; sm = A[..., 2]; sq = A[..., 3]; pos = A[..., 4]; neg = A[..., 5]
        with np.errstate(all='ignore'):
            av = sm / n; sd = np.sqrt(np.maximum(sq / n - av * av, 0) * n / np.maximum(n - 1, 1)); t = av / sd * np.sqrt(n)
            wr = w / n; pf = pos / neg
        idx = np.indices(n.shape[1:]).reshape(len(n.shape) - 1, -1).T   # slot, e, st, t, x, h
        f = lambda a, p: a[p].reshape(-1)
        df = pd.DataFrame({'m': m, 'tf': tf, 'kind': kind, 'side': sname,
                           'slot': idx[:, 0], 'e': idx[:, 1], 'st': idx[:, 2], 't': idx[:, 3], 'x': idx[:, 4], 'h': idx[:, 5],
                           'n1': f(n, 0), 'wr1': f(wr, 0), 'r1': f(av, 0), 'pf1': f(pf, 0), 't1': f(t, 0),
                           'n2': f(n, 1), 'wr2': f(wr, 1), 'r2': f(av, 1), 'pf2': f(pf, 1), 't2': f(t, 1)})
        df = df[(df.n1 > 0) | (df.n2 > 0)]
        df['slot'] = np.array(slots)[df.slot.values] if slots is not None else df.slot
        out.append(df)
    return pd.concat(out, ignore_index=True)


def run_market(m, kw=None, tag='base', tfs=TFS, slot_limit=None, controls=True, atr_fixed=False):
    kw = kw or {}
    sp = ppdata.SPEC[m]
    rows = []; ev_all = []
    for tf in tfs:
        nsl = NSL if slot_limit is None else slot_limit
        acc = np.zeros((2, 2, nsl, NE, NST, NT, NX, NH, 6))
        accR = np.zeros((2, 2, 2, NE, NST, NT, NX, NH, 6)) if controls else None
        accR2 = np.zeros((2, 2, 2, NE, NST, NT, NX, NH, 6)) if controls else None
        nsig = 0
        for d in ppdata.series(m, tf):
            t0 = time.time()
            S = bfeng.signals(d, **kw)
            flipUp, flipDn, buX, beX, sess, mn = bar_arrays(d, S)
            per = (d.per.values == 'P2').astype(np.int64)
            fI = S['fI']
            if len(fI) == 0: continue
            mk = masks(d, S, tf, kw) if slot_limit is None else masks(d, S, tf, kw) & ((1 << nsl) - 1)
            args = (S['o'], S['h'], S['l'], S['c'], S['trend'], S['lnW'] if kw.get('lvlWick', True) else S['lnB'], S['lnA'] if atr_fixed else S['atr'], flipUp, flipDn, buX, beX, sess)
            keep = np.zeros((0, 5), np.int64); outK = np.zeros((1, 5))
            bfgrid.grade(*args, fI, S['fS'].astype(np.int64), S['fW1'], S['fL1'], S['fLine'], mk, per[fI], nsl,
                         sp['stop'], sp['cost'], sp['tick'], 100, 10, bfgrid.KST, bfgrid.KEX, bfgrid.TGT, acc, keep, outK)
            nsig += len(fI)
            if controls:
                rng = np.random.default_rng(7 + tf)
                n = len(d); p = len(fI) / n
                ri = np.where(rng.random(n) < p)[0]; ri = ri[(ri > 20) & (ri < n - 2)]
                o, h, l, c = S['o'], S['h'], S['l'], S['c']
                rm = (in_win(mn[ri], 0, 1440).astype(np.int64)) | (in_win(mn[ri], 585, 720).astype(np.int64) << 1)
                for side_mode, A in (('random', accR), ('trend', accR2)):
                    rs = np.where(rng.random(len(ri)) < 0.5, 1, -1) if side_mode == 'random' else np.where(S['trend'][ri] == 1, 1, -1)
                    rs = rs.astype(np.int64)
                    c1w = np.where(rs == 1, l[ri - 1], h[ri - 1]); c1b = o[ri - 1].astype(float); ln = o[ri - 1].astype(float)
                    bfgrid.grade(*args, ri.astype(np.int64), rs, c1w, c1b, ln, rm, per[ri], 2,
                                 sp['stop'], sp['cost'], sp['tick'], 100, 10, bfgrid.KST, bfgrid.KEX, bfgrid.TGT, A, keep, outK)
            print(m, tf, d.src.iloc[0], len(d), 'signals', len(fI), f'{time.time() - t0:.1f}s', flush=True)
        if nsig == 0: continue
        R = stats_rows(acc, m, tf, 'CDS/CDL', SLOTS[:nsl])
        keep_rows = R[(R.slot.isin(SLOTS[:2])) | ((R.n1 >= 30) & (R.n2 >= 20) & (R.r1 > 0) & (R.r2 > 0))]
        rows.append(keep_rows)
        if controls:
            rows.append(stats_rows(accR, m, tf, 'RANDOM side', SLOTS[:2]))
            rows.append(stats_rows(accR2, m, tf, 'RANDOM with trend', SLOTS[:2]))
        del acc
    out = pd.concat(rows, ignore_index=True)
    for c in ('wr1', 'r1', 'pf1', 't1', 'wr2', 'r2', 'pf2', 't2', 'n1', 'n2'):
        out[c] = out[c].astype(np.float32)
    out.to_parquet(f'grid_{tag}_{m}.parquet')
    print('saved', m, tag, len(out), flush=True)


if __name__ == '__main__':
    tag = sys.argv[1]
    for m in sys.argv[2:]:
        run_market(m, tag=tag)
