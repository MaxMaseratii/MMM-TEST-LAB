"""Driver for test 2: C1 / C2 range retest entries, PO4 / ATR stops, 1:2-1:6 or next-flip exit; every market x chart, two periods, random controls."""
import sys, time, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/pp')
import ppdata, bfeng, bfgrid2 as G
from bfrun import bar_arrays, in_win

TFS = [1, 2, 3, 5, 10, 15, 60, 240]
SLOTS = ['all hours', '09:45-12:00']


def stats_rows(acc, m, tf, kind):
    out = []
    for sname, A in (('long', acc[1]), ('short', acc[0]), ('both', acc[0] + acc[1])):
        n = A[..., 0]; w = A[..., 1]; sm = A[..., 2]; sq = A[..., 3]; pos = A[..., 4]; neg = A[..., 5]
        with np.errstate(all='ignore'):
            av = sm / n; sd = np.sqrt(np.maximum(sq / n - av * av, 0) * n / np.maximum(n - 1, 1)); t = av / sd * np.sqrt(n)
            wr = w / n; pf = pos / neg
        idx = np.indices(n.shape[1:]).reshape(len(n.shape) - 1, -1).T   # slot, w, e, st, t, x
        f = lambda a, p: a[p].reshape(-1)
        df = pd.DataFrame({'m': m, 'tf': tf, 'kind': kind, 'side': sname,
                           'slot': idx[:, 0], 'w': idx[:, 1], 'e': idx[:, 2], 'st': idx[:, 3], 't': idx[:, 4], 'x': idx[:, 5],
                           'n1': f(n, 0), 'wr1': f(wr, 0), 'r1': f(av, 0), 'pf1': f(pf, 0), 't1': f(t, 0),
                           'n2': f(n, 1), 'wr2': f(wr, 1), 'r2': f(av, 1), 'pf2': f(pf, 1), 't2': f(t, 1)})
        df = df[(df.n1 > 0) | (df.n2 > 0)]
        out.append(df)
    return pd.concat(out, ignore_index=True)


def shape():
    return (2, 2, len(SLOTS), G.NW, G.NE, G.NST, G.NT, G.NX, 6)


def run_market(m, tfs=TFS, kw=None):
    kw = kw or {}
    sp = ppdata.SPEC[m]; rows = []
    for tf in tfs:
        acc = np.zeros(shape()); accR = np.zeros(shape()); accT = np.zeros(shape()); nsig = 0
        for d in ppdata.series(m, tf):
            t0 = time.time()
            S = bfeng.signals(d, **kw)
            flipUp, flipDn, buX, beX, sess, mn = bar_arrays(d, S)
            per = (d.per.values == 'P2').astype(np.int64)
            fI = S['fI']
            if len(fI) == 0: continue
            mk = in_win(mn[fI], 0, 1440).astype(np.int64) | (in_win(mn[fI], 585, 720).astype(np.int64) << 1)
            base = (S['o'], S['h'], S['l'], S['c'], S['trend'], S['lnW'], S['atr'], flipUp, flipDn)
            G.grade(*base, fI, S['fS'].astype(np.int64), S['fC1'].astype(np.int64), S['fSI'].astype(np.int64), S['fW1'], S['fSW'],
                    mk, per[fI], 2, sp['stop'], sp['cost'], sp['tick'], 100, acc)
            nsig += len(fI)
            rng = np.random.default_rng(11 + tf)
            n = len(d); p = len(fI) / n
            ri = np.where(rng.random(n) < p)[0]; ri = ri[(ri > 20) & (ri < n - 2)]
            rm = in_win(mn[ri], 0, 1440).astype(np.int64) | (in_win(mn[ri], 585, 720).astype(np.int64) << 1)
            h, l = S['h'], S['l']
            for mode, A in (('random', accR), ('trend', accT)):
                rs = (np.where(rng.random(len(ri)) < 0.5, 1, -1) if mode == 'random' else np.where(S['trend'][ri] == 1, 1, -1)).astype(np.int64)
                c1 = (ri - 1).astype(np.int64); po = np.where(rs == 1, l[ri - 1], h[ri - 1]).astype(float)
                G.grade(*base, ri.astype(np.int64), rs, c1, c1, po, po, rm, per[ri], 2, sp['stop'], sp['cost'], sp['tick'], 100, A)
            print(m, tf, d.src.iloc[0], len(d), 'signals', len(fI), f'{time.time() - t0:.1f}s', flush=True)
        if nsig == 0: continue
        rows += [stats_rows(acc, m, tf, 'CDS/CDL'), stats_rows(accR, m, tf, 'RANDOM side'), stats_rows(accT, m, tf, 'RANDOM with trend')]
    out = pd.concat(rows, ignore_index=True)
    for c in ('wr1', 'r1', 'pf1', 't1', 'wr2', 'r2', 'pf2', 't2', 'n1', 'n2'):
        out[c] = out[c].astype(np.float32)
    out['slot'] = np.array(SLOTS)[out.slot.values]
    out.to_parquet(f'grid2_{m}.parquet')
    print('saved', m, len(out), flush=True)


if __name__ == '__main__':
    for m in sys.argv[1:]:
        run_market(m)
