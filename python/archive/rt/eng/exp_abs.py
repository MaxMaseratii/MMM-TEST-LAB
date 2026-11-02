"""B. Absorption inside boxes and at their edges (MNQ footprint Jul 8 - Oct 16 2026, 5m / 10m / 15m).
Box = the MMM x box (BC expander + candles that close back inside, G1 grow). It ends on the first close outside.
For each finished box: which edge broke, and do the footprint numbers inside the box say it in advance?"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/rt/eng')
from core import *
from zone import zone_engine
import data as D
OUT = '/home/claude/rt/out'

def run():
    m1, m5, bars, fpd, dd = D.fresh()
    recs = []
    for tf in ['5m', '10m', '15m']:
        sig = bars[tf]
        _, _, _, j = D.fp_levels(sig, fpd[tf])
        has = ~j.DELTA.isna().values
        o, h, l, c, v = [sig[k].values for k in ('open', 'high', 'low', 'close', 'volume')]
        dl = j.DELTA.values; bv = j['BUY VOL'].values; sv = j['SELL VOL'].values
        stb = j['STACK BUY'].values; sts = j['STACK SELL'].values
        poc = (j.close + j['POC-CLOSE']).values
        a = atr(sig)
        vol = bv + sv
        rg = np.maximum(h - l, TICK)
        vpr = vol / rg                                   # volume per point = "effort per result"
        vpr_med = pd.Series(vpr).rolling(200, min_periods=50).median().values
        vol_med = pd.Series(vol).rolling(200, min_periods=50).median().values
        ty, pos, isBuX, isBeX, nbc = mmcb(sig)
        for em, mode in ((False, 'CONTRACTION'), (True, 'EXPANDER')):
            z = zone_engine(o, h, l, c, v, True, em)
            ends = np.where(z['end_f'])[0]
            for i in ends:
                t0 = z['end_t0'][i]
                if t0 < 0 or i - t0 < 2 or i + 3 >= len(c):
                    continue
                k = np.arange(t0 + 1, i)       # candles inside the box (after the expander)
                if not has[k].all() or not has[t0]:
                    continue
                H, L = z['end_h'][i], z['end_l'][i]
                W = H - L
                up = c[i] > H
                top = h[k] >= H - .15 * W
                bot = l[k] <= L + .15 * W
                absorb = (vpr[k] > 1.5 * vpr_med[k]) & (vol[k] > vol_med[k])     # big volume, small move
                mid = (H + L) / 2
                rec = dict(tf=tf, box=mode, candles=len(k), up=up,
                           net_delta=dl[k].sum(), exp_delta=dl[t0], exp_dir=1 if c[t0] > o[t0] else -1,
                           delta_top=dl[k][top].sum() if top.any() else 0.0, n_top=top.sum(),
                           delta_bot=dl[k][bot].sum() if bot.any() else 0.0, n_bot=bot.sum(),
                           abs_top=(absorb & (poc[k] > mid)).sum(), abs_bot=(absorb & (poc[k] <= mid)).sum(),
                           abs_top_buyers=(absorb & (poc[k] > mid) & (dl[k] > 0)).sum(),
                           abs_top_sellers=(absorb & (poc[k] > mid) & (dl[k] < 0)).sum(),
                           abs_bot_buyers=(absorb & (poc[k] <= mid) & (dl[k] > 0)).sum(),
                           abs_bot_sellers=(absorb & (poc[k] <= mid) & (dl[k] < 0)).sum(),
                           stack_buy=stb[k].sum(), stack_sell=sts[k].sum(),
                           last_delta=dl[i - 1], poc_side=np.sign(np.nanmean(poc[k]) - mid),
                           brk_delta=dl[i], last_pos=(c[i - 1] - L) / W if W > 0 else .5,
                           # after the break: does it keep going? next BC with the break before one against
                           width_atr=W / a[i] if a[i] > 0 else np.nan)
                # follow-through: first BC after the break bar
                s = 1 if up else -1
                q = i + 1; ft = np.nan
                while q < len(c) and q < i + 50:
                    if isBuX[q] and not isBeX[q]: ft = (s == 1); break
                    if isBeX[q] and not isBuX[q]: ft = (s == -1); break
                    q += 1
                rec['follow_through'] = ft
                rec['move_3_atr'] = s * (c[min(i + 3, len(c) - 1)] - c[i]) / a[i]
                recs.append(rec)
    df = pd.DataFrame(recs)
    df.to_parquet(f'{OUT}/ABS_boxes.parquet')
    return df

if __name__ == '__main__':
    df = run()
    print(len(df), df.groupby(['tf', 'box']).up.agg(['size', 'mean']))
