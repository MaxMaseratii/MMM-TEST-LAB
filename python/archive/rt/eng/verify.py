"""Independent slow check of the simulator on random rows (fresh 15m, 5m replay)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/rt/eng')
from core import *
import data as D
from exp_a import build_rows, datr_prev_map, RK

m1, m5, bars, fpd, dd = D.fresh()
sig = bars['15m']; rep = m5
types_, pos, isBuX, isBeX, nbc = mmcb(sig)
side_of = np.where(types_ >= 0, TSIDE[np.clip(types_, 0, 15)], 0)
sess = session(sig.index)
poc, vah, val, _ = D.fp_levels(sig, fpd['15m'])
datr = datr_prev_map(sig.index, dd, False)
rows, en = build_rows(sig, types_, side_of, (poc, vah, val), datr, sess)
rng = np.random.default_rng(1)
pick = rng.choice(len(rows), 400, replace=False)
rows = rows[pick]
sF, sL, r2s = map_replay(sig, rep)
evN = exit_events(sig)
c = sig.close.values
for (k, x) in [(1, 0), (1, 2), (5, 1), (2, 8)]:
    acc, cnt, keep = simulate(rep.open.values, rep.high.values, rep.low.values, rep.close.values, sF, sL, r2s, c, len(sig),
                              rows[:, 0].astype(np.int64), rows[:, 1].astype(np.int64), rows[:, 2], rows[:, 3], rows[:, 4],
                              np.zeros(len(rows), np.int64), 1, RK, evN, EXIT_MO, 5, 100, 1.0, 2.0, TICK, k, x)
    # slow re-implementation
    ro, rh, rl = rep.open.values, rep.high.values, rep.low.values
    rt = rep.index
    st_t = sig.index
    ev_long = evN[0, x]; ev_short = evN[1, x]
    bad = 0; tot = 0
    for r, row in enumerate(rows):
        j, s, L, stp, tg = int(row[0]), int(row[1]), row[2], row[3], row[4]
        # replay bars after the signal close
        t_close = st_t[j + 1] if j + 1 < len(st_t) else None
        idx = np.where(rt >= t_close)[0]
        if np.isnan(L):
            e = c[j]; fi = idx[0] - 1; g = j + 1
        else:
            d0 = s * (L - stp)
            if d0 < 2:
                assert np.isnan(keep[r]); continue
            canc = L + s * 2 * d0
            lim_end = st_t[j + 6] if j + 6 < len(st_t) else rt[-1] + pd.Timedelta('1min')
            fi = None
            for i in idx:
                if rt[i] >= lim_end: break
                if (s == 1 and rl[i] <= L - .25) or (s == -1 and rh[i] >= L + .25):
                    e = min(L, ro[i]) if s == 1 else max(L, ro[i]); fi = i; break
                if (s == 1 and rh[i] >= canc) or (s == -1 and rl[i] <= canc): break
            if fi is None:
                assert np.isnan(keep[r]), (r, keep[r]); continue
            g = np.searchsorted(st_t, rt[fi], 'right') - 1
        d = s * (e - stp)
        if d < 2:
            assert np.isnan(keep[r]); continue
        if k < 5:
            tp = e + s * RK[k] * d
        else:
            if not (s * (tg - e) > 0):
                assert np.isnan(keep[r]); continue
            tp = tg
        endsig = min(g + 99, len(st_t) - 1)
        ej = (ev_long if s == 1 else ev_short)[min(g + EXIT_MO[x], len(st_t))]
        ej = min(ej, endsig)
        ex_t_end = st_t[ej + 1] if ej + 1 < len(st_t) else rt[-1] + pd.Timedelta('1min')
        res = None
        # fill bar stop
        if not np.isnan(L) and ((s == 1 and rl[fi] <= stp) or (s == -1 and rh[fi] >= stp)):
            res = s * (stp - e) / d
        if res is None:
            for i in range(fi + 1, len(rt)):
                if rt[i] >= ex_t_end:
                    res = s * (c[ej] - e) / d; break
                if (s == 1 and rl[i] <= stp) or (s == -1 and rh[i] >= stp):
                    px = min(ro[i], stp) if s == 1 else max(ro[i], stp); res = s * (px - e) / d; break
                if (s == 1 and rh[i] >= tp) or (s == -1 and rl[i] <= tp):
                    res = s * (tp - e) / d; break
            if res is None:
                res = s * (c[ej] - e) / d
        res -= 1 / d
        tot += 1
        if not np.isclose(res, keep[r], atol=1e-6):
            bad += 1
            if bad < 4: print('mismatch', k, x, r, row, res, keep[r])
    print('target', k, 'exit', EXITS[x], 'checked', tot, 'mismatches', bad)
