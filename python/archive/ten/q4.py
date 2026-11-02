"""Q4: BC runs (same-side body closes until the first opposite BC) on 5m, 15m, 1h"""
import json
from common import *

TD = pd.Timedelta

def walk(bc, hi, lo, cl, i):
    s = bc[i]; cnt = 1; nbc = 0; j = i + 1; last = cl[i]
    while j < len(bc) and bc[j] != -s:
        if bc[j] == s: cnt += 1; last = cl[j]
        else: nbc += 1
        j += 1
    ended = j < len(bc)
    ext = hi[i:j].max() - cl[i] if s == 1 else cl[i] - lo[i:j].min()
    to_last = (last - cl[i]) * s
    return cnt, nbc, ext, to_last, j, ended

def bucket(t):
    h = t.hour + t.minute / 60
    if 9.5 <= h < 11.5: return 'NY AM 09:30-11:30'
    if 11.5 <= h < 14: return 'midday 11:30-14:00'
    if 14 <= h < 16: return 'NY PM 14:00-16:00'
    if 8 <= h < 9.5: return 'pre 08:00-09:30'
    if 2 <= h < 8: return 'London 02:00-08:00'
    if h >= 18 or h < 2: return 'Asia 18:00-02:00'
    return 'after 16:00-18:00'

BUCKETS = ['Asia 18:00-02:00', 'London 02:00-08:00', 'pre 08:00-09:30', 'NY AM 09:30-11:30', 'midday 11:30-14:00', 'NY PM 14:00-16:00', 'after 16:00-18:00']

def run(key):
    d1 = raw()[key]; days = good_days(d1); out = {}
    allruns = {}
    for tf in ['5m', '15m', '1h']:
        m = TFMIN[tf]
        B = bars(key, tf)
        bc = B.bc.values; hi = B.high.values; lo = B.low.values; cl = B.close.values; idx = B.index
        pos = {t: k for k, t in enumerate(idx)}
        recs = []
        for day in days:
            t10 = day + TD(hours=10) - TD(minutes=m)
            if t10 not in pos: continue
            k10 = pos[t10]; ty10 = B.type.iloc[k10]
            for start_after in ['09:30', '10:00']:
                sa = day + pd.Timedelta(start_after + ':00')
                # first bar whose CLOSE is after start_after, same day, opening before 16:00
                lo_k = np.searchsorted(idx.values, (sa - TD(minutes=m) + TD(minutes=1)).to_datetime64())
                k = lo_k
                while k < len(bc) and idx[k] < day + TD(hours=16) and bc[k] == 0: k += 1
                if k >= len(bc) or idx[k] >= day + TD(hours=16): continue
                cnt, nbc, ext, tl, j, ended = walk(bc, hi, lo, cl, k)
                side = 'bull' if bc[k] == 1 else 'bear'
                recs.append(dict(day=str(day.date()), start=start_after, side=side, t_first=str(idx[k].time()),
                                 cnt=cnt, nbc=nbc, ext=ext, to_last=tl, ended=ended,
                                 dur_min=((idx[j] if ended else idx[-1]) - idx[k]).total_seconds() / 60,
                                 end_time=str(idx[j]) if ended else None, end_before16=ended and idx[j] < day + TD(hours=16),
                                 t10=ty10, fam10=family(ty10), lean10=lean(ty10), same10=(lean(ty10) == side)))
        df = pd.DataFrame(recs); df['tf'] = tf
        # all runs, segmented over the full series
        nz = np.flatnonzero(bc)
        starts = [nz[0]] + [nz[t] for t in range(1, len(nz)) if bc[nz[t]] != bc[nz[t - 1]]]
        ar = []
        for k in starts:
            cnt, nbc, ext, tl, j, ended = walk(bc, hi, lo, cl, k)
            if not ended: continue
            ar.append(dict(t=idx[k], side='bull' if bc[k] == 1 else 'bear', cnt=cnt, nbc=nbc, ext=ext, to_last=tl,
                           bucket=bucket(idx[k]), dur_min=(idx[j] - idx[k]).total_seconds() / 60))
        ar = pd.DataFrame(ar)
        out[tf] = df; allruns[tf] = ar
    return out, allruns

def stats(g, k):
    n = len(g)
    c = g.cnt
    return {'key': k, 'n': n, 'avg BC count': mean(c.tolist()), 'med BC count': med(c.tolist()),
            '1 BC%': pct((c == 1).sum(), n), '2 BC%': pct((c == 2).sum(), n), '3 BC%': pct((c == 3).sum(), n),
            '4 BC%': pct((c == 4).sum(), n), '5+ BC%': pct((c >= 5).sum(), n),
            'med pts to run extreme': med(g.ext.tolist()), 'avg pts to run extreme': mean(g.ext.tolist()),
            'p75 pts to extreme': q(g.ext.tolist(), 75),
            'med pts to last BC close': med(g.to_last.tolist()),
            'avg NBCs in run': mean(g.nbc.tolist()), 'med NBCs': med(g.nbc.tolist()),
            'med run minutes': med(g.dur_min.tolist()),
            'got 2nd BC%': pct((c >= 2).sum(), n), '2nd->3rd%': pct((c >= 3).sum(), (c >= 2).sum()),
            '3rd->4th%': pct((c >= 4).sum(), (c >= 3).sum()), '4th->5th%': pct((c >= 5).sum(), (c >= 4).sum())}

def tables(df, ar):
    res = {}
    for st in ['09:30', '10:00']:
        g0 = df[df.start == st]; rows = [stats(g0, 'ALL')]
        for sd in ['bull', 'bear']: rows.append(stats(g0[g0.side == sd], sd + ' runs'))
        rows.append(stats(g0[g0.same10], 'run side = 10:00 candle lean')); rows.append(stats(g0[~g0.same10], 'run side AGAINST 10:00 candle lean'))
        for f in FAMS:
            rows.append(stats(g0[g0.fam10 == f], f'10:00 candle {f}'))
        for f in FAMS:
            for same in [True, False]:
                rows.append(stats(g0[(g0.fam10 == f) & (g0.same10 == same)], f'10:00 {f} / run {"WITH" if same else "AGAINST"} its lean'))
        res[f'first BC after {st}'] = rows
        res[f'first BC after {st} - ends before 16:00%'] = pct(g0.end_before16.sum(), len(g0))
    rows = []
    for b in BUCKETS: rows.append(stats(ar[ar.bucket == b], b))
    rows.append(stats(ar[ar.bucket != 'NY AM 09:30-11:30'], 'ALL OTHER HOURS'))
    rows.append(stats(ar, 'ALL RUNS'))
    for b in ['NY AM 09:30-11:30']:
        for sd in ['bull', 'bear']: rows.append(stats(ar[(ar.bucket == b) & (ar.side == sd)], f'{b} {sd}'))
    res['all runs by start hour'] = rows
    return res

if __name__ == '__main__':
    res = {}
    for key, name in PERIODS.items():
        out, ar = run(key); res[name] = {}
        for tf in out:
            out[tf].to_csv(f'/home/claude/ten/q4_{key}_{tf}_firstBC.csv', index=False)
            res[name][tf] = tables(out[tf], ar[tf])
            print(name, tf, len(out[tf]), len(ar[tf]))
    json.dump(res, open('/home/claude/ten/q4.json', 'w'), indent=1, default=str)
