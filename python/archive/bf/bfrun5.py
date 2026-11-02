"""Test 5 driver: the new Body Flip logic. Every event type through the grid, every market x chart, two periods, random controls."""
import sys, time, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/pp')
import ppdata, bfeng2 as EN2, bfgrid5 as G
from bfrun import in_win

TFS = [1, 2, 3, 5, 10, 15, 60, 240]
KINDS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
SH = (2, 2, 2, G.NE, G.NST, G.NT, G.NX, 6)


def rows(acc, m, tf, kind):
    out = []
    for sname, A in (('long', acc[1]), ('short', acc[0]), ('both', acc[0] + acc[1])):
        n = A[..., 0]; w = A[..., 1]; sm = A[..., 2]; sq = A[..., 3]; pos = A[..., 4]; neg = A[..., 5]
        with np.errstate(all='ignore'):
            av = sm / n; sd = np.sqrt(np.maximum(sq / n - av * av, 0) * n / np.maximum(n - 1, 1)); t = av / sd * np.sqrt(n)
            wr = w / n; pf = pos / neg
        idx = np.indices(n.shape[1:]).reshape(len(n.shape) - 1, -1).T   # slot, e, st, t, x
        f = lambda a, p: a[p].reshape(-1)
        df = pd.DataFrame({'m': m, 'tf': tf, 'kind': kind, 'side': sname, 'slot': idx[:, 0], 'e': idx[:, 1], 'st': idx[:, 2], 't': idx[:, 3], 'x': idx[:, 4],
                           'n1': f(n, 0), 'wr1': f(wr, 0), 'r1': f(av, 0), 'pf1': f(pf, 0), 't1': f(t, 0),
                           'n2': f(n, 1), 'wr2': f(wr, 1), 'r2': f(av, 1), 'pf2': f(pf, 1), 't2': f(t, 1)})
        out.append(df[(df.n1 > 0) | (df.n2 > 0)])
    return pd.concat(out, ignore_index=True)


def run_market(m):
    sp = ppdata.SPEC[m]; R = []; F = []
    for tf in TFS:
        accs = {k: np.zeros(SH) for k in KINDS + ['RANDOM side', 'RANDOM with trend']}
        fnd = {k: np.zeros((2, 2, 2, 9)) for k in accs}
        nn = 0
        for d in ppdata.series(m, tf):
            t0 = time.time()
            S = EN2.signals(d)
            o, h, l, c = S['o'], S['h'], S['l'], S['c']; n = len(c)
            per = (d.per.values == 'P2').astype(np.int64)
            mn = d.index.hour.values * 60 + d.index.minute.values
            mask = in_win(mn, 0, 1440).astype(np.int64) | (in_win(mn, 585, 720).astype(np.int64) << 1)
            hp = np.r_[np.nan, h[:-1]]; lp = np.r_[np.nan, l[:-1]]
            buX = (c > hp) & (c > o); beX = (c < lp) & (c < o)
            eI, eK, eS = S['eI'], S['eK'], S['eS']
            flipUp = np.zeros(n, np.bool_); flipDn = np.zeros(n, np.bool_)
            fm = eK == 1
            flipUp[eI[fm & (eS == 1)]] = True; flipDn[eI[fm & (eS == -1)]] = True
            base = (o, h, l, c, S['trend'].astype(np.int64), S['tl'], S['at'], S['poBu'], S['poBe'], flipUp, flipDn, buX, beX)
            for k in KINDS:
                sel = np.where(eK == k)[0]
                if len(sel) == 0: continue
                I = eI[sel].astype(np.int64); s = eS[sel].astype(np.int64)
                struct = S['eWk'][sel] if k == 1 else np.where(s == 1, l[I] - sp['tick'], h[I] + sp['tick'])
                G.grade(*base, I, s, S['eRef'][sel], struct, mask[I], per[I], 2, sp['stop'], sp['cost'], sp['tick'], 100, 10, accs[k])
                G.found(o, h, l, c, buX, beX, I, s, per[I], mask[I], fnd[k])
            rng = np.random.default_rng(31 + tf)
            ri = np.where(rng.random(n) < fm.sum() / n)[0]; ri = ri[(ri > 20) & (ri < n - 2)].astype(np.int64)
            for kind, rs in (('RANDOM side', np.where(rng.random(len(ri)) < 0.5, 1, -1)), ('RANDOM with trend', np.where(S['trend'][ri] == 1, 1, -1))):
                rs = rs.astype(np.int64)
                struct = np.where(rs == 1, l[ri] - sp['tick'], h[ri] + sp['tick'])
                ref = c[ri] - rs * 0.25 * np.nan_to_num(S['atr'][ri], nan=sp['stop'] * 0.1)
                G.grade(*base, ri, rs, ref, struct, mask[ri], per[ri], 2, sp['stop'], sp['cost'], sp['tick'], 100, 10, accs[kind])
                G.found(o, h, l, c, buX, beX, ri, rs, per[ri], mask[ri], fnd[kind])
            nn += 1
            print(m, tf, d.src.iloc[0], n, 'events', len(eI), 'flips', int(fm.sum()), f'{time.time() - t0:.1f}s', flush=True)
        if nn == 0: continue
        for k, A in accs.items():
            R.append(rows(A, m, tf, EN2.KN[k] if isinstance(k, int) else k))
        for k, A in fnd.items():
            for sd, sname in ((1, 'long'), (0, 'short')):
                for p in (0, 1):
                    for sl in (0, 1):
                        a = A[sd, p, sl]
                        F.append(dict(m=m, tf=tf, kind=EN2.KN[k] if isinstance(k, int) else k, side=sname, per=p, slot=sl, n=a[0], bc_before_opp=a[1], bc_before_nbc=a[2],
                                      p1=a[3], p5=a[4], p10=a[5], sq5=a[6], sq10=a[7], up5=a[8]))
    out = pd.concat(R, ignore_index=True)
    for col in ('wr1', 'r1', 'pf1', 't1', 'wr2', 'r2', 'pf2', 't2', 'n1', 'n2'):
        out[col] = out[col].astype(np.float32)
    out.to_parquet(f'grid5_{m}.parquet'); pd.DataFrame(F).to_parquet(f'found5_{m}.parquet')
    print('saved', m, len(out), flush=True)


if __name__ == '__main__':
    for m in sys.argv[1:]: run_market(m)
