# MMM Body Flip Trend: full test (Nov 2 2026)

Results sheet: artifact **"MMM Body Flip Test"**. Research only, not advice.

## What was tested
**The rule** was copied from the indicator:
- **Body closes:**
  - BuBC = a green close above the prior high.
  - BeBC = a red close below the prior low.
  - Everything else is an NBC.
- **C1:** the 1st opposite body close.
- **C2:** the next same-side body close with a body of 50%+ of C1 = CDS / CDL.
  - A smaller one becomes the new C1.
  - A close past the boundary cancels the setup (✕).
- **Trend line:** starts at the C1 wick and steps when a bigger trend body close prints.
- **ATR stop line:** the trend-line candle wick ± k × live ATR(14).

**Markets:**
- **NQ / MNQ:**
  - P1 = NQ 1m from Dec 2022 to Nov 2025 (757 days).
  - P2 = MNQ 2026.
- **ES / MES, gold, crude:** Dec 2025 – Oct 28 2026. P1 and P2 are the first and second half of each chart's own data.

**Charts:** 1m, 2m, 3m, 5m, 10m, 15m, 30m and 1h. Gold and crude have no 1m–3m data.

**The tests:**
- **A: what happens after each CDS / CDL.**
  - BC run before an opposite BC and before the first NBC.
  - Move after 1, 3, 5 and 10 candles.
  - Does price travel 1R / 2R / 3R before a close back past C1?
  - A fixed-stop 1:2 trade.
  - Failed setups (✕).
  - Splits by C2 size, delta, C1 resets, BIG C1 and higher-timeframe trend.
- **B: the full trade grid.**
  - 6 entries × 8 stops × 7 targets × 9 exits × half-out or not.
  - Long, short and both.
  - 8 time windows and 12 filters, including 09:45–12:00, C, A, Asia, London and PM.
- **C / D: 18 setting variants.**
  - C2 % at 30 / 40 / 60 / 75 / 100.
  - Boundary on the wick.
  - Max wait 5 / 10 / 20.
  - Delta check on.
  - Line step at 75 / 125 / 150%.
  - Step on any candle color.
  - Line on the body.
  - ATR fixed at the step.
  - ATR length 7 and 21.
- **E / F:**
  - Daily rules (max 3 trades, stop after 2 losses).
  - A 50k prop evaluation sim.
- **Controls:** random entries ran beside every test: a random side, and a random candle in the trend direction.

**PASS** = a t-score of 2+ in both periods, with 30+ trades in P1 and 20+ in P2.

## Short answer
- **No edge.** CDS / CDL entries do not beat random entries on any market, chart, window, filter or setting.
- **Full grid (all hours + 09:45–12:00):** 6 of 634,284 CDS / CDL combos passed. Random entries passed 166 of 1,146,852.
- **After a CDS / CDL, price moves like it does after a random candle:** about 0 after 1, 3, 5 and 10 candles everywhere.
  - The BC run is a little longer: 1.4 vs 1.2 BCs. That is mostly built in, because C2 is itself a body close.
- **The classic trade** (market at C2, fixed 50 pt stop, 1:2) loses on NQ on every chart from 1m to 15m in 2022–25 and is about 0 on 30m and 1h.
  - 15m: avg RR −0.03 → +0.01.
  - 5m, 09:45–12:00: −0.08 → −0.20.

## The exit question (close past the trend line but not the ATR line)
- These exits give almost the same result: close past the trend line, close past the ATR line × 0.5 or × 1, and the opposite CDS / CDL. All are near 0.
- A wick touch of the ATR line is the worst exit, because it shakes you out most.
- A close past the trend line that stays inside the ATR room is not a useful warning in either direction.
- The entry has no edge, so no exit can fix it.

## What looked good and why it is not real
- **NQ 10m long, market at C2, ATR × 2 trailing stop, ride:**
  - avg RR +0.06 (t 2.6) → +0.13 (t 2.0).
  - With daily rules: t 3.2 / 2.2, prop pass rate 49%.
  - Random long entries with the same stop and exit: +0.12 → +0.12.
  - The gain is NQ rising plus a wide trailing stop, not the signal.
- **The other passes are small clusters, the size luck gives:**
  - Gold 15m shorts with C2 at 75–100% of C1: 68 + 71 trades.
  - ES 3m 09:45–12:00 limit at the CDS / CDL line: 31 + 29 trades.
  - NQ 30m longs with the higher-timeframe trend: 468 + 140 trades.

## Settings
None of the 18 variants changes the picture. Pass counts stay at luck level, and the classic trade stays near 0 or below.

## What it means
- **Use the Body Flip Trend to read the chart:** who is in control, where the protected C1 sits, how big a body the other side needs. Do not use it as an entry signal.
- **For trading,** keep the strategies that did pass, like EDGE PRO X.M4 on NQ.

## Files
- Session folder: /home/claude/bf.
- Scripts:
  - bfeng.py: the engine.
  - bfgrid.py: the grader.
  - bfrun.py: the grid.
  - bffound.py: test A.
  - bfvar.py: the settings variants.
  - bfprop.py: the prop checks.
- Results: grid_base_all.parquet, found_base.parquet, variants.parquet, prop.parquet.
