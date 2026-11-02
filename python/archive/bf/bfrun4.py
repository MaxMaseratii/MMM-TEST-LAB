"""Driver for test 4 (Max trade management: flip exit always, fee BE on a BC, structure trail). Saves raw stat arrays per market x chart."""
import sys, time, numpy as np
sys.path.insert(0, '/home/claude/pp')
import ppdata, bfeng, bfgrid4 as G
from bfrun import bar_arrays, in_win
TFS = [1, 2, 3, 5, 10, 15, 60, 240]
SH = (3, 2, 2, G.NE, G.NST, G.NV, 6 + 2 * G.NK)

def run_market(m):
    sp = ppdata.SPEC[m]
    for tf in TFS:
        acc = np.zeros(SH); accR = np.zeros(SH); nsig = 0
        for d in ppdata.series(m, tf):
            t0 = time.time()
            S = bfeng.signals(d)
            flipUp, flipDn, buX, beX, sess, mn = bar_arrays(d, S)
            per = (d.per.values == 'P2').astype(np.int64); fI = S['fI']
            if len(fI) == 0: continue
            mk = in_win(mn[fI], 0, 1440).astype(np.int64) | (in_win(mn[fI], 585, 720).astype(np.int64) << 1)
            base = (S['o'], S['h'], S['l'], S['c'], S['trend'], S['lnW'], S['atr'], flipUp, flipDn)
            busy = np.full((3, 2, G.NE, G.NST, G.NV), -10, np.int64)
            G.grade(*base, buX, beX, fI, S['fS'].astype(np.int64), S['fC1'].astype(np.int64), S['fW1'], S['fSW'], mk, per[fI],
                    sp['stop'], sp['cost'], sp['tick'], 100, 10, acc, busy)
            rng = np.random.default_rng(23 + tf); n = len(d)
            ri = np.where(rng.random(n) < len(fI) / n)[0]; ri = ri[(ri > 20) & (ri < n - 2)]
            rm = in_win(mn[ri], 0, 1440).astype(np.int64) | (in_win(mn[ri], 585, 720).astype(np.int64) << 1)
            rs = np.where(rng.random(len(ri)) < 0.5, 1, -1).astype(np.int64)
            po = np.where(rs == 1, S['l'][ri - 1], S['h'][ri - 1]).astype(float)
            busy = np.full((3, 2, G.NE, G.NST, G.NV), -10, np.int64)
            G.grade(*base, buX, beX, ri.astype(np.int64), rs, (ri - 1).astype(np.int64), po, po, rm, per[ri],
                    sp['stop'], sp['cost'], sp['tick'], 100, 10, accR, busy)
            nsig += len(fI)
            print(m, tf, d.src.iloc[0], 'signals', len(fI), f'{time.time() - t0:.1f}s', flush=True)
        if nsig:
            np.savez_compressed(f'g4/{m}_{tf}.npz', cds=acc.astype(np.float32), rnd=accR.astype(np.float32))

if __name__ == '__main__':
    for m in sys.argv[1:]: run_market(m)
