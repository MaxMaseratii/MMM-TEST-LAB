# MMM XB Zone Test: do XBS / XBB / Balanced / FVA work as predicted? (Oct 30 2026)

## Verdict: NO. The zones do not predict direction.

- **0 of 3,168 pairings passed** (t-score 2+ in both periods, n 30+ / 20+).
- **Coin flip:** after the first real touch, price went 50 pts the predicted way first about **49%** of the time:
  - Predicted buy / sell zones (XBS buy, XBB sell, XB low / high): 49.6% → 48.7%
  - Balanced Zone (the "no-trade" zone): 49.7% → 49.5%
  - Wrong zone control (sell XBS, buy XBB): 49.8% → 49.6%
  - FVA after the break: 49.6% → 49.0%
- **The wrong-zone control did as well as the predicted zones.** If XBS were a real buy area, selling there would lose clearly. It did not.
- **Mean avg RR over all pairings** (opposite-side engine, P1 → P2): predicted zones −0.061 → −0.079 · Balanced −0.049 → −0.050 · wrong zone −0.045 → −0.041 · FVA −0.056 → −0.050. All lose about the cost.
- **Walk-forward** (best pairing per entry picked on 2022–25, checked on 2026): predicted zones +0.011 → −0.012 · Balanced +0.011 → −0.009 · wrong zone +0.010 → −0.014 · FVA +0.035 → −0.049.
- The 5m sells that look good in 2026 (e.g. SELL XBB bottom, 50 pt, 1:2: +0.07 avg RR, t 2.3) lost in 2022–25 (−0.04, t −4.3), and SELL XBS (wrong zone) did even better in 2026 (+0.11). That is the 2026 market, not the zone.
- **Use the XB as a map** (where the negotiation is, where the break happens). Do not use XBS / XBB / FVA as entry signals on their own.

## What was tested

- **Definitions (Max, Oct 30):**
  - XB = expander BC + NBCs, last high / low (grows with wicks), dies on a close outside.
  - Balanced Zone = top / bottom of the opens / closes inside the XB.
  - XBB (Buying Zone) = Balanced top → XB high = predicted SELL area. XBS (Selling Zone) = XB low → Balanced bottom = predicted BUY area.
  - BeFVA = first NBC body bottom → XB high (sell after a bearish break). BuFVA = first NBC body top → XB low (buy after a bullish break). Dies on a close through it.
- **Engines:** "Opposite side only" (XB born from a BC against the last BC, the new x 4.0 default) and "All XBs".
- **Data:** NQ 1m Dec 2022 – Dec 2025 (P1) · MNQ 2026 (P2, 5m from Mar 2026). Timeframes 5m, 15m, 1h, 4h.
- **Entries while the XB lives** (limit orders from the first NBC close to the break, level follows the block):
  - BUY XBS top (= Balanced bottom), BUY XBS middle, BUY XB low
  - SELL XBB bottom (= Balanced top), SELL XBB middle, SELL XB high
  - BUY / SELL Balanced middle (the no-trade zone)
  - BUY XBB bottom / SELL XBS top (wrong-zone control)
- **Entries after the break:** limit at the FVA near edge (first NBC body), middle, far edge (XB high / low), in the break direction, while the FVA lives (max 100 candles).
- **Fill rule:** a limit fills only on a TRUE touch: the 1m bar opens on the predicted side and trades through the level.
- **Stops:** fixed 50 pts · 1.5 × ATR(14) · past the XB / FVA far edge (2 ticks).
- **Targets:** 1:1, 1:2, 1:3.
- **Exits:** stop / target · violation close (the XB breaks against the trade / the FVA is closed through) · next session open (02:00, 08:00, 09:30 New York).
- 1 pt cost, stop wins ties, max hold 100 candles.

## Fixed 50 pt stop, 1:2 (opposite-side engine), avg RR P1 → P2 (t)

| TF | BUY XBS top | SELL XBB bottom | BUY Balanced mid | SELL Balanced mid | SELL XBS (wrong) | SELL BeFVA near | BUY BuFVA near |
|---|---|---|---|---|---|---|---|
| 5m | +0.006 → −0.042 | −0.043 → +0.068 | +0.012 → −0.041 | −0.045 → +0.042 | −0.046 → +0.106 | −0.050 → +0.091 | +0.015 → +0.019 |
| 15m | +0.005 → −0.019 | −0.021 → −0.002 | +0.000 → −0.030 | −0.035 → +0.004 | −0.028 → −0.106 | −0.020 → −0.043 | −0.014 → −0.082 |
| 1h | −0.036 → −0.004 | −0.055 → −0.022 | +0.038 → −0.048 | −0.072 → −0.008 | −0.076 → +0.012 | −0.082 → +0.112 | −0.021 → −0.094 |
| 4h | +0.097 → −0.045 | −0.043 → +0.014 | +0.093 → −0.012 | −0.096 → −0.020 | −0.083 → −0.114 | −0.138 → −0.231 | +0.052 → −0.163 |

Full grid and coin-flip tables: artifact "XB Zone Test" (claude.ai/artifact/NC7xeyp65JT9jHh3sBUyYN). Code: /home/claude/xb/xbzone2.py, agg_zone2.py.
