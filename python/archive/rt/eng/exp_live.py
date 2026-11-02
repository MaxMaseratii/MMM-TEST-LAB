"""Live balance-zone control: at EVERY candle that closes inside a live MMM x box (what an indicator sees in real time),
which edge breaks first? Features known at that close only: close location in the box, candles so far,
box delta so far (footprint), last candle delta, location of the closes so far (average)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/rt/eng')
from core import *
from zone import zone_engine
import data as D
OUT = '/home/claude/rt/out'

def study(sig, period, tf, fp=None):
    o, h, l, c, v = [sig[k].values for k in ('open', 'high', 'low', 'close', 'volume')]
    a = atr(sig)
    z = zone_engine(o, h, l, c, v, True, False)
    n = len(c)
    # end of each box (by its expander index)
    endmap = {}
    for j in np.where(z['end_f'])[0]:
        endmap[z['end_t0'][j]] = j
    dl = fp['DELTA'].values if fp is not None else None
    recs = []
    cum = {}; cnt = {}; possum = {}
    for i in range(1, n):
        if not z['z_live'][i]:
            continue
        t0 = z['z_t0'][i]
        j = endmap.get(t0)
        if j is None or j <= i:
            continue
        H, L = z['z_h'][i], z['z_l'][i]
        W = H - L
        if W <= 0:
            continue
        pos = (c[i] - L) / W
        cnt[t0] = cnt.get(t0, 0) + 1
        possum[t0] = possum.get(t0, 0.0) + pos
        rec = dict(period=period, tf=tf, k=cnt[t0], pos=pos, avgpos=possum[t0] / cnt[t0],
                   up=c[j] > z['end_h'][j], bars_left=j - i, width_atr=W / a[i] if a[i] > 0 else np.nan,
                   # points: with-break move after the break (3 candles), signed by the predicted side later
                   brk_close=c[j], now_close=c[i], H=H, L=L, ev_side=z['side'][i])
        if dl is not None and not np.isnan(dl[i]):
            cum[t0] = cum.get(t0, 0.0) + dl[i]
            rec['cumdelta'] = cum[t0]; rec['lastdelta'] = dl[i]
        recs.append(rec)
    return pd.DataFrame(recs)

if __name__ == '__main__':
    R = []
    m1, bars = D.old()
    for tf in ['5m', '15m', '1h']:
        R.append(study(bars[tf], 'NQ 2022-25', tf)); print('old', tf, flush=True)
    m1, m5, fb, fpd, dd = D.fresh()
    for tf in ['5m', '10m', '15m']:
        _, _, _, j = D.fp_levels(fb[tf], fpd[tf])
        R.append(study(fb[tf], 'MNQ Jul-Oct 26', tf, j)); print('fresh', tf, flush=True)
    df = pd.concat(R, ignore_index=True)
    df.to_parquet(f'{OUT}/LIVE_box.parquet')
    df['third'] = pd.cut(df.pos, [-.01, 1 / 3, 2 / 3, 1.01], labels=['bottom', 'middle', 'top'])
    print(df.groupby(['period', 'tf', 'third']).up.agg(['size', 'mean']).round(3).to_string())
