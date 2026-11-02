# MMM Body Flip: C1 / C2 retest test (Nov 2 2026)

Results sheet: artifact **"MMM C1 / C2 retest"**. Research only, not advice.

## What was tested
- **Signal:** every CDS / CDL from the MMM Body Flip Trend, with default settings and the new BuBC / BeBC rule.
- **Entries (22):**
  - Market at the C2 close.
  - A limit inside the **last C1** range, the **strongest C1** range, or the **C2** range, at 0, 12.5, 25, 50, 75, 87.5 and 100% depth.
  - Long: 0% = top of the candle, 100% = its low. Short: 0% = bottom, 100% = its high.
  - 100% of a C1 range is the PO4 line.
  - The limit lives 10 or 30 candles. An opposite flip cancels it.
- **Stops (only these):**
  - PO4 at the last C1 wick.
  - PO4 at the strongest C1 wick.
  - Trailing ATR line ×0.5, ×1, ×1.5 and ×2.
  - Fixed 20 / 40 / 50 / 60 pts on NQ.
  - Other markets use the same size vs their normal stop: ES 8 / 16 / 20 / 24, gold 4.8 / 9.6 / 12 / 14.4, crude 0.20 / 0.40 / 0.50 / 0.60.
- **Targets:** 1:2, 1:3, 1:4, 1:5, 1:6 or no target.
- **Exits:** stop and target only, or also exit at the close of the next opposite flip.
  - "Target = next flip" = no target + next-flip exit.
- **Charts:** 1m, 2m, 3m, 5m, 10m, 15m, 1h and 4h.
  - 4h candles start at 18:00 New York.
  - Gold and crude have no 1m–3m data.
- **Markets:**
  - NQ / MNQ: P1 = NQ 2022–25, P2 = MNQ 2026.
  - ES, gold and crude: the first and second half of each chart's own days.
- **Cuts:** long, short and both. All hours and 09:45–12:00.
- **Controls:** random entries with the same entries, stops and exits.
  - One with a random side.
  - One in the trend direction.
- **Size:** 475,000 CDS / CDL combos with 30+ / 20+ trades.
- **PASS** = a t-score of 2+ in both periods, with 30+ trades in P1 and 20+ in P2.
- **Grader check:** it matches the earlier grader trade for trade.

## Short answer
- **No edge.**
  - 8 of 475,000 CDS / CDL combos pass.
  - Random entries pass 157 of 825,000 combos.
- **Deeper retest = worse.**
  - Limits at 75–87.5% of the C1 range are the worst entries: avg RR −0.4 to −0.8 with the PO4 stop.
  - The stop is tiny, so cost and noise eat it.
  - A deep fill usually means the flip is failing.
- **Shallow C2 range limits (12.5–25%)** are about the same as market at the C2 close. Neither is positive.
- **NQ, PO4 stop, 1:2:** across all 22 entries and 8 charts, only one row is positive in both periods.
  - 1h market with the strongest-C1 PO4: avg RR +0.01 / +0.02.
  - That is flat.

## Each chart (NQ, market at C2, 1:2, both sides, all hours)
avg RR P1 / P2 for each stop.

| Chart | PO4 last | PO4 strongest | ATR ×1 | ATR ×2 | Fixed 20 | Fixed 40 | Fixed 50 | Fixed 60 |
|---|---|---|---|---|---|---|---|---|
| 1m | −0.13 / −0.13 | −0.12 / −0.11 | −0.10 / −0.11 | −0.08 / −0.08 | −0.06 / −0.10 | −0.03 / −0.04 | −0.03 / −0.05 | −0.02 / −0.05 |
| 2m | −0.12 / −0.13 | −0.11 / −0.11 | −0.08 / −0.07 | −0.06 / −0.05 | −0.06 / −0.15 | −0.03 / −0.05 | −0.03 / −0.04 | −0.02 / −0.07 |
| 3m | −0.09 / −0.06 | −0.08 / −0.06 | −0.06 / −0.04 | −0.04 / −0.04 | −0.07 / −0.10 | −0.04 / −0.07 | −0.02 / −0.06 | −0.02 / −0.12 |
| 5m | −0.08 / −0.06 | −0.07 / −0.05 | −0.05 / −0.05 | −0.02 / −0.02 | −0.06 / −0.11 | −0.03 / −0.04 | −0.03 / −0.05 | −0.02 / −0.04 |
| 10m | −0.06 / −0.05 | −0.05 / −0.06 | −0.01 / −0.02 | −0.01 / −0.01 | −0.07 / −0.13 | −0.02 / −0.06 | −0.02 / −0.06 | −0.02 / −0.09 |
| 15m | −0.04 / −0.02 | −0.03 / +0.01 | −0.02 / +0.02 | +0.00 / +0.02 | −0.08 / −0.11 | −0.01 / +0.02 | −0.03 / +0.01 | −0.01 / +0.00 |
| 1h | −0.01 / +0.00 | +0.01 / +0.02 | +0.02 / −0.01 | −0.01 / +0.04 | −0.19 / −0.22 | +0.00 / −0.05 | +0.02 / +0.03 | +0.04 / −0.04 |
| 4h | −0.00 / −0.24 | −0.04 / −0.25 | +0.03 / −0.06 | +0.06 / +0.04 | −0.42 / −0.62 | −0.16 / −0.11 | −0.06 / −0.04 | −0.14 / −0.16 |

- **1m to 10m:** every stop loses in both periods.
- **15m and 1h:** about 0. The best is fixed 50 on 1h: WR 35% / 36%, avg RR +0.02 / +0.03, PF 1.03 / 1.05, t 0.5 / 0.4. That is flat.
- **4h:** too few trades (307 / 94) to trust. Only ATR ×2 is above 0 in both, at t 1.0 / 0.3.
- **Passes per chart:** only NQ 10m (the long ATR ×2 ride) and gold 15m pass. No ES or crude chart passes.
- **Best combo per chart:** it never reaches t 2 in both periods on NQ 1m–5m or 15m–4h. Most of the best NQ rows are long-only, and random long entries score in the same range, because NQ went up.

## Fixed stops 20 / 40 / 50 / 60
- **20 pts is the worst stop from 10m up.** It is too tight, so normal noise hits it.
- **40 to 60 pts** mostly lose less than the PO4 stop on 1m–5m (smaller stop = cost eats more), but they still lose.
- **On 15m and 1h,** 40 / 50 / 60 are about 0.
- **The difference between 40, 50 and 60 is small.** None of them turns the signal into an edge.

## Stops
- **Strongest-C1 PO4 vs last-C1 PO4:**
  - The strongest loses a little less on NQ, gold and crude, because the stop is wider and costs eat less of it.
  - On ES it is the reverse.
  - Both lose.
  - The two lines differ on about 1 flip in 6 on 5m / 15m and 1 in 4 on 4h.
- **ATR trailing stops:** the wider the stop, the closer to 0 (×2 is best).
  - Random entries show the same pattern, so it is the stop, not the signal.

## Targets and the next-flip exit
- **1:2 to 1:6 and the next-flip exit all give about the same result.**
  - NQ mean avg RR is −0.08 to −0.12 for 1:2 to 1:6, with or without the flip exit.
  - No target: −0.01 / −0.07.
- **"Target = next flip"** (no target + flip exit) is no better than a fixed target.

## The 8 passes
- **NQ 10m long, market at C2, ATR ×2, no target:**
  - WR 36% / 38%, avg RR +0.06 / +0.13, t 2.6 / 2.0.
  - This is the same row as the last test. Random long entries do as well (+0.12 / +0.12).
- **Gold 15m, both sides, 09:45–12:00, limit at 12.5% of the last C1 range (6 rows):**
  - Best: fixed 9.6 pts (= NQ 40), 1:2 + next-flip exit, wait 30: 49 / 43 trades, WR 53% / 51%, avg RR +0.48 / +0.47, PF 2.10 / 2.07, t 2.4 / 2.2.
  - The PO4, ATR ×1 and other fixed-stop versions pass too.
  - Over all hours the same setup loses (−0.07 / −0.05).
  - Only about 45 trades per period, and only the 0–25% levels are positive.
  - It is a small window pocket. Watch it; do not trade it.

## What it means
- Buying the pullback into C1 or C2 after a flip does not beat a random entry with the same stop.
- Keep the PO4 and ATR lines for reading the chart and placing stops. They are not an entry edge.

## Indicator change
- New input **"PO4 From": Last C1 / Strongest C1.**
  - It is in the Labels group, under the BePO4 / BuPO4 line.
  - Strongest = the biggest C1 body in a chain of C1s that replaced each other.
  - The label says "(strongest C1)" when it differs from the last C1.
  - The trend line still starts at the last C1.

## Files
- **Scripts:**
  - bfeng.py now also stores the strongest C1.
  - bfgrid2.py is the grader (now with fixed 20 / 40 / 50 / 60).
  - bfrun2.py is the driver.
  - agg3.py and agg4.py are the summaries.
- **Results:** grid2_NQ / ES / GC / CL.parquet.
