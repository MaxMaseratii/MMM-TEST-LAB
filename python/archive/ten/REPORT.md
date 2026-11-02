# 10:00 NY Study: MMCB candles, opening gaps, 10-14 pullback, BC runs, other-side gaps, runs to 11:30

**How to read every table:** each cell shows **2022-25 / 2026**. Example `62 / 55` = 62% in 2022-25 and 55% in 2026.

- **2022-25** = NQ 1-minute data, Dec 2022 to Dec 2025. **763 days.**
- **2026** = MNQ 1-minute data, Mar-May and Sep-Oct 2026. **61 days only.** This is a SMALL SAMPLE.
- A `*` after a row name = fewer than 30 cases in 2026. Treat that 2026 number as a guess, not a fact.
- Weekdays only. Days with any missing 1m bar from 09:30 to 09:59 were skipped.
- All times are New York. "pts" = NQ points. n = how many cases.
- Checks done before running: the 4H bar labelled 06:00 = the 1m bars 06:00 to 09:59 (same open, high, low, close). The candle classifier was tested on 16 hand-made candles (one per type) and on real candles.

**Words used:**
- **Lean** = the side the MMCB type points to (bull or bear). BuAFs- leans bear. BeAFs- leans bull.
- **BC** = body close. Bull BC = close above the previous candle high. Bear BC = close below the previous low. **NBC** = no body close.
- **Family** = BC+ (strong BC), BC- (weak BC), C2 (took both sides then closed beyond one), AFs (took one side, closed back inside), CI (inside candle), S&D (took both sides, closed inside).
- **Took HI first** = the next candle trades above this candle high before it trades below this candle low.

## Best per timeframe (summary of all 7 parts)

**One line:** at 10:00, trust a **BC+** candle (C2 a bit less) for the next candle's target, ignore a weak candle's direction, expect short runs (2 BCs) and take points before the opposite candle, latest 11:30.

**4H (06:00-10:00 candle)**
- BC+: next 4H candle takes the target first about 87-90% (2022-25), 75-78% (2026). C2: 77-85%.
- Weak 4H candle (BC-, AFs, CI, S&D): price goes to the open gap on the other side BEFORE the target 52% of the time. Wait at that gap.
- Does not tell you the 16:00 close. Pullback when right: median 34 / 65 pts, mostly before 10:30.

**1h (09:00-10:00 candle)**
- BC+: target first about 86-91% (2022-25), 91-100% (2026, small n). C2: 73-79%.
- Weak 1h candle: gap on the other side first 45%. Coin flip between gap and target.

**15m (09:45-10:00 candle)** — the best balance
- BC+: target first about 89-92% / 78-94%. (C2 at 10:00 on 15m is rare: under 20 cases.)
- Strong candle (BC+ or C2): the gap on the other side comes first only 12%.
- Run after 10:00: median 2 same-side BCs, about 2 NBCs, MFE median 36 pts (2026: 56). About half the runs are still alive at 11:30.
- Take 20-30 pts: reached 70 / 87% (20 pts) and 59 / 73% (30 pts) before the opposite candle.

**5m (09:55-10:00 candle)** — the fastest
- BC+: target first about 86-89% / 71-93%. The gap on the other side first only 5% (BC+ or C2).
- 5m UPG gaps made 09:30-10:00: touched 83 / 73%, react 63 / 68% (68 / 79% with the 4H lean).
- Run after 10:00: median 2 BCs, about 3 NBCs, MFE median 30-36 pts (2026: 36-46), ends in 25-35 minutes. Take 20 pts: reached 68 / 80%.

**What does NOT work:** BC- candles for direction (coin flip), the 10:00 lean for the 16:00 close, holding until the opposite candle (gives the points back), and the first BC after 10:00 as an entry with a 50 pt stop at 1:2 (no edge).

**Important:** sections 5-7 describe what price does, they are not tested strategies. MFE and "X pts reached" have no random baseline, and 2026 has only 61 days.

## 1. Candles that close at 10:00 NY

Candles: 4H 06:00-10:00, 1h 09:00-10:00, 15m 09:45-10:00, 5m 09:55-10:00. "Next candle" = the candle of the same timeframe that opens at 10:00. "16:00" = the 16:00 close compared to the 10:00 close.

**Most important:**
- **BC+ candles (strong close near the top or bottom) work.** The next candle takes the lean side high/low FIRST about 86-92% of the time, on every timeframe, in both periods. Think of it like a ball already at the door: the close sits right next to that extreme, so it gets hit first.
- **BC- candles (weak close) are close to a coin flip** for which side gets taken first (lean side first only about 42-61%). A body close alone is not enough; the close position matters.
- **The 10:00 lean does NOT tell you the 16:00 close.** On bear-lean days in 2022-25, NY still closed UP 52-57% of the time (the market went up a lot in those years). In 2026 it is about 50/50. Do not hold all day just because of the 10:00 candle.
- **4H 06-10 candle -> 10-14 candle:** the 10-14 candle takes the lean-side extreme first 75% (bull lean) / 71% (bear lean) in 2022-25, and 76% / 68% in 2026. But it only CLOSES beyond that extreme 45% / 34% of the time (2022-25). So: the high/low gets taken, but often the candle does not hold past it.

### 1.1 4H 06:00-10:00

**By type (share + who gets taken first + 16:00 close):**

| type | n | share % | took HI first % | took LO first % | took neither % | took lean side at all % | next candle same lean % | 16:00 UP % | 16:00 median pts (10:00 close to 16:00 close) |
|---|---|---|---|---|---|---|---|---|---|
| BuC2+ * | 63 / 7 | 8.3 / 11.5 | 92.1 / 100 | 4.8 / 0 | 3.2 / 0 | 92.1 / 100 | 68.3 / 71.4 | 61.7 / 42.9 | 34.2 / -3.5 |
| BuC2- * | 10 / 0 | 1.3 / 0 | 40 / - | 50 / - | 10 / - | 40 / - | 50 / - | 50 / - | 0.5 / - |
| BeC2+ * | 57 / 3 | 7.5 / 4.9 | 5.3 / 0 | 86 / 100 | 8.8 / 0 | 86 / 100 | 50.9 / 66.7 | 58.9 / 0 | 14.1 / -101 |
| BeC2- * | 18 / 0 | 2.4 / 0 | 27.8 / - | 50 / - | 22.2 / - | 50 / - | 33.3 / - | 77.8 / - | 43.2 / - |
| BuBC+ * | 126 / 9 | 16.5 / 14.8 | 90.5 / 77.8 | 7.1 / 0 | 2.4 / 22.2 | 91.3 / 77.8 | 63.5 / 44.4 | 62 / 33.3 | 26.8 / -65 |
| BuBC- * | 75 / 9 | 9.8 / 14.8 | 49.3 / 77.8 | 41.3 / 22.2 | 9.3 / 0 | 57.3 / 77.8 | 60 / 66.7 | 57.5 / 55.6 | 31.5 / 96 |
| BeBC+ * | 83 / 12 | 10.9 / 19.7 | 7.2 / 16.7 | 86.7 / 75 | 6 / 8.3 | 86.7 / 75 | 49.4 / 50 | 56.4 / 41.7 | 11.1 / -44.1 |
| BeBC- * | 66 / 5 | 8.7 / 8.2 | 40.9 / 40 | 45.5 / 40 | 13.6 / 20 | 51.5 / 60 | 47 / 60 | 54.7 / 40 | 15.8 / -32.8 |
| S&D.BuAF * | 38 / 3 | 5 / 4.9 | 68.4 / 0 | 23.7 / 66.7 | 7.9 / 33.3 | 68.4 / 0 | 63.2 / 66.7 | 51.4 / 33.3 | 3 / -8.2 |
| S&D.BeAF * | 43 / 0 | 5.6 / 0 | 25.6 / - | 62.8 / - | 11.6 / - | 65.1 / - | 39.5 / - | 60.5 / - | 27.2 / - |
| BuAFs+ * | 64 / 4 | 8.4 / 6.6 | 73.4 / 75 | 25 / 0 | 1.6 / 25 | 82.8 / 75 | 59.4 / 25 | 58.1 / 50 | 30.6 / -32.8 |
| BuAFs- * | 23 / 1 | 3 / 1.6 | 26.1 / 100 | 73.9 / 0 | 0 / 0 | 78.3 / 0 | 52.2 / 0 | 52.4 / 100 | 15.8 / 21.5 |
| BeAFs+ * | 60 / 7 | 7.9 / 11.5 | 23.3 / 28.6 | 75 / 71.4 | 1.7 / 0 | 78.3 / 71.4 | 48.3 / 14.3 | 50.9 / 85.7 | 0.2 / 81.5 |
| BeAFs- * | 14 / 0 | 1.8 / 0 | 50 / - | 50 / - | 0 / - | 57.1 / - | 78.6 / - | 46.2 / - | 0 / - |
| CI.BuAF * | 12 / 1 | 1.6 / 1.6 | 83.3 / 100 | 16.7 / 0 | 0 / 0 | 91.7 / 100 | 75 / 100 | 45.5 / 100 | -5.5 / 177 |
| CI.BeAF * | 10 / 0 | 1.3 / 0 | 40 / - | 60 / - | 0 / - | 70 / - | 50 / - | 50 / - | 4.6 / - |
| bull | 402 / 33 | 52.8 / 54.1 | 75.4 / 75.8 | 20.4 / 12.1 | 4.2 / 12.1 | 79.1 / 75.8 | 63.4 / 57.6 | 58.1 / 45.5 | 27.2 / -8.2 |
| bear * | 360 / 28 | 47.2 / 45.9 | 21.1 / 25 | 70.8 / 67.9 | 8.1 / 7.1 | 73.3 / 71.4 | 47.2 / 42.9 | 56.8 / 50 | 16 / 0.6 |
| ALL | 762 / 61 | 100 / 100 | 49.7 / 52.5 | 44.2 / 37.7 | 6 / 9.8 | 76.4 / 73.8 | 55.8 / 50.8 | 57.5 / 47.5 | 19.8 / -3.5 |

**By family and lean side (16:00 measured in the lean direction: + = moved the lean way):**

| family | n | took lean side FIRST % | took lean side at all % | next candle same lean % | 16:00 closed lean way % | 16:00 median pts lean way |
|---|---|---|---|---|---|---|
| BC+ bull * | 126 / 9 | 90.5 / 77.8 | 91.3 / 77.8 | 63.5 / 44.4 | 62 / 33.3 | 26.8 / -65 |
| BC+ bear * | 83 / 12 | 86.7 / 75 | 86.7 / 75 | 49.4 / 50 | 43.6 / 58.3 | -11.1 / 44.1 |
| BC- bull * | 75 / 9 | 49.3 / 77.8 | 57.3 / 77.8 | 60 / 66.7 | 57.5 / 55.6 | 31.5 / 96 |
| BC- bear * | 66 / 5 | 45.5 / 40 | 51.5 / 60 | 47 / 60 | 45.3 / 60 | -15.8 / 32.8 |
| C2 bull * | 73 / 7 | 84.9 / 100 | 84.9 / 100 | 65.8 / 71.4 | 60 / 42.9 | 28.1 / -3.5 |
| C2 bear * | 75 / 3 | 77.3 / 100 | 77.3 / 100 | 46.7 / 66.7 | 36.5 / 100 | -22.5 / 101 |
| AFs bull * | 78 / 4 | 69.2 / 75 | 78.2 / 75 | 62.8 / 25 | 56 / 50 | 28.8 / -32.8 |
| AFs bear * | 83 / 8 | 74.7 / 62.5 | 78.3 / 62.5 | 49.4 / 12.5 | 48.7 / 12.5 | -8 / -51.5 |
| CI bull * | 12 / 1 | 83.3 / 100 | 91.7 / 100 | 75 / 100 | 45.5 / 100 | -5.5 / 177 |
| CI bear * | 10 / 0 | 60 / - | 70 / - | 50 / - | 50 / - | -4.6 / - |
| S&D bull * | 38 / 3 | 68.4 / 0 | 68.4 / 0 | 63.2 / 66.7 | 51.4 / 33.3 | 3 / -8.2 |
| S&D bear * | 43 / 0 | 62.8 / - | 65.1 / - | 39.5 / - | 39.5 / - | -27.2 / - |

**Next candle family (what type the 10:00 candle turns into next):**

| this type | n | next = BC+ % | next = BC- % | next = C2 % | next = AFs % | next = CI % | next = S&D % |
|---|---|---|---|---|---|---|---|
| BuC2+ * | 63 / 7 | 47.6 / 14.3 | 6.3 / 42.9 | 6.3 / 0 | 28.6 / 28.6 | 3.2 / 0 | 7.9 / 14.3 |
| BuC2- * | 10 / 0 | 30 / - | 10 / - | 0 / - | 50 / - | 10 / - | 0 / - |
| BeC2+ * | 57 / 3 | 19.3 / 33.3 | 17.5 / 33.3 | 0 / 0 | 50.9 / 33.3 | 8.8 / 0 | 3.5 / 0 |
| BeC2- * | 18 / 0 | 22.2 / - | 11.1 / - | 0 / - | 27.8 / - | 22.2 / - | 16.7 / - |
| BuBC+ * | 126 / 9 | 33.3 / 33.3 | 14.3 / 0 | 11.9 / 0 | 26.2 / 33.3 | 2.4 / 22.2 | 11.9 / 11.1 |
| BuBC- * | 75 / 9 | 33.3 / 55.6 | 13.3 / 0 | 8 / 11.1 | 30.7 / 22.2 | 9.3 / 0 | 5.3 / 11.1 |
| BeBC+ * | 83 / 12 | 21.7 / 50 | 18.1 / 8.3 | 8.4 / 0 | 36.1 / 33.3 | 6 / 8.3 | 9.6 / 0 |
| BeBC- * | 66 / 5 | 36.4 / 0 | 12.1 / 0 | 9.1 / 20 | 25.8 / 60 | 13.6 / 20 | 3 / 0 |
| S&D.BuAF * | 38 / 3 | 34.2 / 0 | 18.4 / 33.3 | 13.2 / 0 | 21.1 / 33.3 | 7.9 / 33.3 | 5.3 / 0 |
| S&D.BeAF * | 43 / 0 | 25.6 / - | 16.3 / - | 9.3 / - | 27.9 / - | 11.6 / - | 9.3 / - |
| BuAFs+ * | 64 / 4 | 37.5 / 0 | 21.9 / 0 | 15.6 / 50 | 14.1 / 25 | 1.6 / 25 | 9.4 / 0 |
| BuAFs- * | 23 / 1 | 43.5 / 100 | 13 / 0 | 8.7 / 0 | 26.1 / 0 | 0 / 0 | 8.7 / 0 |
| BeAFs+ * | 60 / 7 | 31.7 / 14.3 | 20 / 28.6 | 18.3 / 14.3 | 26.7 / 42.9 | 1.7 / 0 | 1.7 / 0 |
| BeAFs- * | 14 / 0 | 14.3 / - | 21.4 / - | 7.1 / - | 50 / - | 0 / - | 7.1 / - |
| CI.BuAF * | 12 / 1 | 41.7 / 0 | 25 / 100 | 8.3 / 0 | 25 / 0 | 0 / 0 | 0 / 0 |
| CI.BeAF * | 10 / 0 | 20 / - | 30 / - | 20 / - | 10 / - | 0 / - | 20 / - |
| bull | 402 / 33 | 35.8 / 27.3 | 14.9 / 15.2 | 10.4 / 9.1 | 26.4 / 27.3 | 4.2 / 12.1 | 8.2 / 9.1 |
| bear * | 360 / 28 | 27.5 / 32.1 | 16.7 / 14.3 | 8.9 / 7.1 | 32.2 / 39.3 | 8.1 / 7.1 | 6.7 / 0 |

### 1.2 1h 09:00-10:00

**By type (share + who gets taken first + 16:00 close):**

| type | n | share % | took HI first % | took LO first % | took neither % | took lean side at all % | next candle same lean % | 16:00 UP % | 16:00 median pts (10:00 close to 16:00 close) |
|---|---|---|---|---|---|---|---|---|---|
| BuC2+ * | 70 / 6 | 9.2 / 9.8 | 82.9 / 100 | 10 / 0 | 7.1 / 0 | 82.9 / 100 | 55.7 / 50 | 54.4 / 16.7 | 14.6 / -59.9 |
| BuC2- * | 19 / 1 | 2.5 / 1.6 | 63.2 / 100 | 26.3 / 0 | 10.5 / 0 | 63.2 / 100 | 47.4 / 100 | 66.7 / 100 | 53.6 / 279 |
| BeC2+ * | 66 / 4 | 8.7 / 6.6 | 1.5 / 0 | 83.3 / 100 | 15.2 / 0 | 83.3 / 100 | 62.1 / 75 | 50 / 25 | 2.9 / -122 |
| BeC2- * | 23 / 2 | 3 / 3.3 | 17.4 / 0 | 43.5 / 0 | 39.1 / 100 | 43.5 / 0 | 56.5 / 0 | 72.7 / 100 | 35.1 / 85.2 |
| BuBC+ * | 118 / 11 | 15.5 / 18 | 90.7 / 90.9 | 5.9 / 0 | 3.4 / 9.1 | 93.2 / 90.9 | 61.9 / 54.5 | 67.3 / 45.5 | 43 / -34.5 |
| BuBC- * | 57 / 4 | 7.5 / 6.6 | 50.9 / 50 | 42.1 / 50 | 7 / 0 | 56.1 / 50 | 50.9 / 25 | 57.7 / 50 | 29.2 / 72.2 |
| BeBC+ * | 81 / 9 | 10.6 / 14.8 | 8.6 / 0 | 86.4 / 100 | 4.9 / 0 | 86.4 / 100 | 54.3 / 44.4 | 50.6 / 33.3 | 0.5 / -64.5 |
| BeBC- * | 53 / 4 | 6.9 / 6.6 | 32.1 / 75 | 47.2 / 25 | 20.8 / 0 | 49.1 / 25 | 50.9 / 50 | 63.5 / 100 | 22.5 / 133 |
| S&D.BuAF * | 47 / 1 | 6.2 / 1.6 | 59.6 / 0 | 38.3 / 100 | 2.1 / 0 | 61.7 / 0 | 40.4 / 0 | 43.5 / 0 | -31.5 / -330 |
| S&D.BeAF * | 50 / 4 | 6.6 / 6.6 | 22 / 50 | 64 / 50 | 14 / 0 | 66 / 50 | 54 / 50 | 52.1 / 50 | 14.9 / 65.6 |
| BuAFs+ * | 64 / 10 | 8.4 / 16.4 | 85.9 / 70 | 14.1 / 20 | 0 / 10 | 85.9 / 70 | 64.1 / 80 | 59.7 / 60 | 37.9 / 57.8 |
| BuAFs- * | 16 / 0 | 2.1 / 0 | 31.2 / - | 56.2 / - | 12.5 / - | 56.2 / - | 50 / - | 40 / - | -7 / - |
| BeAFs+ * | 54 / 3 | 7.1 / 4.9 | 25.9 / 33.3 | 72.2 / 66.7 | 1.9 / 0 | 75.9 / 66.7 | 42.6 / 0 | 58.8 / 33.3 | 46.8 / -35 |
| BeAFs- * | 20 / 2 | 2.6 / 3.3 | 65 / 100 | 30 / 0 | 5 / 0 | 65 / 100 | 50 / 100 | 65 / 50 | 38 / -52.6 |
| CI.BuAF * | 10 / 0 | 1.3 / 0 | 90 / - | 10 / - | 0 / - | 100 / - | 70 / - | 60 / - | 10.4 / - |
| CI.BeAF * | 15 / 0 | 2 / 0 | 40 / - | 60 / - | 0 / - | 60 / - | 53.3 / - | 64.3 / - | 37.2 / - |
| bull | 405 / 35 | 53.1 / 57.4 | 76.8 / 80 | 19 / 14.3 | 4.2 / 5.7 | 78.8 / 80 | 56 / 60 | 59.4 / 45.7 | 26.8 / -8.2 |
| bear * | 358 / 26 | 46.9 / 42.6 | 18.2 / 23.1 | 69.6 / 69.2 | 12.3 / 7.7 | 70.7 / 69.2 | 53.4 / 42.3 | 55.4 / 50 | 16 / 0.6 |
| ALL | 763 / 61 | 100 / 100 | 49.3 / 55.7 | 42.7 / 37.7 | 8 / 6.6 | 75 / 75.4 | 54.8 / 52.5 | 57.5 / 47.5 | 19.8 / -3.5 |

**By family and lean side (16:00 measured in the lean direction: + = moved the lean way):**

| family | n | took lean side FIRST % | took lean side at all % | next candle same lean % | 16:00 closed lean way % | 16:00 median pts lean way |
|---|---|---|---|---|---|---|
| BC+ bull * | 118 / 11 | 90.7 / 90.9 | 93.2 / 90.9 | 61.9 / 54.5 | 67.3 / 45.5 | 43 / -34.5 |
| BC+ bear * | 81 / 9 | 86.4 / 100 | 86.4 / 100 | 54.3 / 44.4 | 49.4 / 66.7 | -0.5 / 64.5 |
| BC- bull * | 57 / 4 | 50.9 / 50 | 56.1 / 50 | 50.9 / 25 | 57.7 / 50 | 29.2 / 72.2 |
| BC- bear * | 53 / 4 | 47.2 / 25 | 49.1 / 25 | 50.9 / 50 | 36.5 / 0 | -22.5 / -133 |
| C2 bull * | 89 / 7 | 78.7 / 100 | 78.7 / 100 | 53.9 / 57.1 | 57 / 28.6 | 25.1 / -54.8 |
| C2 bear * | 89 / 6 | 73 / 66.7 | 73 / 66.7 | 60.7 / 50 | 44.2 / 50 | -13.4 / 34.8 |
| AFs bull * | 84 / 12 | 81 / 75 | 81 / 75 | 60.7 / 83.3 | 61 / 58.3 | 38 / 57.8 |
| AFs bear * | 70 / 3 | 68.6 / 66.7 | 71.4 / 66.7 | 44.3 / 0 | 45.5 / 66.7 | -21 / 35 |
| CI bull * | 10 / 0 | 90 / - | 100 / - | 70 / - | 60 / - | 10.4 / - |
| CI bear * | 15 / 0 | 60 / - | 60 / - | 53.3 / - | 35.7 / - | -37.2 / - |
| S&D bull * | 47 / 1 | 59.6 / 0 | 61.7 / 0 | 40.4 / 0 | 43.5 / 0 | -31.5 / -330 |
| S&D bear * | 50 / 4 | 64 / 50 | 66 / 50 | 54 / 50 | 47.9 / 50 | -14.9 / -65.6 |

**Next candle family (what type the 10:00 candle turns into next):**

| this type | n | next = BC+ % | next = BC- % | next = C2 % | next = AFs % | next = CI % | next = S&D % |
|---|---|---|---|---|---|---|---|
| BuC2+ * | 70 / 6 | 32.9 / 16.7 | 20 / 0 | 2.9 / 0 | 34.3 / 33.3 | 7.1 / 0 | 2.9 / 50 |
| BuC2- * | 19 / 1 | 26.3 / 100 | 10.5 / 0 | 0 / 0 | 52.6 / 0 | 10.5 / 0 | 0 / 0 |
| BeC2+ * | 66 / 4 | 21.2 / 25 | 21.2 / 50 | 4.5 / 0 | 34.8 / 25 | 15.2 / 0 | 3 / 0 |
| BeC2- * | 23 / 2 | 13 / 0 | 21.7 / 0 | 4.3 / 0 | 21.7 / 0 | 39.1 / 100 | 0 / 0 |
| BuBC+ * | 118 / 11 | 31.4 / 36.4 | 17.8 / 9.1 | 8.5 / 0 | 28.8 / 45.5 | 3.4 / 9.1 | 10.2 / 0 |
| BuBC- * | 57 / 4 | 35.1 / 50 | 14 / 0 | 7 / 0 | 31.6 / 50 | 7 / 0 | 5.3 / 0 |
| BeBC+ * | 81 / 9 | 39.5 / 0 | 11.1 / 33.3 | 1.2 / 0 | 43.2 / 66.7 | 4.9 / 0 | 0 / 0 |
| BeBC- * | 53 / 4 | 32.1 / 50 | 13.2 / 25 | 0 / 0 | 30.2 / 25 | 20.8 / 0 | 3.8 / 0 |
| S&D.BuAF * | 47 / 1 | 46.8 / 100 | 8.5 / 0 | 4.3 / 0 | 34 / 0 | 2.1 / 0 | 4.3 / 0 |
| S&D.BeAF * | 50 / 4 | 28 / 50 | 18 / 0 | 4 / 0 | 30 / 50 | 14 / 0 | 6 / 0 |
| BuAFs+ * | 64 / 10 | 53.1 / 40 | 15.6 / 0 | 3.1 / 0 | 21.9 / 50 | 0 / 10 | 6.2 / 0 |
| BuAFs- * | 16 / 0 | 37.5 / - | 12.5 / - | 12.5 / - | 18.8 / - | 12.5 / - | 6.2 / - |
| BeAFs+ * | 54 / 3 | 33.3 / 0 | 14.8 / 0 | 9.3 / 33.3 | 31.5 / 33.3 | 1.9 / 0 | 9.3 / 33.3 |
| BeAFs- * | 20 / 2 | 10 / 50 | 15 / 0 | 10 / 0 | 50 / 50 | 5 / 0 | 10 / 0 |
| CI.BuAF * | 10 / 0 | 30 / - | 20 / - | 20 / - | 20 / - | 0 / - | 10 / - |
| CI.BeAF * | 15 / 0 | 46.7 / - | 26.7 / - | 6.7 / - | 20 / - | 0 / - | 0 / - |
| bull | 405 / 35 | 36 / 40 | 15.8 / 2.9 | 5.9 / 0 | 31.6 / 42.9 | 4.2 / 5.7 | 6.4 / 8.6 |
| bear * | 358 / 26 | 31 / 19.2 | 16.2 / 23.1 | 4.2 / 3.8 | 32.7 / 42.3 | 12.3 / 7.7 | 3.6 / 3.8 |

### 1.3 15m 09:45-10:00

**By type (share + who gets taken first + 16:00 close):**

| type | n | share % | took HI first % | took LO first % | took neither % | took lean side at all % | next candle same lean % | 16:00 UP % | 16:00 median pts (10:00 close to 16:00 close) |
|---|---|---|---|---|---|---|---|---|---|
| BuC2+ * | 8 / 1 | 1 / 1.6 | 100 / 100 | 0 / 0 | 0 / 0 | 100 / 100 | 75 / 0 | 37.5 / 100 | -14.8 / 230 |
| BeC2+ * | 9 / 1 | 1.2 / 1.6 | 0 / 0 | 77.8 / 100 | 22.2 / 0 | 77.8 / 100 | 55.6 / 100 | 66.7 / 0 | 34.2 / -289 |
| BuBC+ * | 119 / 17 | 15.6 / 27.9 | 92.4 / 94.1 | 3.4 / 0 | 3.4 / 5.9 | 94.1 / 94.1 | 56.3 / 70.6 | 60.9 / 41.2 | 29 / -34.5 |
| BuBC- * | 59 / 3 | 7.7 / 4.9 | 57.6 / 33.3 | 23.7 / 66.7 | 15.3 / 0 | 67.8 / 33.3 | 62.7 / 33.3 | 56.1 / 33.3 | 27.2 / -8.2 |
| BeBC+ * | 91 / 9 | 11.9 / 14.8 | 2.2 / 0 | 89 / 77.8 | 8.8 / 22.2 | 89 / 77.8 | 53.8 / 33.3 | 52.2 / 22.2 | 9.2 / -101 |
| BeBC- * | 57 / 3 | 7.5 / 4.9 | 36.8 / 66.7 | 42.1 / 33.3 | 21.1 / 0 | 47.4 / 33.3 | 47.4 / 0 | 49.1 / 66.7 | -1 / 163 |
| S&D.BuAF * | 4 / 0 | 0.5 / 0 | 75 / - | 0 / - | 25 / - | 75 / - | 50 / - | 75 / - | 37.2 / - |
| S&D.BeAF * | 9 / 1 | 1.2 / 1.6 | 11.1 / 100 | 77.8 / 0 | 11.1 / 0 | 77.8 / 0 | 66.7 / 0 | 44.4 / 100 | -77.2 / 454 |
| BuAFs+ * | 99 / 10 | 13 / 16.4 | 71.7 / 60 | 15.2 / 10 | 13.1 / 30 | 73.7 / 60 | 64.6 / 50 | 66.7 / 70 | 46 / 59 |
| BuAFs- * | 52 / 3 | 6.8 / 4.9 | 28.8 / 0 | 57.7 / 100 | 13.5 / 0 | 59.6 / 100 | 55.8 / 100 | 60 / 100 | 16.8 / 27 |
| BeAFs+ * | 89 / 4 | 11.7 / 6.6 | 21.3 / 0 | 69.7 / 100 | 7.9 / 0 | 70.8 / 100 | 57.3 / 50 | 53.5 / 50 | 9.6 / 45.9 |
| BeAFs- * | 43 / 4 | 5.6 / 6.6 | 62.8 / 25 | 20.9 / 25 | 14 / 50 | 69.8 / 25 | 60.5 / 50 | 61.9 / 25 | 21.6 / -28.2 |
| CI.BuAF * | 70 / 3 | 9.2 / 4.9 | 75.7 / 100 | 18.6 / 0 | 4.3 / 0 | 81.4 / 100 | 68.6 / 66.7 | 64.2 / 66.7 | 34.8 / 7.8 |
| CI.BeAF * | 54 / 2 | 7.1 / 3.3 | 16.7 / 0 | 72.2 / 100 | 9.3 / 0 | 83.3 / 100 | 59.3 / 50 | 45.7 / 0 | -11.2 / -49.8 |
| bull | 402 / 38 | 52.7 / 62.3 | 76.1 / 73.7 | 13.7 / 10.5 | 9 / 15.8 | 80.3 / 73.7 | 62.2 / 57.9 | 62 / 50 | 33 / -0.4 |
| bear * | 361 / 23 | 47.3 / 37.7 | 18.6 / 13 | 69.3 / 78.3 | 11.6 / 8.7 | 72.3 / 78.3 | 55.1 / 43.5 | 52.5 / 43.5 | 6.8 / -35 |
| ALL | 763 / 61 | 100 / 100 | 48.9 / 50.8 | 40 / 36.1 | 10.2 / 13.1 | 76.5 / 75.4 | 58.8 / 52.5 | 57.5 / 47.5 | 19.8 / -3.5 |

**By family and lean side (16:00 measured in the lean direction: + = moved the lean way):**

| family | n | took lean side FIRST % | took lean side at all % | next candle same lean % | 16:00 closed lean way % | 16:00 median pts lean way |
|---|---|---|---|---|---|---|
| BC+ bull * | 119 / 17 | 92.4 / 94.1 | 94.1 / 94.1 | 56.3 / 70.6 | 60.9 / 41.2 | 29 / -34.5 |
| BC+ bear * | 91 / 9 | 89 / 77.8 | 89 / 77.8 | 53.8 / 33.3 | 47.8 / 77.8 | -9.2 / 101 |
| BC- bull * | 59 / 3 | 57.6 / 33.3 | 67.8 / 33.3 | 62.7 / 33.3 | 56.1 / 33.3 | 27.2 / -8.2 |
| BC- bear * | 57 / 3 | 42.1 / 33.3 | 47.4 / 33.3 | 47.4 / 0 | 50.9 / 33.3 | 1 / -163 |
| C2 bull * | 8 / 1 | 100 / 100 | 100 / 100 | 75 / 0 | 37.5 / 100 | -14.8 / 230 |
| C2 bear * | 9 / 1 | 77.8 / 100 | 77.8 / 100 | 55.6 / 100 | 33.3 / 100 | -34.2 / 289 |
| AFs bull * | 142 / 14 | 69 / 50 | 72.5 / 50 | 63.4 / 50 | 65.2 / 57.1 | 39.4 / 22.9 |
| AFs bear * | 141 / 7 | 65.2 / 100 | 66.7 / 100 | 56.7 / 71.4 | 44.1 / 28.6 | -13.1 / -27 |
| CI bull * | 70 / 3 | 75.7 / 100 | 81.4 / 100 | 68.6 / 66.7 | 64.2 / 66.7 | 34.8 / 7.8 |
| CI bear * | 54 / 2 | 72.2 / 100 | 83.3 / 100 | 59.3 / 50 | 54.3 / 100 | 11.2 / 49.8 |
| S&D bull * | 4 / 0 | 75 / - | 75 / - | 50 / - | 75 / - | 37.2 / - |
| S&D bear * | 9 / 1 | 77.8 / 0 | 77.8 / 0 | 66.7 / 0 | 55.6 / 0 | 77.2 / -454 |

**Next candle family (what type the 10:00 candle turns into next):**

| this type | n | next = BC+ % | next = BC- % | next = C2 % | next = AFs % | next = CI % | next = S&D % |
|---|---|---|---|---|---|---|---|
| BuC2+ * | 8 / 1 | 37.5 / 0 | 37.5 / 0 | 0 / 0 | 25 / 100 | 0 / 0 | 0 / 0 |
| BeC2+ * | 9 / 1 | 11.1 / 0 | 22.2 / 0 | 0 / 0 | 44.4 / 100 | 22.2 / 0 | 0 / 0 |
| BuBC+ * | 119 / 17 | 28.6 / 17.6 | 20.2 / 23.5 | 2.5 / 0 | 39.5 / 47.1 | 3.4 / 5.9 | 5.9 / 5.9 |
| BuBC- * | 59 / 3 | 37.3 / 66.7 | 10.2 / 33.3 | 11.9 / 0 | 20.3 / 0 | 15.3 / 0 | 5.1 / 0 |
| BeBC+ * | 91 / 9 | 25.3 / 22.2 | 23.1 / 11.1 | 7.7 / 0 | 35.2 / 44.4 | 8.8 / 22.2 | 0 / 0 |
| BeBC- * | 57 / 3 | 26.3 / 33.3 | 10.5 / 0 | 5.3 / 0 | 35.1 / 66.7 | 21.1 / 0 | 1.8 / 0 |
| S&D.BuAF * | 4 / 0 | 25 / - | 0 / - | 0 / - | 50 / - | 25 / - | 0 / - |
| S&D.BeAF * | 9 / 1 | 44.4 / 0 | 0 / 0 | 0 / 0 | 44.4 / 100 | 11.1 / 0 | 0 / 0 |
| BuAFs+ * | 99 / 10 | 37.4 / 20 | 19.2 / 0 | 4 / 0 | 21.2 / 40 | 13.1 / 30 | 5.1 / 10 |
| BuAFs- * | 52 / 3 | 34.6 / 0 | 9.6 / 66.7 | 5.8 / 0 | 36.5 / 33.3 | 13.5 / 0 | 0 / 0 |
| BeAFs+ * | 89 / 4 | 33.7 / 25 | 14.6 / 25 | 5.6 / 25 | 33.7 / 25 | 7.9 / 0 | 4.5 / 0 |
| BeAFs- * | 43 / 4 | 20.9 / 50 | 7 / 0 | 4.7 / 0 | 41.9 / 0 | 14 / 50 | 11.6 / 0 |
| CI.BuAF * | 70 / 3 | 30 / 33.3 | 25.7 / 0 | 10 / 0 | 25.7 / 66.7 | 4.3 / 0 | 4.3 / 0 |
| CI.BeAF * | 54 / 2 | 24.1 / 50 | 14.8 / 0 | 13 / 0 | 31.5 / 50 | 9.3 / 0 | 7.4 / 0 |
| bull | 402 / 38 | 31.6 / 26.3 | 18.2 / 13.2 | 5.7 / 0 | 29.9 / 39.5 | 9 / 15.8 | 5.7 / 5.3 |
| bear * | 361 / 23 | 28.8 / 21.7 | 15.2 / 17.4 | 6.9 / 4.3 | 34.9 / 47.8 | 11.6 / 8.7 | 2.5 / 0 |

### 1.4 5m 09:55-10:00

**By type (share + who gets taken first + 16:00 close):**

| type | n | share % | took HI first % | took LO first % | took neither % | took lean side at all % | next candle same lean % | 16:00 UP % | 16:00 median pts (10:00 close to 16:00 close) |
|---|---|---|---|---|---|---|---|---|---|
| BuC2+ * | 12 / 1 | 1.6 / 1.6 | 91.7 / 0 | 0 / 0 | 0 / 100 | 100 / 0 | 75 / 0 | 75 / 0 | 71.1 / -65 |
| BeC2+ * | 14 / 1 | 1.8 / 1.6 | 14.3 / 0 | 78.6 / 100 | 7.1 / 0 | 78.6 / 100 | 42.9 / 100 | 71.4 / 100 | 26.5 / 250 |
| BeC2- * | 2 / 0 | 0.3 / 0 | 0 / - | 50 / - | 50 / - | 50 / - | 50 / - | 0 / - | -124 / - |
| BuBC+ * | 116 / 15 | 15.2 / 24.6 | 88.8 / 93.3 | 6 / 6.7 | 5.2 / 0 | 90.5 / 93.3 | 59.5 / 53.3 | 57.5 / 53.3 | 27.2 / 2.8 |
| BuBC- * | 57 / 2 | 7.5 / 3.3 | 61.4 / 0 | 26.3 / 50 | 10.5 / 50 | 70.2 / 0 | 59.6 / 0 | 65.5 / 50 | 32 / 3.6 |
| BeBC+ * | 83 / 7 | 10.9 / 11.5 | 4.8 / 0 | 85.5 / 71.4 | 7.2 / 28.6 | 89.2 / 71.4 | 55.4 / 42.9 | 55.6 / 14.3 | 28 / -170 |
| BeBC- * | 48 / 2 | 6.3 / 3.3 | 31.2 / 50 | 54.2 / 50 | 12.5 / 0 | 58.3 / 50 | 52.1 / 0 | 50 / 50 | 1.1 / -39.8 |
| S&D.BuAF * | 14 / 2 | 1.8 / 3.3 | 57.1 / 50 | 14.3 / 50 | 21.4 / 0 | 64.3 / 50 | 64.3 / 50 | 58.3 / 50 | 72.4 / 151 |
| S&D.BeAF * | 12 / 0 | 1.6 / 0 | 25 / - | 58.3 / - | 16.7 / - | 66.7 / - | 41.7 / - | 58.3 / - | 39.2 / - |
| BuAFs+ * | 96 / 15 | 12.6 / 24.6 | 66.7 / 73.3 | 26 / 6.7 | 4.2 / 20 | 71.9 / 73.3 | 46.9 / 60 | 48.4 / 53.3 | -0.2 / 75 |
| BuAFs- * | 47 / 5 | 6.2 / 8.2 | 17 / 40 | 61.7 / 40 | 10.6 / 20 | 76.6 / 60 | 53.2 / 40 | 54.5 / 40 | 14.4 / -1.5 |
| BeAFs+ * | 104 / 5 | 13.6 / 8.2 | 26 / 20 | 63.5 / 80 | 5.8 / 0 | 74 / 80 | 51.9 / 100 | 64 / 60 | 30.8 / 7.8 |
| BeAFs- * | 43 / 1 | 5.6 / 1.6 | 65.1 / 0 | 27.9 / 100 | 4.7 / 0 | 72.1 / 0 | 72.1 / 0 | 62.5 / 0 | 37.6 / -85 |
| CI.BuAF * | 64 / 4 | 8.4 / 6.6 | 73.4 / 100 | 20.3 / 0 | 6.2 / 0 | 79.7 / 100 | 60.9 / 75 | 66.1 / 75 | 27.9 / 77 |
| CI.BeAF * | 51 / 1 | 6.7 / 1.6 | 27.5 / 0 | 64.7 / 100 | 2 / 0 | 74.5 / 100 | 49 / 100 | 43.8 / 0 | -12.4 / -35 |
| bull | 402 / 40 | 52.7 / 65.6 | 73.6 / 75 | 18.4 / 12.5 | 6.2 / 12.5 | 78.9 / 75 | 58.7 / 52.5 | 58.9 / 52.5 | 26.8 / 22.9 |
| bear * | 361 / 21 | 47.3 / 34.4 | 20.2 / 19 | 67.6 / 66.7 | 7.8 / 14.3 | 75.6 / 71.4 | 51.8 / 57.1 | 55.9 / 38.1 | 13.5 / -35 |
| ALL | 763 / 61 | 100 / 100 | 48.4 / 55.7 | 41.7 / 31.1 | 6.9 / 13.1 | 77.3 / 73.8 | 55.4 / 54.1 | 57.5 / 47.5 | 19.8 / -3.5 |

**By family and lean side (16:00 measured in the lean direction: + = moved the lean way):**

| family | n | took lean side FIRST % | took lean side at all % | next candle same lean % | 16:00 closed lean way % | 16:00 median pts lean way |
|---|---|---|---|---|---|---|
| BC+ bull * | 116 / 15 | 88.8 / 93.3 | 90.5 / 93.3 | 59.5 / 53.3 | 57.5 / 53.3 | 27.2 / 2.8 |
| BC+ bear * | 83 / 7 | 85.5 / 71.4 | 89.2 / 71.4 | 55.4 / 42.9 | 44.4 / 85.7 | -28 / 170 |
| BC- bull * | 57 / 2 | 61.4 / 0 | 70.2 / 0 | 59.6 / 0 | 65.5 / 50 | 32 / 3.6 |
| BC- bear * | 48 / 2 | 54.2 / 50 | 58.3 / 50 | 52.1 / 0 | 50 / 50 | -1.1 / 39.8 |
| C2 bull * | 12 / 1 | 91.7 / 0 | 100 / 0 | 75 / 0 | 75 / 0 | 71.1 / -65 |
| C2 bear * | 16 / 1 | 75 / 100 | 75 / 100 | 43.8 / 100 | 37.5 / 0 | -15.9 / -250 |
| AFs bull * | 139 / 16 | 66.2 / 68.8 | 71.9 / 68.8 | 54.7 / 56.2 | 52.6 / 50 | 7.2 / 25.6 |
| AFs bear * | 151 / 10 | 62.9 / 60 | 74.8 / 70 | 52.3 / 70 | 38.9 / 50 | -25.8 / -1.1 |
| CI bull * | 64 / 4 | 73.4 / 100 | 79.7 / 100 | 60.9 / 75 | 66.1 / 75 | 27.9 / 77 |
| CI bear * | 51 / 1 | 64.7 / 100 | 74.5 / 100 | 49 / 100 | 56.2 / 100 | 12.4 / 35 |
| S&D bull * | 14 / 2 | 57.1 / 50 | 64.3 / 50 | 64.3 / 50 | 58.3 / 50 | 72.4 / 151 |
| S&D bear * | 12 / 0 | 58.3 / - | 66.7 / - | 41.7 / - | 41.7 / - | -39.2 / - |

**Next candle family (what type the 10:00 candle turns into next):**

| this type | n | next = BC+ % | next = BC- % | next = C2 % | next = AFs % | next = CI % | next = S&D % |
|---|---|---|---|---|---|---|---|
| BuC2+ * | 12 / 1 | 41.7 / 0 | 16.7 / 0 | 8.3 / 0 | 33.3 / 0 | 0 / 100 | 0 / 0 |
| BeC2+ * | 14 / 1 | 28.6 / 100 | 21.4 / 0 | 0 / 0 | 42.9 / 0 | 7.1 / 0 | 0 / 0 |
| BeC2- * | 2 / 0 | 0 / - | 0 / - | 0 / - | 50 / - | 50 / - | 0 / - |
| BuBC+ * | 116 / 15 | 37.9 / 6.7 | 12.9 / 40 | 5.2 / 6.7 | 34.5 / 46.7 | 5.2 / 0 | 4.3 / 0 |
| BuBC- * | 57 / 2 | 15.8 / 0 | 21.1 / 50 | 5.3 / 0 | 35.1 / 0 | 10.5 / 50 | 12.3 / 0 |
| BeBC+ * | 83 / 7 | 26.5 / 14.3 | 22.9 / 14.3 | 4.8 / 0 | 34.9 / 42.9 | 7.2 / 28.6 | 3.6 / 0 |
| BeBC- * | 48 / 2 | 33.3 / 0 | 16.7 / 50 | 10.4 / 0 | 25 / 50 | 12.5 / 0 | 2.1 / 0 |
| S&D.BuAF * | 14 / 2 | 28.6 / 50 | 0 / 0 | 0 / 0 | 42.9 / 50 | 21.4 / 0 | 7.1 / 0 |
| S&D.BeAF * | 12 / 0 | 25 / - | 16.7 / - | 25 / - | 16.7 / - | 16.7 / - | 0 / - |
| BuAFs+ * | 96 / 15 | 27.1 / 46.7 | 12.5 / 6.7 | 9.4 / 0 | 40.6 / 26.7 | 4.2 / 20 | 6.2 / 0 |
| BuAFs- * | 47 / 5 | 23.4 / 0 | 6.4 / 0 | 19.1 / 20 | 29.8 / 40 | 10.6 / 20 | 10.6 / 20 |
| BeAFs+ * | 104 / 5 | 24 / 60 | 16.3 / 20 | 12.5 / 0 | 34.6 / 20 | 5.8 / 0 | 6.7 / 0 |
| BeAFs- * | 43 / 1 | 25.6 / 100 | 23.3 / 0 | 11.6 / 0 | 25.6 / 0 | 4.7 / 0 | 9.3 / 0 |
| CI.BuAF * | 64 / 4 | 21.9 / 50 | 25 / 25 | 7.8 / 0 | 31.2 / 25 | 6.2 / 0 | 7.8 / 0 |
| CI.BeAF * | 51 / 1 | 35.3 / 100 | 13.7 / 0 | 13.7 / 0 | 27.5 / 0 | 2 / 0 | 7.8 / 0 |
| bull | 402 / 40 | 28.1 / 30 | 16.7 / 22.5 | 7.2 / 2.5 | 34.8 / 32.5 | 6.2 / 12.5 | 7 / 0 |
| bear * | 361 / 21 | 27.4 / 28.6 | 16.3 / 14.3 | 11.4 / 4.8 | 31.6 / 33.3 | 7.8 / 14.3 | 5.5 / 4.8 |

### 1.5 4H 06-10 candle -> what the 10:00-14:00 4H candle does

| 06-10 type | n | took 06-10 HI first % | took 06-10 LO first % | took neither % | took lean side at all % | 10-14 closes ABOVE 06-10 high % | 10-14 closes BELOW 06-10 low % | closes inside % |
|---|---|---|---|---|---|---|---|---|
| ALL | 762 / 61 | 49.7 / 52.5 | 44.2 / 37.7 | 6 / 9.8 | 76.4 / 73.8 | 32.5 / 27.9 | 24.8 / 24.6 | 42.7 / 47.5 |
| bull lean | 402 / 33 | 75.4 / 75.8 | 20.4 / 12.1 | 4.2 / 12.1 | 79.1 / 75.8 | 44.8 / 36.4 | 16.4 / 15.2 | 38.8 / 48.5 |
| bear lean * | 360 / 28 | 21.1 / 25 | 70.8 / 67.9 | 8.1 / 7.1 | 73.3 / 71.4 | 18.9 / 17.9 | 34.2 / 35.7 | 46.9 / 46.4 |
| BuC2+ * | 63 / 7 | 92.1 / 100 | 4.8 / 0 | 3.2 / 0 | 92.1 / 100 | 54 / 57.1 | 6.3 / 0 | 39.7 / 42.9 |
| BuC2- * | 10 / 0 | 40 / - | 50 / - | 10 / - | 40 / - | 20 / - | 20 / - | 60 / - |
| BeC2+ * | 57 / 3 | 5.3 / 0 | 86 / 100 | 8.8 / 0 | 86 / 100 | 0 / 0 | 36.8 / 66.7 | 63.2 / 33.3 |
| BeC2- * | 18 / 0 | 27.8 / - | 50 / - | 22.2 / - | 50 / - | 16.7 / - | 16.7 / - | 66.7 / - |
| BuBC+ * | 126 / 9 | 90.5 / 77.8 | 7.1 / 0 | 2.4 / 22.2 | 91.3 / 77.8 | 46 / 33.3 | 13.5 / 0 | 40.5 / 66.7 |
| BuBC- * | 75 / 9 | 49.3 / 77.8 | 41.3 / 22.2 | 9.3 / 0 | 57.3 / 77.8 | 33.3 / 44.4 | 21.3 / 22.2 | 45.3 / 33.3 |
| BeBC+ * | 83 / 12 | 7.2 / 16.7 | 86.7 / 75 | 6 / 8.3 | 86.7 / 75 | 10.8 / 8.3 | 37.3 / 50 | 51.8 / 41.7 |
| BeBC- * | 66 / 5 | 40.9 / 40 | 45.5 / 40 | 13.6 / 20 | 51.5 / 60 | 30.3 / 0 | 27.3 / 20 | 42.4 / 80 |
| S&D.BuAF * | 38 / 3 | 68.4 / 0 | 23.7 / 66.7 | 7.9 / 33.3 | 68.4 / 0 | 39.5 / 0 | 26.3 / 33.3 | 34.2 / 66.7 |
| S&D.BeAF * | 43 / 0 | 25.6 / - | 62.8 / - | 11.6 / - | 65.1 / - | 27.9 / - | 23.3 / - | 48.8 / - |
| BuAFs+ * | 64 / 4 | 73.4 / 75 | 25 / 0 | 1.6 / 25 | 82.8 / 75 | 53.1 / 0 | 21.9 / 50 | 25 / 50 |
| BuAFs- * | 23 / 1 | 26.1 / 100 | 73.9 / 0 | 0 / 0 | 78.3 / 0 | 21.7 / 100 | 43.5 / 0 | 34.8 / 0 |
| BeAFs+ * | 60 / 7 | 23.3 / 28.6 | 75 / 71.4 | 1.7 / 0 | 78.3 / 71.4 | 26.7 / 42.9 | 43.3 / 14.3 | 30 / 42.9 |
| BeAFs- * | 14 / 0 | 50 / - | 50 / - | 0 / - | 57.1 / - | 28.6 / - | 14.3 / - | 57.1 / - |
| CI.BuAF * | 12 / 1 | 83.3 / 100 | 16.7 / 0 | 0 / 0 | 91.7 / 100 | 66.7 / 100 | 8.3 / 0 | 25 / 0 |
| CI.BeAF * | 10 / 0 | 40 / - | 60 / - | 0 / - | 70 / - | 30 / - | 40 / - | 30 / - |

## 2. UPG gaps made 09:30-10:00 (5m and 1m)

Bull UPG = c2 is a bull BC (close above c1 high) and c3 low is above c1 high. Gap zone = c1 high to c3 low. Bear = mirror. We count gaps whose c3 candle opens 09:30 or later and closes by 10:00 (5m: c3 = 09:30 to 09:55 bar; 1m: 09:30 to 09:59 bar). Gaps can overlap (each 3-candle set counts once). We watch until 16:00.

- **Touch** = price trades back into the zone. **Full fill** = price trades through the far edge (c1 high for a bull gap).
- **React** = after the touch, a 5m candle closes back outside the gap on the gap side BEFORE any 5m close beyond the far edge. **Fail** = a 5m close beyond the far edge comes first.

**Most important:**
- **Gaps almost always get touched, and fast.** 5m gaps: 83% / 73% touched, median 5 / 3.5 minutes after the gap is made. 1m gaps: 92% / 92% touched, median 1 minute. A gap here is like a sponge: price comes back to soak it up.
- **Most of them get fully filled too:** 5m 74% / 67%, 1m 88% / 87%. If a 5m gap is touched, 90% / 91% get fully filled at some point before 16:00. So "react" is often only a bounce, not a final hold.
- **React beats fail: 63% / 68% (5m).** The gap side wins more when the gap points the SAME way as the 4H 06-10 lean: react 68% / 79%. Against the 4H lean: react only 47% / 29%. WARNING: the 4H candle is still open until 10:00, so this filter is only fully known at 10:00 (it peeks a little ahead for gaps made before 10:00).
- **The first 5m close outside the gap tells you a lot:** a FAIL close is nearly always a real body close (5m gaps: BC+ family 68% / 76%, BC family total 87% / 81%). A REACT close is most often an AFs candle (47% / 51%), like BuAFs+ for a bull gap (sweep the low, close back up). So: strong BC through the far edge = the gap is dead. AFs back out of the gap = the gap held. (This rule is for 5m gaps. For tiny 1m gaps the fail candle is often just an AFs, 35% / 38%.)
- **After a FULL fill it is close to a coin flip.** In 60 minutes, 5m gaps: price goes 30 pts the fill way 65% / 82% and 30 pts back the other way 60% / 77% (2026 moves more). Which 30 comes first: about 50/50 (5m 50% / 57% continue first, 1m 46% / 53%). Price gets back past the near edge of the gap within 60 min 82% / 88%. So a filled gap is NOT a clean breakout signal.

### 2.1 Gap counts, touch, fill, react/fail

| gap set | n gaps | gaps per day | median gap size pts | touched % | median min to touch | 75th pct min to touch | touched within 5 min % | touched within 30 min % | full fill % | full fill if touched % | n touched | REACT % (of touched) | FAIL % | neither % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5m bull | 565 / 41 | 0.7 / 0.7 | 10.2 / 15.2 | 81.8 / 70.7 | 5 / 4 | 22 / 14 | 41.4 / 41.5 | 65.3 / 61 | 74.2 / 65.9 | 90.7 / 93.1 | 462 / 29 | 64.9 / 72.4 | 35.1 / 27.6 | 0 / 0 |
| 5m bear | 554 / 49 | 0.7 / 0.8 | 11 / 13 | 83.2 / 75.5 | 6 / 3 | 23 / 11 | 41.5 / 44.9 | 66.2 / 65.3 | 73.6 / 67.3 | 88.5 / 89.2 | 461 / 37 | 61.6 / 64.9 | 37.7 / 35.1 | 0.7 / 0 |
| 5m all | 1119 / 90 | 1.5 / 1.5 | 10.5 / 14.5 | 82.5 / 73.3 | 5 / 3.5 | 23 / 12.8 | 41.5 / 43.3 | 65.8 / 63.3 | 73.9 / 66.7 | 89.6 / 90.9 | 923 / 66 | 63.3 / 68.2 | 36.4 / 31.8 | 0.3 / 0 |
| 1m bull | 2465 / 206 | 3.2 / 3.4 | 4.8 / 8 | 92.6 / 89.8 | 1 / 1 | 5.5 / 5 | 69.5 / 69.9 | 84.9 / 82.5 | 88.1 / 85.9 | 95.1 / 95.7 | 2283 / 185 | 61.4 / 64.9 | 38.6 / 35.1 | 0 / 0 |
| 1m bear | 2302 / 194 | 3 / 3.2 | 5.5 / 8 | 92.4 / 93.8 | 1 / 1 | 5 / 5 | 70.8 / 70.6 | 85.1 / 85.1 | 87.7 / 88.7 | 94.8 / 94.5 | 2128 / 182 | 60.7 / 60.4 | 39.3 / 39.6 | 0 / 0 |
| 1m all | 4767 / 400 | 6.2 / 6.6 | 5 / 8 | 92.5 / 91.8 | 1 / 1 | 5 / 5 | 70.1 / 70.2 | 85 / 83.8 | 87.9 / 87.2 | 95 / 95.1 | 4411 / 367 | 61 / 62.7 | 38.9 / 37.3 | 0 / 0 |

### 2.2 Gap with or against the 4H 06-10 lean

| gap vs 4H lean | n gaps | touched % | full fill % | n touched | REACT % | FAIL % |
|---|---|---|---|---|---|---|
| 5m gap WITH 4H 06-10 lean | 910 / 76 | 79.9 / 68.4 | 70.5 / 60.5 | 727 / 52 | 67.7 / 78.8 | 31.9 / 21.2 |
| 5m gap AGAINST 4H 06-10 lean * | 209 / 14 | 93.8 / 100 | 88.5 / 100 | 196 / 14 | 46.9 / 28.6 | 53.1 / 71.4 |
| 1m gap WITH 4H 06-10 lean | 3147 / 271 | 90.1 / 88.2 | 84.3 / 82.7 | 2834 / 239 | 67.6 / 71.5 | 32.3 / 28.5 |
| 1m gap AGAINST 4H 06-10 lean | 1620 / 129 | 97.3 / 99.2 | 94.8 / 96.9 | 1577 / 128 | 49.1 / 46.1 | 50.9 / 53.9 |

### 2.3 After a FULL fill (next 60 minutes, measured from the far edge)

"Same way" = the way price filled the gap (down for a bull gap). "Reverse" = back the gap way. "Back past gap" = price trades back beyond the near edge of the gap.

| gap set | n fills | went 30 pts same way % | went 60 pts same way % | went 30 pts reverse % | 30 same way FIRST (vs 30 reverse) % | 30 reverse FIRST % | back past gap in 60 min % | back past gap by 16:00 % | median pts same way (MFE) | 75th pct same way | median pts reverse (MAE) | 75th pct reverse |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5m bull * | 419 / 27 | 66.3 / 81.5 | 40.8 / 48.1 | 61.1 / 88.9 | 52.7 / 51.9 | 42.7 / 48.1 | 81.9 / 92.6 | 89.5 / 92.6 | 47.2 / 52.8 | 88.6 / 88.9 | 41.8 / 89.5 | 80.2 / 124 |
| 5m bear | 408 / 33 | 64.2 / 81.8 | 33.6 / 72.7 | 58.1 / 66.7 | 47.3 / 60.6 | 46.8 / 39.4 | 82.6 / 84.8 | 87.7 / 87.9 | 42.1 / 96.2 | 77.4 / 120 | 36.4 / 53.5 | 72.7 / 96.5 |
| 5m all | 827 / 60 | 65.3 / 81.7 | 37.2 / 61.7 | 59.6 / 76.7 | 50.1 / 56.7 | 44.7 / 43.3 | 82.2 / 88.3 | 88.6 / 90 | 44.5 / 78.2 | 81.5 / 116 | 39 / 65.8 | 78 / 110 |
| 1m bull | 2172 / 177 | 64.3 / 78 | 39.4 / 60.5 | 66.9 / 75.7 | 46.1 / 52.5 | 50.5 / 47.5 | 91.2 / 89.3 | 94.9 / 94.9 | 46.5 / 83.8 | 88.2 / 140 | 47.5 / 60.5 | 84.5 / 110 |
| 1m bear | 2018 / 172 | 63.1 / 76.2 | 36.5 / 51.7 | 65.1 / 73.3 | 46.1 / 53.5 | 49 / 46.5 | 89.6 / 91.9 | 94.2 / 95.9 | 43.2 / 65 | 81.4 / 111 | 46.1 / 65 | 87.9 / 139 |
| 1m all | 4190 / 349 | 63.7 / 77.1 | 38 / 56.2 | 66 / 74.5 | 46.1 / 53 | 49.8 / 47 | 90.4 / 90.5 | 94.5 / 95.4 | 44.5 / 74.8 | 84.2 / 126 | 47 / 62 | 85.8 / 124 |

### 2.4 The FIRST 5m candle that closes outside the gap after the touch

Top 5 MMCB types (count, %). "close WITH gap dir" is 100% for react and 0% for fail by definition. "candle lean = close side" = the MMCB lean of that candle points the same way it closed.

| set | n | top 5 types 2022-25 | top 5 types 2026 | families 2022-25 | close WITH 4H 06-10 lean % | candle lean = close side % |
|---|---|---|---|---|---|---|
| 5m react gaps | 584 / 45 | BuAFs+ 17.3%, BeAFs+ 16.6%, BeBC- 8.6%, S&D.BeAF 8.4%, BeAFs- 7.7% | BuAFs+ 20.0%, BeAFs+ 17.8%, BuBC- 11.1%, S&D.BeAF 8.9%, BeBC+ 8.9% | AFs 46.7%, BC- 15.9%, S&D 13.7%, BC+ 11.5%, C2 8.4%, CI 3.8% | 84.2 / 91.1 | 58.4 / 60 |
| 5m fail gaps * | 336 / 21 | BuBC+ 39.3%, BeBC+ 28.6%, BeBC- 11.0%, BuBC- 7.7%, BeC2+ 4.2% | BuBC+ 52.4%, BeBC+ 23.8%, BuBC- 4.8%, BuC2+ 4.8%, BeC2+ 4.8% | BC+ 67.9%, BC- 18.8%, C2 7.7%, AFs 3.0%, CI 2.1%, S&D 0.6% | 31 / 47.6 | 98.8 / 100 |
| 5m all gaps | 920 / 66 | BuBC+ 17.9%, BeBC+ 14.1%, BuAFs+ 11.6%, BeAFs+ 10.7%, BeBC- 9.5% | BuBC+ 16.7%, BuAFs+ 13.6%, BeBC+ 13.6%, BeAFs+ 12.1%, BuBC- 9.1% | BC+ 32.1%, AFs 30.8%, BC- 17.0%, S&D 8.9%, C2 8.2%, CI 3.2% | 64.8 / 77.3 | 73.2 / 72.7 |
| 5m bull react gaps * | 300 / 21 | BuAFs+ 33.0%, BeBC- 15.3%, BuAFs- 9.3%, S&D.BeAF 8.3%, S&D.BuAF 6.7% | BuAFs+ 42.9%, BeBC+ 14.3%, S&D.BuAF 9.5%, S&D.BeAF 9.5%, BuAFs- 9.5% | AFs 44.3%, BC- 17.0%, S&D 15.0%, BC+ 11.7%, C2 8.3%, CI 3.7% | 83.7 / 100 | 58.7 / 61.9 |
| 5m bull fail gaps * | 162 / 8 | BeBC+ 59.3%, BeBC- 22.8%, BeC2+ 8.6%, CI.BeAF 3.7%, BuAFs+ 1.9% | BeBC+ 62.5%, BeC2+ 12.5%, CI.BeAF 12.5%, BuAFs- 12.5% | BC+ 59.3%, BC- 22.8%, C2 9.3%, AFs 3.7%, CI 3.7%, S&D 1.2% | 31.5 / 37.5 | 98.1 / 100 |
| 5m bear react gaps * | 284 / 24 | BeAFs+ 33.8%, BeAFs- 14.1%, BuBC- 13.4%, S&D.BeAF 8.5%, BeC2+ 6.3% | BeAFs+ 33.3%, BuBC- 16.7%, BeAFs- 12.5%, S&D.BeAF 8.3%, BeC2+ 8.3% | AFs 49.3%, BC- 14.8%, S&D 12.3%, BC+ 11.3%, C2 8.5%, CI 3.9% | 84.9 / 83.3 | 58.1 / 58.3 |
| 5m bear fail gaps * | 174 / 13 | BuBC+ 75.9%, BuBC- 14.9%, BuC2+ 6.3%, BuAFs+ 1.7%, CI.BuAF 0.6% | BuBC+ 84.6%, BuBC- 7.7%, BuC2+ 7.7% | BC+ 75.9%, BC- 14.9%, C2 6.3%, AFs 2.3%, CI 0.6% | 30.5 / 53.8 | 99.4 / 100 |
| 1m react gaps | 2692 / 230 | BuBC+ 14.3%, BeBC+ 13.6%, BuAFs+ 10.7%, BeAFs+ 10.4%, BeBC- 9.3% | BuBC+ 17.0%, BuAFs+ 13.0%, BeBC+ 12.2%, BeAFs+ 10.4%, BuBC- 7.4% | AFs 31.6%, BC+ 28.0%, BC- 18.6%, CI 11.2%, C2 6.2%, S&D 4.4% | 71.2 / 74.3 | 75.3 / 73.9 |
| 1m fail gaps | 1718 / 137 | BuBC+ 14.9%, BeBC+ 14.1%, BuAFs+ 13.8%, BeAFs+ 13.7%, BeBC- 7.0% | BuAFs+ 21.9%, BuBC+ 15.3%, BeBC+ 13.1%, BeAFs+ 9.5%, BeBC- 6.6% | AFs 35.2%, BC+ 29.0%, BC- 12.2%, CI 9.6%, C2 8.4%, S&D 5.5% | 46.7 / 50.4 | 93.7 / 92.7 |
| 1m all gaps | 4410 / 367 | BuBC+ 14.6%, BeBC+ 13.8%, BuAFs+ 11.9%, BeAFs+ 11.7%, BeBC- 8.4% | BuBC+ 16.3%, BuAFs+ 16.3%, BeBC+ 12.5%, BeAFs+ 10.1%, BeBC- 7.1% | AFs 33.0%, BC+ 28.4%, BC- 16.1%, CI 10.6%, C2 7.1%, S&D 4.8% | 61.7 / 65.4 | 82.5 / 80.9 |
| 1m bull react gaps | 1401 / 120 | BuBC+ 23.9%, BuBC- 13.4%, BuAFs+ 12.8%, CI.BuAF 9.1%, BeAFs+ 8.7% | BuBC+ 30.0%, BuAFs+ 13.3%, BeAFs- 10.8%, BeAFs+ 10.0%, BuBC- 9.2% | AFs 31.8%, BC+ 27.0%, BC- 20.1%, CI 11.2%, C2 5.6%, S&D 4.3% | 74.2 / 75.8 | 75.2 / 76.7 |
| 1m bull fail gaps | 881 / 65 | BeBC+ 27.6%, BeAFs+ 25.5%, BeBC- 10.9%, BeC2+ 8.9%, CI.BeAF 8.2% | BeBC+ 27.7%, BeAFs+ 16.9%, CI.BeAF 13.8%, BuAFs- 12.3%, BeBC- 10.8% | AFs 35.1%, BC+ 27.6%, BC- 13.4%, C2 9.8%, CI 8.6%, S&D 5.6% | 42.6 / 46.2 | 93.3 / 90.8 |
| 1m bear react gaps | 1291 / 110 | BeBC+ 25.1%, BeAFs+ 12.2%, BeBC- 12.2%, BuAFs- 8.7%, BuAFs+ 8.4% | BeBC+ 24.5%, BuAFs+ 12.7%, BeAFs+ 10.9%, CI.BeAF 10.0%, BeBC- 10.0% | AFs 31.4%, BC+ 29.0%, BC- 17.0%, CI 11.2%, C2 6.8%, S&D 4.5% | 68 / 72.7 | 75.4 / 70.9 |
| 1m bear fail gaps | 837 / 72 | BuBC+ 30.6%, BuAFs+ 26.0%, CI.BuAF 10.2%, BuBC- 8.1%, BeAFs- 7.4% | BuAFs+ 38.9%, BuBC+ 29.2%, CI.BuAF 9.7%, BuBC- 5.6%, BuC2+ 5.6% | AFs 35.2%, BC+ 30.6%, BC- 11.0%, CI 10.6%, C2 7.0%, S&D 5.5% | 51 / 54.2 | 94.1 / 94.4 |

Families for 2026:

- 5m react (n=45): AFs 51.1%, S&D 15.6%, BC- 13.3%, C2 11.1%, BC+ 8.9%
- 5m fail (n=21): BC+ 76.2%, C2 9.5%, BC- 4.8%, CI 4.8%, AFs 4.8%
- 5m all (n=66): AFs 36.4%, BC+ 30.3%, S&D 10.6%, C2 10.6%, BC- 10.6%, CI 1.5%
- 5m bull react (n=21): AFs 52.4%, S&D 19.0%, BC+ 14.3%, BC- 9.5%, C2 4.8%
- 5m bull fail (n=8): BC+ 62.5%, C2 12.5%, CI 12.5%, AFs 12.5%
- 5m bear react (n=24): AFs 50.0%, C2 16.7%, BC- 16.7%, S&D 12.5%, BC+ 4.2%
- 5m bear fail (n=13): BC+ 84.6%, BC- 7.7%, C2 7.7%
- 1m react (n=230): AFs 34.8%, BC+ 29.1%, BC- 14.8%, CI 12.2%, C2 6.1%, S&D 3.0%
- 1m fail (n=137): AFs 38.0%, BC+ 28.5%, CI 12.4%, BC- 11.7%, C2 5.8%, S&D 3.6%
- 1m all (n=367): AFs 36.0%, BC+ 28.9%, BC- 13.6%, CI 12.3%, C2 6.0%, S&D 3.3%
- 1m bull react (n=120): AFs 35.8%, BC+ 30.8%, BC- 14.2%, CI 11.7%, C2 4.2%, S&D 3.3%
- 1m bull fail (n=65): AFs 32.3%, BC+ 27.7%, BC- 15.4%, CI 15.4%, C2 6.2%, S&D 3.1%
- 1m bear react (n=110): AFs 33.6%, BC+ 27.3%, BC- 15.5%, CI 12.7%, C2 8.2%, S&D 2.7%
- 1m bear fail (n=72): AFs 43.1%, BC+ 29.2%, CI 9.7%, BC- 8.3%, C2 5.6%, S&D 4.2%

## 3. Pullback inside the 10:00-14:00 4H candle

(a) "Adverse" = the biggest move AGAINST the 06-10 4H lean, measured from the 10:00 open, anywhere from 10:00 to 13:59. (b) For the 10-14 candle itself: if it closes up, how far it went below its open (and the mirror for down candles).

**Most important:**
- **The 06-10 lean is a coin flip for the 10-14 close:** 51% / 49% close the lean way. The 06-10 candle alone is not a direction signal for 10-14.
- **When the lean IS right, the pullback is small and EARLY:** median 34 / 65 pts against you (about 25% of the 06-10 range), 75th pct 58 / 97 pts. The worst point comes before 10:30 in 61% / 53% of these days. If price is still going against you after 10:30-11:00, the lean is probably wrong (on wrong days the worst point comes late, median 175 minutes after 10:00).
- **Stop size check (your 50 pt NQ stop):** even on days the lean is RIGHT, price goes 50+ pts against the 10:00 open 31% / 57% of the time. A 50 pt stop right at the 10:00 open is too tight for 2026 volatility. Use the % of the 06-10 range (about 25% typical, 40-44% at the 75th pct) instead of fixed points, or wait for the early pullback.
- **10-14 candle wicks:** an UP 10-14 candle first drops about 29 / 45 pts below its open (median), about 24% of its own range. A DOWN candle first rises about 31 / 47 pts. The opposite wick is made FIRST about 88% / 84-90% of the time.

### 3.1 (a) Move against the 06-10 lean after 10:00

| group | n | median pts against | 75th pct pts | 90th pct pts | median % of 06-10 range | 75th pct % | 50+ pts against % | median 06-10 range pts | median pts in favour | 10-14 closes lean way % |
|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 735 / 61 | 67 / 128 | 132 / 216 | 212 / 301 | 50.4 / 45.9 | 95 / 93.2 | 60.7 / 78.7 | 132 / 226 | 75.2 / 89.8 | 51.2 / 49.2 |
| bull lean | 387 / 33 | 61.5 / 117 | 134 / 215 | 217 / 329 | 50.2 / 41.1 | 105 / 93.2 | 58.4 / 72.7 | 127 / 220 | 78.2 / 75.5 | 55.8 / 51.5 |
| bear lean * | 348 / 28 | 74.4 / 135 | 129 / 229 | 202 / 268 | 50.9 / 54.8 | 89.7 / 93.1 | 63.2 / 85.7 | 143 / 247 | 73 / 104 | 46 / 46.4 |
| lean RIGHT (10-14 closes with lean) | 376 / 30 | 33.8 / 64.5 | 57.9 / 97.4 | 96.1 / 140 | 25.6 / 24.9 | 43.8 / 40 | 30.9 / 56.7 | 138 / 240 | 118 / 169 | 100 / 100 |
| lean WRONG | 359 / 31 | 123 / 215 | 185 / 274 | 272 / 375 | 90.8 / 83.8 | 136 / 135 | 91.9 / 100 | 129 / 220 | 36.2 / 54.2 | 0 / 0 |
| bull lean RIGHT * | 216 / 17 | 35.1 / 46.5 | 59.8 / 79.5 | 102 / 159 | 26.5 / 23.3 | 47.5 / 37.4 | 32.9 / 47.1 | 134 / 231 | 108 / 164 | 100 / 100 |
| bear lean RIGHT * | 160 / 13 | 31.5 / 73.2 | 52.8 / 110 | 90 / 134 | 23.1 / 30.4 | 41 / 43.1 | 28.1 / 69.2 | 144 / 265 | 141 / 174 | 100 / 100 |
| BC+ * | 199 / 21 | 68.8 / 128 | 135 / 200 | 244 / 242 | 51 / 43.1 | 95.5 / 63.3 | 58.8 / 81 | 153 / 260 | 71.5 / 98.5 | 49.7 / 42.9 |
| BC- * | 137 / 14 | 68.8 / 69.1 | 134 / 176 | 194 / 300 | 48.4 / 35.8 | 93.8 / 104 | 60.6 / 50 | 125 / 241 | 76 / 158 | 54 / 57.1 |
| C2 * | 145 / 10 | 74.5 / 85.1 | 127 / 134 | 200 / 163 | 47.5 / 33.9 | 76.2 / 45.3 | 64.1 / 80 | 166 / 240 | 76.8 / 116 | 49.7 / 70 |
| AFs * | 153 / 12 | 59.5 / 230 | 125 / 317 | 182 / 377 | 51 / 98.7 | 119 / 172 | 58.2 / 100 | 109 / 210 | 75.8 / 74.2 | 54.2 / 25 |
| CI * | 21 / 1 | 76.8 / 78 | 128 / 78 | 281 / 78 | 74.5 / 37.4 | 103 / 37.4 | 61.9 / 100 | 81.5 / 209 | 84.5 / 248 | 57.1 / 100 |
| S&D * | 80 / 3 | 62.9 / 216 | 131 / 227 | 211 / 234 | 54.1 / 93.2 | 99.1 / 114 | 63.8 / 100 | 131 / 203 | 71 / 46.5 | 45 / 66.7 |

**When does the worst point happen? (minutes after 10:00)**

| group | n | median minutes | by 10:30 % | 10:30-11 % | 11-12 % | 12-13 % | 13-14 % |
|---|---|---|---|---|---|---|---|
| ALL | 735 / 61 | 71 / 101 | 35 / 26.2 | 11.7 / 9.8 | 16.1 / 14.8 | 12.1 / 23 | 25.2 / 26.2 |
| bull lean | 387 / 33 | 62 / 90 | 36.7 / 30.3 | 11.4 / 9.1 | 18.1 / 18.2 | 11.9 / 15.2 | 22 / 27.3 |
| bear lean * | 348 / 28 | 88 / 126 | 33 / 21.4 | 12.1 / 10.7 | 13.8 / 10.7 | 12.4 / 32.1 | 28.7 / 25 |
| lean RIGHT (10-14 closes with lean) | 376 / 30 | 18.5 / 26 | 61.4 / 53.3 | 16.2 / 13.3 | 12.8 / 16.7 | 6.6 / 13.3 | 2.9 / 3.3 |
| lean WRONG | 359 / 31 | 175 / 175 | 7.2 / 0 | 7 / 6.5 | 19.5 / 12.9 | 17.8 / 32.3 | 48.5 / 48.4 |
| bull lean RIGHT * | 216 / 17 | 20.5 / 20 | 61.1 / 58.8 | 15.7 / 11.8 | 14.4 / 17.6 | 5.6 / 5.9 | 3.2 / 5.9 |
| bear lean RIGHT * | 160 / 13 | 17 / 48 | 61.9 / 46.2 | 16.9 / 15.4 | 10.6 / 15.4 | 8.1 / 23.1 | 2.5 / 0 |
| BC+ * | 199 / 21 | 75 / 127 | 37.2 / 14.3 | 7.5 / 14.3 | 18.6 / 14.3 | 11.1 / 38.1 | 25.6 / 19 |
| BC- * | 137 / 14 | 68 / 24.5 | 38.7 / 57.1 | 9.5 / 0 | 15.3 / 14.3 | 14.6 / 7.1 | 21.9 / 21.4 |
| C2 * | 145 / 10 | 64 / 51 | 31 / 40 | 17.2 / 10 | 14.5 / 20 | 11.7 / 10 | 25.5 / 20 |
| AFs * | 153 / 12 | 71 / 177 | 35.9 / 0 | 11.8 / 16.7 | 13.1 / 0 | 13.7 / 33.3 | 25.5 / 50 |
| CI * | 21 / 1 | 37 / 90 | 33.3 / 0 | 23.8 / 0 | 9.5 / 100 | 9.5 / 0 | 23.8 / 0 |
| S&D * | 80 / 3 | 83 / 82 | 28.8 / 33.3 | 12.5 / 0 | 21.2 / 33.3 | 8.8 / 0 | 28.8 / 33.3 |

### 3.2 (b) The 10-14 candle: how far it goes the wrong way first

"pts against open first" = for an UP candle, the lowest point below the open BEFORE the candle high is made (mirror for DOWN). "wick" = open to the low (any time).

| group | n | share % | median pts against first | 75th pct | median wick pts | 75th pct wick | median wick % of range | 75th pct wick % | opposite extreme made first % | median 10-14 range pts |
|---|---|---|---|---|---|---|---|---|---|---|
| ALL lean / 10-14 closes UP | 404 / 32 | 55 / 52.5 | 28.9 / 44.6 | 57.3 / 79.6 | 35.4 / 54.9 | 61.9 / 82 | 24 / 24 | 42.3 / 40.8 | 87.6 / 84.4 | 152 / 249 |
| ALL lean / 10-14 closes DOWN * | 331 / 29 | 45 / 47.5 | 30.8 / 46.5 | 57.5 / 90.8 | 33.8 / 68 | 59.6 / 90.8 | 19.4 / 20.9 | 37.2 / 37.7 | 90 / 89.7 | 178 / 250 |
| bull lean / 10-14 closes UP * | 216 / 17 | 55.8 / 51.5 | 28.9 / 40.8 | 53.9 / 78 | 35.1 / 46.5 | 59.8 / 79.5 | 23 / 23.9 | 42.4 / 41.2 | 87.5 / 82.4 | 150 / 204 |
| bull lean / 10-14 closes DOWN * | 171 / 16 | 44.2 / 48.5 | 33.5 / 36.4 | 73 / 76.2 | 39 / 42 | 74.8 / 76.2 | 21.4 / 18.6 | 37.7 / 30.3 | 90.1 / 93.8 | 179 / 268 |
| bear lean / 10-14 closes UP * | 188 / 15 | 54 / 53.6 | 28.8 / 47.8 | 57.9 / 78.6 | 35.8 / 55.5 | 66.8 / 82.8 | 24.8 / 24 | 42.2 / 36.9 | 87.8 / 86.7 | 153 / 274 |
| bear lean / 10-14 closes DOWN * | 160 / 13 | 46 / 46.4 | 27.2 / 73.2 | 47.9 / 110 | 31.5 / 73.2 | 52.8 / 110 | 17.6 / 21.1 | 36.8 / 48 | 90 / 84.6 | 178 / 230 |

## 4. BC runs around 09:30-10:00

A run starts at the first BC. Every next BC on the SAME side adds 1. NBCs in between do not stop the run. Only an OPPOSITE BC ends it. "pts to run extreme" = from the first BC close to the best high (bull) or low (bear) before the opposite BC. "pts to last BC close" = from first BC close to the close of the last same-side BC. The walk can go past 16:00 if no opposite BC shows up.

**Most important:**
- **A run is short: median 2 BCs, average about 2.5-2.8.** About 37% of runs are just ONE BC, then the other side body-closes. This is true on 5m, 15m and 1h, both periods.
- **Each new BC has about a 60% chance to get another one on the same side** (2nd BC ~60%, 2nd->3rd ~59%, 3rd->4th ~58%). It does not get safer or riskier as the run gets longer. Like flipping a coin that lands your way 6 times in 10.
- **09:30-11:30 runs do NOT have more BCs than other hours** (5m: 2.54 vs 2.44 avg). But they travel MORE points: 5m median 27 / 41 pts vs 10 / 18 pts at other hours; 15m 42 / 74 vs 18 / 34. Same count, bigger candles.
- **Bull runs last a bit longer than bear runs** (2022-25 5m 2.77 vs 2.74 from 09:30; 15m 3.00 vs 2.50; 1h 3.00 vs 2.40). The 10:00 candle family changes little for runs that start after 10:00 (5m avg 2.4-2.9 for every family). One useful line: on 1h, a 10:00 BC+ candle -> next run WITH its lean averages 3.0 BCs and median 88 pts (2022-25), the best family row.
- WARNING on "first BC after 09:30" split by 10:00 candle: that run often INCLUDES the 10:00 candle, so the "same lean" row peeks ahead. Use the "after 10:00" tables for trading rules.

### 4.1 5m - run from the first BC after 09:30

Run ended before 16:00: 100% / 100%

| group | n | avg BCs | median BCs | 1 BC % | 2 % | 3 % | 4 % | 5+ % | median pts to extreme | avg pts to extreme | median pts to last BC close | avg NBCs in run | median run minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 763 / 61 | 2.8 / 2.5 | 2 / 2 | 36.3 / 37.7 | 22.8 / 26.2 | 14.2 / 16.4 | 10.5 / 6.6 | 16.3 / 13.1 | 38.2 / 57.8 | 60 / 75.6 | 20.8 / 33.5 | 3 / 2.6 | 20 / 20 |
| bull runs | 403 / 36 | 2.8 / 2.5 | 2 / 2 | 37 / 36.1 | 22.1 / 33.3 | 14.1 / 8.3 | 9.2 / 8.3 | 17.6 / 13.9 | 34.8 / 56 | 53.3 / 63.7 | 19 / 30.5 | 3 / 2.5 | 20 / 20 |
| bear runs * | 360 / 25 | 2.7 / 2.5 | 2 / 2 | 35.6 / 40 | 23.6 / 16 | 14.2 / 28 | 11.9 / 4 | 14.7 / 12 | 43.6 / 73.2 | 67.4 / 92.7 | 22.4 / 53.8 | 3 / 2.9 | 20 / 25 |
| run side = 10:00 candle lean | 406 / 37 | 3.1 / 2.9 | 2 / 2 | 32.8 / 32.4 | 21.4 / 21.6 | 12.3 / 16.2 | 12.1 / 10.8 | 21.4 / 18.9 | 43.6 / 64.8 | 68.3 / 85.5 | 26.9 / 55.8 | 3.3 / 2.8 | 25 / 20 |
| run side AGAINST 10:00 candle lean * | 357 / 24 | 2.4 / 1.9 | 2 / 2 | 40.3 / 45.8 | 24.4 / 33.3 | 16.2 / 16.7 | 8.7 / 0 | 10.4 / 4.2 | 33.2 / 55.6 | 50.6 / 60.2 | 12 / 17.5 | 2.6 / 2.3 | 20 / 20 |
| 10:00 candle BC+ * | 199 / 22 | 2.8 / 2.4 | 2 / 2 | 35.2 / 45.5 | 22.1 / 13.6 | 14.1 / 18.2 | 12.1 / 9.1 | 16.6 / 13.6 | 41 / 42.1 | 64.8 / 69 | 25 / 28.5 | 2.6 / 1.9 | 20 / 17.5 |
| 10:00 candle BC- * | 105 / 4 | 2.8 / 1.5 | 2 / 1.5 | 35.2 / 50 | 25.7 / 50 | 8.6 / 0 | 12.4 / 0 | 18.1 / 0 | 43.2 / 38.2 | 57.9 / 40.6 | 21.8 / 9.2 | 2.7 / 2 | 25 / 17.5 |
| 10:00 candle C2 * | 28 / 2 | 3.2 / 3.5 | 2.5 / 3.5 | 21.4 / 50 | 28.6 / 0 | 3.6 / 0 | 28.6 / 0 | 17.9 / 50 | 34 / 126 | 61.9 / 126 | 21.9 / 101 | 2.3 / 2 | 22.5 / 27.5 |
| 10:00 candle AFs * | 290 / 26 | 2.7 / 2.9 | 2 / 2 | 37.2 / 23.1 | 21.7 / 34.6 | 16.9 / 23.1 | 9 / 3.8 | 15.2 / 15.4 | 38.2 / 83 | 57 / 91 | 18.1 / 58.5 | 3.4 / 3.4 | 25 / 22.5 |
| 10:00 candle CI * | 115 / 5 | 2.6 / 1.8 | 2 / 1 | 39.1 / 60 | 24.3 / 20 | 13 / 0 | 7 / 20 | 16.5 / 0 | 34.2 / 37.8 | 58.7 / 41.1 | 19 / 0 | 2.8 / 3 | 20 / 30 |
| 10:00 candle S&D * | 26 / 2 | 2.5 / 1.5 | 2 / 1.5 | 42.3 / 50 | 15.4 / 50 | 23.1 / 0 | 3.8 / 0 | 15.4 / 0 | 30.5 / 52 | 68 / 52 | 14.4 / 9.1 | 3.6 / 1 | 25 / 12.5 |
| 10:00 BC+ / run WITH its lean * | 111 / 15 | 3.6 / 2.8 | 3 / 3 | 25.2 / 40 | 18.9 / 6.7 | 9.9 / 20 | 17.1 / 13.3 | 28.8 / 20 | 54.5 / 64.2 | 84.2 / 82.2 | 40.8 / 64.2 | 3.3 / 2.1 | 35 / 30 |
| 10:00 BC+ / run AGAINST its lean * | 88 / 7 | 1.9 / 1.6 | 2 / 1 | 47.7 / 57.1 | 26.1 / 28.6 | 19.3 / 14.3 | 5.7 / 0 | 1.1 / 0 | 30.4 / 35 | 40.4 / 40.6 | 5.4 / 0 | 1.6 / 1.7 | 20 / 15 |
| 10:00 BC- / run WITH its lean * | 63 / 1 | 3.6 / 1 | 3 / 1 | 23.8 / 100 | 20.6 / 0 | 7.9 / 0 | 17.5 / 0 | 30.2 / 0 | 59.8 / 15 | 74.7 / 15 | 36.8 / 0 | 3.2 / 2 | 30 / 15 |
| 10:00 BC- / run AGAINST its lean * | 42 / 3 | 1.7 / 1.7 | 1 / 2 | 52.4 / 33.3 | 33.3 / 66.7 | 9.5 / 0 | 4.8 / 0 | 0 / 0 | 25.1 / 56 | 32.5 / 49.2 | 0 / 18.5 | 1.9 / 2 | 20 / 20 |
| 10:00 C2 / run WITH its lean * | 14 / 2 | 3.5 / 3.5 | 2 / 3.5 | 28.6 / 50 | 28.6 / 0 | 0 / 0 | 14.3 / 0 | 28.6 / 50 | 27.9 / 126 | 62.5 / 126 | 18 / 101 | 3.6 / 2 | 15 / 27.5 |
| 10:00 C2 / run AGAINST its lean * | 14 / 0 | 3 / - | 3.5 / - | 14.3 / - | 28.6 / - | 7.1 / - | 42.9 / - | 7.1 / - | 41.9 / - | 61.4 / - | 28.5 / - | 0.9 / - | 25 / - |
| 10:00 AFs / run WITH its lean * | 137 / 15 | 2.5 / 3.3 | 2 / 2 | 40.9 / 20 | 22.6 / 33.3 | 16.8 / 20 | 7.3 / 6.7 | 12.4 / 20 | 31.8 / 82.5 | 55.2 / 97.5 | 13.8 / 59.8 | 3.2 / 4.1 | 20 / 30 |
| 10:00 AFs / run AGAINST its lean * | 153 / 11 | 2.9 / 2.4 | 2 / 2 | 34 / 27.3 | 20.9 / 36.4 | 17 / 27.3 | 10.5 / 0 | 17.6 / 9.1 | 41.5 / 84.5 | 58.7 / 82.2 | 23.8 / 53.8 | 3.6 / 2.5 | 30 / 20 |
| 10:00 CI / run WITH its lean * | 66 / 2 | 2.9 / 3 | 2 / 3 | 39.4 / 0 | 22.7 / 50 | 9.1 / 0 | 9.1 / 50 | 19.7 / 0 | 34.6 / 47.8 | 64.3 / 47.8 | 22 / 38.9 | 3.2 / 2 | 20 / 25 |
| 10:00 CI / run AGAINST its lean * | 49 / 3 | 2.3 / 1 | 2 / 1 | 38.8 / 100 | 26.5 / 0 | 18.4 / 0 | 4.1 / 0 | 12.2 / 0 | 34 / 35.2 | 51.1 / 36.8 | 12 / 0 | 2.4 / 3.7 | 20 / 30 |
| 10:00 S&D / run WITH its lean * | 15 / 2 | 2.7 / 1.5 | 3 / 1.5 | 26.7 / 50 | 20 / 50 | 33.3 / 0 | 6.7 / 0 | 13.3 / 0 | 53 / 52 | 65.3 / 52 | 42.8 / 9.1 | 3.9 / 1 | 35 / 12.5 |
| 10:00 S&D / run AGAINST its lean * | 11 / 0 | 2.4 / - | 1 / - | 63.6 / - | 9.1 / - | 9.1 / - | 0 / - | 18.2 / - | 20 / - | 71.6 / - | 0 / - | 3.3 / - | 15 / - |

Chance of the next same-side BC:

| group | n | got 2nd BC % | 2nd -> 3rd % | 3rd -> 4th % | 4th -> 5th % |
|---|---|---|---|---|---|
| ALL | 763 / 61 | 63.7 / 62.3 | 64.2 / 57.9 | 65.4 / 54.5 | 60.8 / 66.7 |
| bull runs | 403 / 36 | 63 / 63.9 | 65 / 47.8 | 65.5 / 72.7 | 65.7 / 62.5 |
| bear runs * | 360 / 25 | 64.4 / 60 | 63.4 / 73.3 | 65.3 / 36.4 | 55.2 / 75 |
| run side = 10:00 candle lean | 406 / 37 | 67.2 / 67.6 | 68.1 / 68 | 73.1 / 64.7 | 64 / 63.6 |
| run side AGAINST 10:00 candle lean * | 357 / 24 | 59.7 / 54.2 | 59.2 / 38.5 | 54 / 20 | 54.4 / 100 |

### 4.2 5m - run from the first BC after 10:00

Run ended before 16:00: 100% / 100%

| group | n | avg BCs | median BCs | 1 BC % | 2 % | 3 % | 4 % | 5+ % | median pts to extreme | avg pts to extreme | median pts to last BC close | avg NBCs in run | median run minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 763 / 61 | 2.6 / 2.3 | 2 / 2 | 37.4 / 42.6 | 23.6 / 29.5 | 14.9 / 9.8 | 9.7 / 3.3 | 14.4 / 14.8 | 30.8 / 38.5 | 48.5 / 60.8 | 13.8 / 16.2 | 3 / 2.8 | 20 / 20 |
| bull runs | 397 / 36 | 2.7 / 2.3 | 2 / 2 | 34 / 44.4 | 24.7 / 25 | 16.9 / 11.1 | 9.3 / 2.8 | 15.1 / 16.7 | 29 / 35.2 | 44.4 / 51.6 | 16.2 / 18.1 | 3.2 / 2.8 | 20 / 20 |
| bear runs * | 366 / 25 | 2.5 / 2.3 | 2 / 2 | 41 / 40 | 22.4 / 36 | 12.8 / 8 | 10.1 / 4 | 13.7 / 12 | 35.1 / 52 | 52.9 / 74.1 | 10.5 / 12 | 2.9 / 2.7 | 20 / 20 |
| run side = 10:00 candle lean | 464 / 41 | 2.7 / 2.3 | 2 / 2 | 35.3 / 48.8 | 24.6 / 22 | 15.7 / 9.8 | 9.7 / 2.4 | 14.7 / 17.1 | 33 / 37 | 50 / 62.1 | 17.4 / 0 | 3.1 / 2.8 | 20 / 20 |
| run side AGAINST 10:00 candle lean * | 299 / 20 | 2.6 / 2.2 | 2 / 2 | 40.5 / 30 | 22.1 / 45 | 13.7 / 10 | 9.7 / 5 | 14 / 10 | 28.5 / 42.2 | 46 / 58.3 | 9 / 19.4 | 2.9 / 2.7 | 20 / 20 |
| 10:00 candle BC+ * | 199 / 22 | 2.6 / 2.5 | 2 / 1 | 35.2 / 54.5 | 23.6 / 18.2 | 16.1 / 0 | 10.6 / 4.5 | 14.6 / 22.7 | 33.2 / 35.2 | 47.4 / 59.4 | 18.2 / 0 | 2.9 / 2.7 | 20 / 20 |
| 10:00 candle BC- * | 105 / 4 | 2.4 / 1.5 | 2 / 1.5 | 40 / 50 | 23.8 / 50 | 17.1 / 0 | 7.6 / 0 | 11.4 / 0 | 30.8 / 31 | 44.8 / 28.6 | 9 / 6 | 2.7 / 2.2 | 20 / 17.5 |
| 10:00 candle C2 * | 28 / 2 | 2.5 / 1.5 | 2 / 1.5 | 42.9 / 50 | 14.3 / 50 | 21.4 / 0 | 7.1 / 0 | 14.3 / 0 | 27.2 / 56.4 | 50.7 / 56.4 | 12 / 30 | 3.2 / 2 | 27.5 / 17.5 |
| 10:00 candle AFs * | 290 / 26 | 2.7 / 2.5 | 2 / 2 | 37.6 / 30.8 | 25.5 / 30.8 | 12.1 / 19.2 | 10 / 3.8 | 14.8 / 15.4 | 29.6 / 64.2 | 49.9 / 74.3 | 11.4 / 25.5 | 3.1 / 3.1 | 20 / 25 |
| 10:00 candle CI * | 115 / 5 | 2.8 / 1.8 | 2 / 2 | 34.8 / 40 | 24.3 / 40 | 15.7 / 20 | 10.4 / 0 | 14.8 / 0 | 31.2 / 25.5 | 47.8 / 30.4 | 17.5 / 16.2 | 3.4 / 1.6 | 25 / 15 |
| 10:00 candle S&D * | 26 / 2 | 2.9 / 1.5 | 2 / 1.5 | 46.2 / 50 | 7.7 / 50 | 19.2 / 0 | 7.7 / 0 | 19.2 / 0 | 36.6 / 45.4 | 55.1 / 45.4 | 20.8 / 36 | 2.9 / 4 | 15 / 27.5 |
| 10:00 BC+ / run WITH its lean * | 134 / 14 | 2.6 / 2.6 | 2 / 1 | 37.3 / 57.1 | 23.1 / 14.3 | 17.2 / 0 | 9 / 0 | 13.4 / 28.6 | 32.1 / 45 | 47.5 / 66.4 | 16.9 / 0 | 2.8 / 3.7 | 20 / 22.5 |
| 10:00 BC+ / run AGAINST its lean * | 65 / 8 | 2.8 / 2.1 | 2 / 1.5 | 30.8 / 50 | 24.6 / 25 | 13.8 / 0 | 13.8 / 12.5 | 16.9 / 12.5 | 36.2 / 28.4 | 47.2 / 47.2 | 24.8 / 9.2 | 3.1 / 0.9 | 20 / 10 |
| 10:00 BC- / run WITH its lean * | 52 / 1 | 2.6 / 1 | 2 / 1 | 34.6 / 100 | 25 / 0 | 17.3 / 0 | 7.7 / 0 | 15.4 / 0 | 32.5 / 7 | 50.1 / 7 | 16.8 / 0 | 3.1 / 1 | 22.5 / 10 |
| 10:00 BC- / run AGAINST its lean * | 53 / 3 | 2.1 / 1.7 | 2 / 2 | 45.3 / 33.3 | 22.6 / 66.7 | 17 / 0 | 7.5 / 0 | 7.5 / 0 | 27.8 / 34.8 | 39.6 / 35.8 | 7 / 12 | 2.3 / 2.7 | 20 / 20 |
| 10:00 C2 / run WITH its lean * | 21 / 2 | 2.5 / 1.5 | 2 / 1.5 | 38.1 / 50 | 14.3 / 50 | 23.8 / 0 | 9.5 / 0 | 14.3 / 0 | 28.2 / 56.4 | 51.9 / 56.4 | 13.2 / 30 | 3.1 / 2 | 30 / 17.5 |
| 10:00 C2 / run AGAINST its lean * | 7 / 0 | 2.4 / - | 1 / - | 57.1 / - | 14.3 / - | 14.3 / - | 0 / - | 14.3 / - | 18.8 / - | 47.1 / - | 0 / - | 3.3 / - | 20 / - |
| 10:00 AFs / run WITH its lean * | 166 / 19 | 2.7 / 2.5 | 2 / 2 | 35.5 / 36.8 | 25.9 / 26.3 | 12.7 / 15.8 | 10.8 / 5.3 | 15.1 / 15.8 | 32.1 / 38.5 | 50.9 / 72.2 | 15.6 / 15.2 | 3.2 / 2.6 | 20 / 20 |
| 10:00 AFs / run AGAINST its lean * | 124 / 7 | 2.6 / 2.7 | 2 / 2 | 40.3 / 14.3 | 25 / 42.9 | 11.3 / 28.6 | 8.9 / 0 | 14.5 / 14.3 | 26.6 / 71 | 48.6 / 80.1 | 6.2 / 41.5 | 3 / 4.6 | 20 / 30 |
| 10:00 CI / run WITH its lean * | 76 / 4 | 2.9 / 1.8 | 2 / 1.5 | 28.9 / 50 | 28.9 / 25 | 14.5 / 25 | 11.8 / 0 | 15.8 / 0 | 37.4 / 21.2 | 54.4 / 28.9 | 20.5 / 9.2 | 3.6 / 2 | 25 / 17.5 |
| 10:00 CI / run AGAINST its lean * | 39 / 1 | 2.4 / 2 | 2 / 2 | 46.2 / 0 | 15.4 / 100 | 17.9 / 0 | 7.7 / 0 | 12.8 / 0 | 25.5 / 36.5 | 34.9 / 36.5 | 5.8 / 16.2 | 2.9 / 0 | 15 / 10 |
| 10:00 S&D / run WITH its lean * | 15 / 1 | 2.6 / 1 | 2 / 1 | 46.7 / 100 | 13.3 / 0 | 26.7 / 0 | 0 / 0 | 13.3 / 0 | 36 / 8.2 | 38.4 / 8.2 | 17.8 / 0 | 2.9 / 1 | 15 / 10 |
| 10:00 S&D / run AGAINST its lean * | 11 / 1 | 3.4 / 2 | 3 / 2 | 45.5 / 0 | 0 / 100 | 9.1 / 0 | 18.2 / 0 | 27.3 / 0 | 52.5 / 82.5 | 77.8 / 82.5 | 40.8 / 72 | 2.9 / 7 | 15 / 45 |

Chance of the next same-side BC:

| group | n | got 2nd BC % | 2nd -> 3rd % | 3rd -> 4th % | 4th -> 5th % |
|---|---|---|---|---|---|
| ALL | 763 / 61 | 62.6 / 57.4 | 62.3 / 48.6 | 61.7 / 64.7 | 59.8 / 81.8 |
| bull runs | 397 / 36 | 66 / 55.6 | 62.6 / 55 | 59.1 / 63.6 | 61.9 / 85.7 |
| bear runs * | 366 / 25 | 59 / 60 | 62 / 40 | 64.9 / 66.7 | 57.5 / 75 |
| run side = 10:00 candle lean | 464 / 41 | 64.7 / 51.2 | 62 / 57.1 | 60.8 / 66.7 | 60.2 / 87.5 |
| run side AGAINST 10:00 candle lean * | 299 / 20 | 59.5 / 70 | 62.9 / 35.7 | 63.4 / 60 | 59.2 / 66.7 |

### 4.3 5m - ALL runs by the hour they START (whole data, every run)

| start time | n | avg BCs | median BCs | 1 BC % | 2 % | 3 % | 4 % | 5+ % | median pts to extreme | avg pts to extreme | median pts to last BC close | avg NBCs in run | median run minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Asia 18:00-02:00 | 13717 / 1073 | 2.4 / 2.5 | 2 / 2 | 40.5 / 39.4 | 25.1 / 25.3 | 14.8 / 15.9 | 8.5 / 7.2 | 11.1 / 12.1 | 6.5 / 15.2 | 12.7 / 26.7 | 2.5 / 6.8 | 3 / 3.1 | 20 / 20 |
| London 02:00-08:00 | 10536 / 824 | 2.5 / 2.5 | 2 / 2 | 38.9 / 40.3 | 25.2 / 22.3 | 15.2 / 15.5 | 8.4 / 8 | 12.3 / 13.8 | 10 / 17.5 | 17.6 / 32.1 | 4.5 / 6.9 | 2.7 / 2.9 | 20 / 20 |
| pre 08:00-09:30 | 2777 / 220 | 2.5 / 2.4 | 2 / 2 | 39.4 / 39.5 | 26 / 25.9 | 13.8 / 13.6 | 8.2 / 10 | 12.6 / 10.9 | 15 / 26.8 | 32.9 / 46.3 | 6.2 / 10.5 | 2.5 / 2.4 | 20 / 20 |
| NY AM 09:30-11:30 | 3470 / 296 | 2.5 / 2.5 | 2 / 2 | 39.2 / 38.2 | 24.4 / 24.3 | 13.3 / 15.2 | 9.7 / 8.8 | 13.4 / 13.5 | 26.6 / 41.1 | 44.4 / 61.4 | 12 / 18.5 | 2.9 / 2.6 | 20 / 20 |
| midday 11:30-14:00 | 4162 / 352 | 2.6 / 2.3 | 2 / 2 | 39.4 / 42 | 23.8 / 25 | 14.3 / 16.5 | 8.8 / 5.1 | 13.7 / 11.4 | 18.5 / 26 | 32.5 / 44.2 | 8.5 / 9 | 2.9 / 2.9 | 20 / 20 |
| NY PM 14:00-16:00 | 3269 / 273 | 2.5 / 2.5 | 2 / 2 | 39.7 / 38.1 | 24.4 / 21.6 | 14.4 / 17.2 | 9 / 9.2 | 12.4 / 13.9 | 18.2 / 26.8 | 31.8 / 40 | 7.2 / 12 | 3 / 3 | 20 / 20 |
| after 16:00-18:00 | 1486 / 132 | 2.3 / 2.2 | 2 / 2 | 40.6 / 44.7 | 25.5 / 24.2 | 15.1 / 13.6 | 8.5 / 9.8 | 10.2 / 7.6 | 8.2 / 14.8 | 19.5 / 31.1 | 3 / 2.5 | 2.8 / 2.9 | 35 / 30 |
| ALL OTHER HOURS | 35947 / 2874 | 2.4 / 2.4 | 2 / 2 | 39.8 / 40.1 | 25 / 24.1 | 14.8 / 15.7 | 8.5 / 7.7 | 11.9 / 12.4 | 9.8 / 18.2 | 20 / 33.3 | 3.8 / 7.8 | 2.9 / 2.9 | 20 / 20 |
| ALL RUNS | 39417 / 3170 | 2.5 / 2.5 | 2 / 2 | 39.7 / 39.9 | 24.9 / 24.1 | 14.6 / 15.7 | 8.6 / 7.8 | 12.1 / 12.5 | 10.8 / 19.8 | 22.1 / 36 | 4 / 8 | 2.9 / 2.9 | 20 / 20 |
| NY AM 09:30-11:30 bull | 1754 / 149 | 2.7 / 2.7 | 2 / 2 | 34.8 / 34.9 | 24.5 / 27.5 | 14.3 / 12.8 | 10.4 / 7.4 | 16 / 17.4 | 28 / 39.8 | 42.9 / 59.8 | 15.2 / 20.2 | 2.9 / 2.9 | 20 / 20 |
| NY AM 09:30-11:30 bear | 1716 / 147 | 2.3 / 2.4 | 2 / 2 | 43.6 / 41.5 | 24.4 / 21.1 | 12.4 / 17.7 | 8.9 / 10.2 | 10.8 / 9.5 | 25.5 / 43.2 | 45.9 / 63 | 8.5 / 17.8 | 2.8 / 2.4 | 20 / 20 |

| start time | n | got 2nd BC % | 2nd -> 3rd % | 3rd -> 4th % | 4th -> 5th % |
|---|---|---|---|---|---|
| Asia 18:00-02:00 | 13717 / 1073 | 59.5 / 60.6 | 57.8 / 58.2 | 57 / 54.8 | 56.5 / 62.8 |
| London 02:00-08:00 | 10536 / 824 | 61.1 / 59.7 | 58.8 / 62.6 | 57.6 / 58.4 | 59.3 / 63.3 |
| pre 08:00-09:30 | 2777 / 220 | 60.6 / 60.5 | 57.1 / 57.1 | 60 / 60.5 | 60.5 / 52.2 |
| NY AM 09:30-11:30 | 3470 / 296 | 60.8 / 61.8 | 59.9 / 60.7 | 63.4 / 59.5 | 58.2 / 60.6 |
| midday 11:30-14:00 | 4162 / 352 | 60.6 / 58 | 60.7 / 56.9 | 61.1 / 50 | 60.9 / 69 |
| NY PM 14:00-16:00 | 3269 / 273 | 60.3 / 61.9 | 59.4 / 65.1 | 59.7 / 57.3 | 57.9 / 60.3 |
| after 16:00-18:00 | 1486 / 132 | 59.4 / 55.3 | 57.1 / 56.2 | 55.4 / 56.1 | 54.5 / 43.5 |
| ALL OTHER HOURS | 35947 / 2874 | 60.2 / 59.9 | 58.5 / 59.8 | 58.1 / 56.1 | 58.3 / 61.7 |
| ALL RUNS | 39417 / 3170 | 60.3 / 60.1 | 58.6 / 59.9 | 58.6 / 56.4 | 58.3 / 61.6 |
| NY AM 09:30-11:30 bull | 1754 / 149 | 65.2 / 65.1 | 62.5 / 57.7 | 65 / 66.1 | 60.6 / 70.3 |
| NY AM 09:30-11:30 bear | 1716 / 147 | 56.4 / 58.5 | 56.8 / 64 | 61.4 / 52.7 | 54.9 / 48.3 |

### 4.4 15m - run from the first BC after 09:30

Run ended before 16:00: 99.1% / 100%

| group | n | avg BCs | median BCs | 1 BC % | 2 % | 3 % | 4 % | 5+ % | median pts to extreme | avg pts to extreme | median pts to last BC close | avg NBCs in run | median run minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 763 / 61 | 2.8 / 2.6 | 2 / 2 | 37 / 32.8 | 21.6 / 27.9 | 15.1 / 19.7 | 10 / 9.8 | 16.4 / 9.8 | 55.2 / 90 | 84 / 110 | 29.8 / 63.5 | 2.9 / 3 | 60 / 60 |
| bull runs | 401 / 33 | 3 / 2.9 | 2 / 2 | 33.2 / 30.3 | 20 / 24.2 | 17.5 / 27.3 | 11.5 / 6.1 | 18 / 12.1 | 56.2 / 90 | 78.9 / 106 | 39 / 63.5 | 3.2 / 3 | 75 / 60 |
| bear runs * | 362 / 28 | 2.5 / 2.2 | 2 / 2 | 41.2 / 35.7 | 23.5 / 32.1 | 12.4 / 10.7 | 8.3 / 14.3 | 14.6 / 7.1 | 54.1 / 92.8 | 89.7 / 115 | 23.9 / 57.4 | 2.6 / 2.9 | 60 / 67.5 |
| run side = 10:00 candle lean | 488 / 40 | 3.2 / 2.9 | 3 / 2 | 21.5 / 17.5 | 26 / 37.5 | 18.6 / 25 | 12.3 / 7.5 | 21.5 / 12.5 | 76.2 / 120 | 102 / 127 | 54.4 / 84.5 | 3.2 / 2.7 | 75 / 60 |
| run side AGAINST 10:00 candle lean * | 275 / 21 | 1.9 / 2 | 1 / 1 | 64.4 / 61.9 | 13.8 / 9.5 | 8.7 / 9.5 | 5.8 / 14.3 | 7.3 / 4.8 | 31.5 / 50.5 | 51.4 / 77.3 | 0 / 0 | 2.5 / 3.4 | 30 / 45 |
| 10:00 candle BC+ * | 210 / 26 | 3.4 / 2.9 | 3 / 2 | 20.5 / 26.9 | 24.3 / 30.8 | 21.4 / 26.9 | 10.5 / 7.7 | 23.3 / 7.7 | 93.4 / 110 | 112 / 125 | 67.4 / 77.5 | 2.8 / 2.1 | 75 / 60 |
| 10:00 candle BC- * | 116 / 6 | 3.1 / 2 | 3 / 2 | 19 / 16.7 | 29.3 / 66.7 | 19 / 16.7 | 15.5 / 0 | 17.2 / 0 | 68.8 / 70.6 | 93.4 / 87.1 | 43.5 / 44.9 | 2.5 / 1 | 60 / 45 |
| 10:00 candle C2 * | 17 / 2 | 1.9 / 5 | 1 / 5 | 64.7 / 0 | 17.6 / 0 | 5.9 / 0 | 5.9 / 0 | 5.9 / 100 | 21 / 197 | 36.6 / 197 | 0 / 183 | 1 / 8.5 | 15 / 202 |
| 10:00 candle AFs * | 283 / 21 | 2.3 / 2.3 | 2 / 2 | 49.5 / 47.6 | 18 / 19 | 12.4 / 9.5 | 8.8 / 14.3 | 11.3 / 9.5 | 44 / 60.8 | 66.9 / 93.3 | 0 / 0 | 3.1 / 4.1 | 60 / 75 |
| 10:00 candle CI * | 124 / 5 | 2.6 / 2 | 2 / 2 | 47.6 / 40 | 20.2 / 20 | 8.1 / 40 | 7.3 / 0 | 16.9 / 0 | 42.2 / 69.2 | 73.6 / 66.6 | 9 / 44.8 | 3.4 / 2.4 | 60 / 75 |
| 10:00 candle S&D * | 13 / 1 | 2.4 / 4 | 1 / 4 | 53.8 / 0 | 7.7 / 0 | 15.4 / 0 | 7.7 / 100 | 15.4 / 0 | 76.2 / 242 | 79.2 / 242 | 0 / 207 | 3.6 / 4 | 75 / 120 |
| 10:00 BC+ / run WITH its lean * | 183 / 22 | 3.7 / 3.2 | 3 / 2.5 | 8.7 / 13.6 | 27.9 / 36.4 | 24.6 / 31.8 | 12 / 9.1 | 26.8 / 9.1 | 112 / 125 | 125 / 142 | 80.8 / 94.5 | 3.2 / 2.5 | 75 / 60 |
| 10:00 BC+ / run AGAINST its lean * | 27 / 4 | 1 / 1 | 1 / 1 | 100 / 100 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 19.5 / 37.6 | 26.3 / 34.4 | 0 / 0 | 0 / 0 | 15 / 15 |
| 10:00 BC- / run WITH its lean * | 107 / 6 | 3.3 / 2 | 3 / 2 | 12.1 / 16.7 | 31.8 / 66.7 | 20.6 / 16.7 | 16.8 / 0 | 18.7 / 0 | 73 / 70.6 | 98.5 / 87.1 | 49.8 / 44.9 | 2.7 / 1 | 75 / 45 |
| 10:00 BC- / run AGAINST its lean * | 9 / 0 | 1 / - | 1 / - | 100 / - | 0 / - | 0 / - | 0 / - | 0 / - | 31.2 / - | 32.6 / - | 0 / - | 0 / - | 15 / - |
| 10:00 C2 / run WITH its lean * | 8 / 2 | 2.9 / 5 | 2 / 5 | 25 / 0 | 37.5 / 0 | 12.5 / 0 | 12.5 / 0 | 12.5 / 100 | 54 / 197 | 59.7 / 197 | 39.4 / 183 | 2.1 / 8.5 | 45 / 202 |
| 10:00 C2 / run AGAINST its lean * | 9 / 0 | 1 / - | 1 / - | 100 / - | 0 / - | 0 / - | 0 / - | 0 / - | 17 / - | 16.2 / - | 0 / - | 0 / - | 15 / - |
| 10:00 AFs / run WITH its lean * | 121 / 8 | 2.7 / 2.4 | 2 / 2 | 37.2 / 37.5 | 19.8 / 25 | 14.9 / 12.5 | 10.7 / 12.5 | 17.4 / 12.5 | 53.5 / 98.2 | 80.9 / 101 | 31.5 / 57.9 | 3.5 / 3.2 | 75 / 67.5 |
| 10:00 AFs / run AGAINST its lean * | 162 / 13 | 2 / 2.3 | 1 / 1 | 58.6 / 53.8 | 16.7 / 15.4 | 10.5 / 7.7 | 7.4 / 15.4 | 6.8 / 7.7 | 36 / 52 | 56.5 / 88.5 | 0 / 0 | 2.9 / 4.6 | 45 / 90 |
| 10:00 CI / run WITH its lean * | 63 / 2 | 3 / 2.5 | 2 / 2.5 | 39.7 / 0 | 23.8 / 50 | 6.3 / 50 | 9.5 / 0 | 20.6 / 0 | 59 / 120 | 91.6 / 120 | 36 / 91 | 3.6 / 2.5 | 75 / 75 |
| 10:00 CI / run AGAINST its lean * | 61 / 3 | 2.3 / 1.7 | 1 / 1 | 55.7 / 66.7 | 16.4 / 0 | 9.8 / 33.3 | 4.9 / 0 | 13.1 / 0 | 35.5 / 21.8 | 54.9 / 30.8 | 0 / 0 | 3.2 / 2.3 | 45 / 45 |
| 10:00 S&D / run WITH its lean * | 6 / 0 | 2.3 / - | 1 / - | 66.7 / - | 0 / - | 16.7 / - | 0 / - | 16.7 / - | 76.9 / - | 91.3 / - | 0 / - | 3 / - | 67.5 / - |
| 10:00 S&D / run AGAINST its lean * | 7 / 1 | 2.4 / 4 | 2 / 4 | 42.9 / 0 | 14.3 / 0 | 14.3 / 0 | 14.3 / 100 | 14.3 / 0 | 76.2 / 242 | 68.8 / 242 | 60.5 / 207 | 4.1 / 4 | 105 / 120 |

Chance of the next same-side BC:

| group | n | got 2nd BC % | 2nd -> 3rd % | 3rd -> 4th % | 4th -> 5th % |
|---|---|---|---|---|---|
| ALL | 763 / 61 | 63 / 67.2 | 65.7 / 58.5 | 63.6 / 50 | 62.2 / 50 |
| bull runs | 401 / 33 | 66.8 / 69.7 | 70.1 / 65.2 | 62.8 / 40 | 61 / 66.7 |
| bear runs * | 362 / 28 | 58.8 / 64.3 | 60.1 / 50 | 64.8 / 66.7 | 63.9 / 33.3 |
| run side = 10:00 candle lean | 488 / 40 | 78.5 / 82.5 | 66.8 / 54.5 | 64.5 / 44.4 | 63.6 / 62.5 |
| run side AGAINST 10:00 candle lean * | 275 / 21 | 35.6 / 38.1 | 61.2 / 75 | 60 / 66.7 | 55.6 / 25 |

### 4.5 15m - run from the first BC after 10:00

Run ended before 16:00: 98.7% / 100%

| group | n | avg BCs | median BCs | 1 BC % | 2 % | 3 % | 4 % | 5+ % | median pts to extreme | avg pts to extreme | median pts to last BC close | avg NBCs in run | median run minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 763 / 61 | 2.6 / 2.6 | 2 / 2 | 37.1 / 41 | 24 / 27.9 | 15.3 / 11.5 | 8.9 / 8.2 | 14.7 / 11.5 | 43.5 / 65 | 68.2 / 93.7 | 21.2 / 29.8 | 3 / 2.8 | 60 / 45 |
| bull runs * | 419 / 29 | 2.8 / 3.2 | 2 / 2 | 34.1 / 27.6 | 25.3 / 31 | 16.9 / 10.3 | 6.9 / 13.8 | 16.7 / 17.2 | 40.8 / 86.8 | 59.9 / 108 | 22.2 / 62.8 | 3.1 / 3.5 | 60 / 75 |
| bear runs | 344 / 32 | 2.5 / 2 | 2 / 1 | 40.7 / 53.1 | 22.4 / 25 | 13.4 / 12.5 | 11.3 / 3.1 | 12.2 / 6.2 | 48.1 / 61 | 78.4 / 80.6 | 20 / 0 | 2.8 / 2.1 | 60 / 45 |
| run side = 10:00 candle lean | 496 / 34 | 2.8 / 2.9 | 2 / 2 | 37.1 / 41.2 | 21.4 / 23.5 | 14.9 / 8.8 | 10.1 / 11.8 | 16.5 / 14.7 | 45 / 67.5 | 72.8 / 99.9 | 25.2 / 33.5 | 3.1 / 3.2 | 60 / 67.5 |
| run side AGAINST 10:00 candle lean * | 267 / 27 | 2.5 / 2.2 | 2 / 2 | 37.1 / 40.7 | 28.8 / 33.3 | 16.1 / 14.8 | 6.7 / 3.7 | 11.2 / 7.4 | 37.8 / 65 | 59.8 / 85.9 | 15 / 27.8 | 2.8 / 2.3 | 60 / 45 |
| 10:00 candle BC+ * | 210 / 26 | 2.8 / 2.6 | 2 / 2 | 35.2 / 42.3 | 24.3 / 38.5 | 15.2 / 7.7 | 9 / 0 | 16.2 / 11.5 | 45.6 / 56.2 | 74.3 / 92.9 | 22.8 / 28.2 | 3.1 / 2.5 | 67.5 / 45 |
| 10:00 candle BC- * | 116 / 6 | 2.6 / 2 | 2 / 2 | 37.1 / 33.3 | 27.6 / 50 | 13.8 / 0 | 10.3 / 16.7 | 11.2 / 0 | 39.1 / 57.9 | 60.4 / 74.8 | 18.8 / 25.6 | 2.7 / 1.3 | 60 / 45 |
| 10:00 candle C2 * | 17 / 2 | 2.7 / 4 | 2 / 4 | 35.3 / 0 | 29.4 / 0 | 5.9 / 0 | 5.9 / 100 | 23.5 / 0 | 59.5 / 151 | 76.6 / 151 | 38.8 / 136 | 2.2 / 5.5 | 60 / 142 |
| 10:00 candle AFs * | 283 / 21 | 2.5 / 2.7 | 2 / 2 | 36 / 42.9 | 25.8 / 14.3 | 17.3 / 14.3 | 8.8 / 9.5 | 12 / 19 | 41.2 / 86.8 | 65.2 / 103 | 21.5 / 66.5 | 2.8 / 3.7 | 60 / 60 |
| 10:00 candle CI * | 124 / 5 | 2.8 / 1.6 | 2 / 1 | 43.5 / 60 | 14.5 / 20 | 14.5 / 20 | 8.1 / 0 | 19.4 / 0 | 43.2 / 35.5 | 69.4 / 48.5 | 16.2 / 0 | 3.4 / 1.8 | 75 / 45 |
| 10:00 candle S&D * | 13 / 1 | 3.3 / 3 | 2 / 3 | 30.8 / 0 | 30.8 / 0 | 7.7 / 100 | 7.7 / 0 | 23.1 / 0 | 72 / 150 | 83.3 / 150 | 29.8 / 114 | 3.8 / 1 | 60 / 60 |
| 10:00 BC+ / run WITH its lean * | 147 / 16 | 2.9 / 3 | 2 / 2 | 37.4 / 31.2 | 19.7 / 50 | 14.3 / 6.2 | 10.9 / 0 | 17.7 / 12.5 | 49.8 / 56.2 | 77.1 / 101 | 19.8 / 33.5 | 3.1 / 2.6 | 60 / 67.5 |
| 10:00 BC+ / run AGAINST its lean * | 63 / 10 | 2.5 / 2.1 | 2 / 1 | 30.2 / 60 | 34.9 / 20 | 17.5 / 10 | 4.8 / 0 | 12.7 / 10 | 42.2 / 52 | 67.8 / 79.1 | 23.2 / 0 | 3 / 2.4 | 75 / 45 |
| 10:00 BC- / run WITH its lean * | 69 / 1 | 2.5 / 1 | 2 / 1 | 36.2 / 100 | 29 / 0 | 11.6 / 0 | 13 / 0 | 10.1 / 0 | 43.8 / 26.8 | 61.5 / 26.8 | 20.2 / 0 | 3 / 1 | 75 / 30 |
| 10:00 BC- / run AGAINST its lean * | 47 / 5 | 2.7 / 2.2 | 2 / 2 | 38.3 / 20 | 25.5 / 60 | 17 / 0 | 6.4 / 20 | 12.8 / 0 | 36.5 / 58.8 | 58.9 / 84.3 | 14 / 42 | 2.4 / 1.4 | 60 / 45 |
| 10:00 C2 / run WITH its lean * | 13 / 2 | 2.1 / 4 | 2 / 4 | 46.2 / 0 | 30.8 / 0 | 7.7 / 0 | 0 / 100 | 15.4 / 0 | 31 / 151 | 55.3 / 151 | 12.8 / 136 | 1.9 / 5.5 | 45 / 142 |
| 10:00 C2 / run AGAINST its lean * | 4 / 0 | 4.5 / - | 4.5 / - | 0 / - | 25 / - | 0 / - | 25 / - | 50 / - | 139 / - | 146 / - | 117 / - | 3.5 / - | 82.5 / - |
| 10:00 AFs / run WITH its lean * | 181 / 12 | 2.6 / 2.9 | 2 / 2 | 34.3 / 50 | 23.2 / 0 | 17.7 / 8.3 | 9.9 / 16.7 | 14.9 / 25 | 45 / 92 | 72.8 / 105 | 30.2 / 34.1 | 2.9 / 4.2 | 60 / 75 |
| 10:00 AFs / run AGAINST its lean * | 102 / 9 | 2.2 / 2.4 | 2 / 2 | 39.2 / 33.3 | 30.4 / 33.3 | 16.7 / 22.2 | 6.9 / 0 | 6.9 / 11.1 | 35.9 / 82.5 | 51.9 / 100 | 6.5 / 66.5 | 2.5 / 3 | 60 / 60 |
| 10:00 CI / run WITH its lean * | 80 / 3 | 3 / 1.7 | 2 / 1 | 43.8 / 66.7 | 11.2 / 0 | 15 / 33.3 | 8.8 / 0 | 21.2 / 0 | 47.8 / 35.5 | 74.2 / 62.9 | 19.1 / 0 | 3.3 / 2 | 60 / 45 |
| 10:00 CI / run AGAINST its lean * | 44 / 2 | 2.6 / 1.5 | 2 / 1.5 | 43.2 / 50 | 20.5 / 50 | 13.6 / 0 | 6.8 / 0 | 15.9 / 0 | 39 / 26.9 | 60.5 / 26.9 | 11.2 / 13.9 | 3.6 / 1.5 | 75 / 45 |
| 10:00 S&D / run WITH its lean * | 6 / 0 | 4.8 / - | 4.5 / - | 16.7 / - | 33.3 / - | 0 / - | 0 / - | 50 / - | 129 / - | 116 / - | 75.8 / - | 5.5 / - | 142 / - |
| 10:00 S&D / run AGAINST its lean * | 7 / 1 | 2 / 3 | 2 / 3 | 42.9 / 0 | 28.6 / 0 | 14.3 / 100 | 14.3 / 0 | 0 / 0 | 36.5 / 150 | 55 / 150 | 17.8 / 114 | 2.3 / 1 | 45 / 60 |

Chance of the next same-side BC:

| group | n | got 2nd BC % | 2nd -> 3rd % | 3rd -> 4th % | 4th -> 5th % |
|---|---|---|---|---|---|
| ALL | 763 / 61 | 62.9 / 59 | 61.9 / 52.8 | 60.6 / 63.2 | 62.2 / 58.3 |
| bull runs * | 419 / 29 | 65.9 / 72.4 | 61.6 / 57.1 | 58.2 / 75 | 70.7 / 55.6 |
| bear runs | 344 / 32 | 59.3 / 46.9 | 62.3 / 46.7 | 63.8 / 42.9 | 51.9 / 66.7 |
| run side = 10:00 candle lean | 496 / 34 | 62.9 / 58.8 | 66 / 60 | 64.1 / 75 | 62.1 / 55.6 |
| run side AGAINST 10:00 candle lean * | 267 / 27 | 62.9 / 59.3 | 54.2 / 43.8 | 52.7 / 42.9 | 62.5 / 66.7 |

### 4.6 15m - ALL runs by the hour they START (whole data, every run)

| start time | n | avg BCs | median BCs | 1 BC % | 2 % | 3 % | 4 % | 5+ % | median pts to extreme | avg pts to extreme | median pts to last BC close | avg NBCs in run | median run minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Asia 18:00-02:00 | 4695 / 366 | 2.4 / 2.6 | 2 / 2 | 40.5 / 34.7 | 25.3 / 26.8 | 14.7 / 14.8 | 8.4 / 9.6 | 11.1 / 14.2 | 11.8 / 28.1 | 22.8 / 47.5 | 4.5 / 12.2 | 2.9 / 2.9 | 60 / 60 |
| London 02:00-08:00 | 3508 / 280 | 2.5 / 2.5 | 2 / 2 | 38.2 / 40 | 25.3 / 21.8 | 15.5 / 17.1 | 9 / 8.9 | 12.1 / 12.1 | 17.5 / 37.1 | 34.4 / 57.1 | 8 / 14.8 | 2.7 / 2.7 | 60 / 60 |
| pre 08:00-09:30 | 942 / 83 | 2.5 / 2.2 | 2 / 2 | 41 / 44.6 | 25.3 / 26.5 | 13 / 12 | 7.4 / 3.6 | 13.4 / 13.3 | 31.1 / 44 | 64.7 / 89.1 | 10.6 / 16.8 | 2.5 / 2.5 | 60 / 45 |
| NY AM 09:30-11:30 | 1177 / 100 | 2.6 / 2.6 | 2 / 2 | 37.5 / 35 | 25.9 / 27 | 13.7 / 18 | 9.3 / 7 | 13.6 / 13 | 42.2 / 73.5 | 71.3 / 101 | 21.5 / 40.5 | 2.8 / 2.9 | 60 / 60 |
| midday 11:30-14:00 | 1421 / 116 | 2.6 / 2.3 | 2 / 2 | 39.5 / 44.8 | 23.4 / 24.1 | 14.1 / 15.5 | 8.9 / 7.8 | 14.1 / 7.8 | 32 / 46.2 | 55.4 / 75 | 14.8 / 7.8 | 2.9 / 2.9 | 60 / 60 |
| NY PM 14:00-16:00 | 1091 / 98 | 2.4 / 2.3 | 2 / 2 | 38 / 40.8 | 25.7 / 29.6 | 15.1 / 12.2 | 9.3 / 9.2 | 11.9 / 8.2 | 29.2 / 40 | 49.2 / 65 | 11.5 / 16.4 | 3.1 / 2.7 | 60 / 60 |
| after 16:00-18:00 | 401 / 43 | 2.3 / 2 | 2 / 1 | 40.1 / 55.8 | 27.7 / 18.6 | 16 / 14 | 8 / 2.3 | 8.2 / 9.3 | 15.5 / 19.8 | 32.7 / 50 | 6.2 / 0 | 2.7 / 2.3 | 135 / 120 |
| ALL OTHER HOURS | 12058 / 986 | 2.5 / 2.4 | 2 / 2 | 39.5 / 39.8 | 25.2 / 24.9 | 14.8 / 15 | 8.6 / 8.3 | 11.9 / 12 | 17.5 / 34 | 36 / 58.8 | 6.8 / 12.1 | 2.8 / 2.8 | 60 / 60 |
| ALL RUNS | 13235 / 1086 | 2.5 / 2.5 | 2 / 2 | 39.3 / 39.3 | 25.2 / 25.1 | 14.7 / 15.3 | 8.7 / 8.2 | 12.1 / 12.1 | 19 / 37.9 | 39.1 / 62.7 | 7.2 / 13.8 | 2.8 / 2.8 | 60 / 60 |
| NY AM 09:30-11:30 bull | 593 / 53 | 2.8 / 2.9 | 2 / 2 | 33.2 / 30.2 | 24.3 / 28.3 | 15.3 / 20.8 | 9.4 / 7.5 | 17.7 / 13.2 | 43.2 / 84.5 | 66.6 / 106 | 26 / 45 | 2.9 / 3.2 | 60 / 60 |
| NY AM 09:30-11:30 bear | 584 / 47 | 2.3 / 2.3 | 2 / 2 | 41.8 / 40.4 | 27.6 / 25.5 | 12 / 14.9 | 9.2 / 6.4 | 9.4 / 12.8 | 41.5 / 70 | 76 / 95.6 | 13.4 / 27.8 | 2.7 / 2.5 | 60 / 60 |

| start time | n | got 2nd BC % | 2nd -> 3rd % | 3rd -> 4th % | 4th -> 5th % |
|---|---|---|---|---|---|
| Asia 18:00-02:00 | 4695 / 366 | 59.5 / 65.3 | 57.5 / 59 | 57.1 / 61.7 | 57 / 59.8 |
| London 02:00-08:00 | 3508 / 280 | 61.8 / 60 | 59 / 63.7 | 57.6 / 55.1 | 57.4 / 57.6 |
| pre 08:00-09:30 | 942 / 83 | 59 / 55.4 | 57.2 / 52.2 | 61.6 / 58.3 | 64.3 / 78.6 |
| NY AM 09:30-11:30 | 1177 / 100 | 62.5 / 65 | 58.6 / 58.5 | 62.6 / 52.6 | 59.3 / 65 |
| midday 11:30-14:00 | 1421 / 116 | 60.5 / 55.2 | 61.4 / 56.2 | 62 / 50 | 61.2 / 50 |
| NY PM 14:00-16:00 | 1091 / 98 | 62 / 59.2 | 58.6 / 50 | 58.3 / 58.6 | 56.3 / 47.1 |
| after 16:00-18:00 | 401 / 43 | 59.9 / 44.2 | 53.8 / 57.9 | 50.4 / 45.5 | 50.8 / 80 |
| ALL OTHER HOURS | 12058 / 986 | 60.5 / 60.2 | 58.4 / 58.6 | 58.1 / 57.5 | 58 / 59 |
| ALL RUNS | 13235 / 1086 | 60.7 / 60.7 | 58.4 / 58.6 | 58.5 / 57 | 58.1 / 59.5 |
| NY AM 09:30-11:30 bull | 593 / 53 | 66.8 / 69.8 | 63.6 / 59.5 | 63.9 / 50 | 65.2 / 63.6 |
| NY AM 09:30-11:30 bear | 584 / 47 | 58.2 / 59.6 | 52.6 / 57.1 | 60.9 / 56.2 | 50.5 / 66.7 |

### 4.7 1h - run from the first BC after 09:30

Run ended before 16:00: 62.3% / 50.8%

| group | n | avg BCs | median BCs | 1 BC % | 2 % | 3 % | 4 % | 5+ % | median pts to extreme | avg pts to extreme | median pts to last BC close | avg NBCs in run | median run minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 756 / 61 | 2.7 / 3.1 | 2 / 2 | 36.9 / 36.1 | 23.4 / 18 | 14.7 / 13.1 | 9.1 / 14.8 | 15.9 / 18 | 75.6 / 106 | 118 / 165 | 36.1 / 53.2 | 3.2 / 3.3 | 300 / 300 |
| bull runs | 419 / 34 | 3 / 3.5 | 2 / 2.5 | 31.5 / 38.2 | 20.8 / 11.8 | 16.5 / 14.7 | 10.7 / 11.8 | 20.5 / 23.5 | 73.5 / 76.6 | 106 / 151 | 44.5 / 33.1 | 3.4 / 3.8 | 300 / 360 |
| bear runs * | 337 / 27 | 2.4 / 2.7 | 2 / 2 | 43.6 / 33.3 | 26.7 / 25.9 | 12.5 / 11.1 | 7.1 / 18.5 | 10.1 / 11.1 | 77.2 / 140 | 132 / 182 | 26.2 / 88 | 2.9 / 2.7 | 240 / 300 |
| run side = 10:00 candle lean | 640 / 54 | 2.7 / 3.2 | 2 / 2 | 37.7 / 35.2 | 22.2 / 18.5 | 14.7 / 13 | 9.7 / 13 | 15.8 / 20.4 | 78.4 / 108 | 119 / 169 | 36.6 / 53.6 | 3.1 / 3.5 | 270 / 360 |
| run side AGAINST 10:00 candle lean * | 116 / 7 | 2.8 / 2.3 | 2 / 2 | 32.8 / 42.9 | 30.2 / 14.3 | 14.7 / 14.3 | 6 / 28.6 | 16.4 / 0 | 64.9 / 88.8 | 111 / 135 | 33.4 / 13 | 3.6 / 2.1 | 300 / 240 |
| 10:00 candle BC+ * | 199 / 20 | 3.1 / 3.8 | 3 / 3 | 31.2 / 30 | 18.1 / 15 | 16.6 / 10 | 14.6 / 10 | 19.6 / 35 | 104 / 129 | 135 / 217 | 59.5 / 94.5 | 3.4 / 3.9 | 300 / 390 |
| 10:00 candle BC- * | 110 / 8 | 2.5 / 3.8 | 2 / 2 | 48.2 / 37.5 | 22.7 / 37.5 | 10 / 0 | 1.8 / 0 | 17.3 / 25 | 71.4 / 95.8 | 119 / 161 | 2.8 / 47.9 | 2.8 / 4.4 | 240 / 330 |
| 10:00 candle C2 * | 178 / 13 | 2.6 / 3.1 | 2 / 2 | 33.7 / 38.5 | 25.8 / 15.4 | 16.3 / 7.7 | 11.8 / 23.1 | 12.4 / 15.4 | 86.6 / 106 | 119 / 162 | 41.1 / 21.2 | 2.8 / 3.1 | 240 / 300 |
| 10:00 candle AFs * | 150 / 15 | 2.6 / 2.3 | 2 / 2 | 39.3 / 40 | 23.3 / 13.3 | 16.7 / 26.7 | 7.3 / 20 | 13.3 / 0 | 65.5 / 76.5 | 93.5 / 109 | 26.5 / 14.5 | 3.4 / 2.7 | 300 / 300 |
| 10:00 candle CI * | 25 / 0 | 2.6 / - | 2 / - | 32 / - | 40 / - | 8 / - | 4 / - | 16 / - | 59 / - | 122 / - | 20.8 / - | 3.4 / - | 300 / - |
| 10:00 candle S&D * | 94 / 5 | 2.7 / 2.2 | 2 / 2 | 39.4 / 40 | 26.6 / 20 | 11.7 / 20 | 5.3 / 20 | 17 / 0 | 64 / 156 | 114 / 139 | 22.8 / 101 | 3.2 / 1.6 | 300 / 180 |
| 10:00 BC+ / run WITH its lean * | 199 / 20 | 3.1 / 3.8 | 3 / 3 | 31.2 / 30 | 18.1 / 15 | 16.6 / 10 | 14.6 / 10 | 19.6 / 35 | 104 / 129 | 135 / 217 | 59.5 / 94.5 | 3.4 / 3.9 | 300 / 390 |
| 10:00 BC- / run WITH its lean * | 110 / 8 | 2.5 / 3.8 | 2 / 2 | 48.2 / 37.5 | 22.7 / 37.5 | 10 / 0 | 1.8 / 0 | 17.3 / 25 | 71.4 / 95.8 | 119 / 161 | 2.8 / 47.9 | 2.8 / 4.4 | 240 / 330 |
| 10:00 C2 / run WITH its lean * | 178 / 13 | 2.6 / 3.1 | 2 / 2 | 33.7 / 38.5 | 25.8 / 15.4 | 16.3 / 7.7 | 11.8 / 23.1 | 12.4 / 15.4 | 86.6 / 106 | 119 / 162 | 41.1 / 21.2 | 2.8 / 3.1 | 240 / 300 |
| 10:00 AFs / run WITH its lean * | 87 / 11 | 2.7 / 2.4 | 2 / 3 | 46 / 36.4 | 14.9 / 9.1 | 16.1 / 36.4 | 8 / 18.2 | 14.9 / 0 | 66 / 74.8 | 100 / 102 | 0 / 32.2 | 3.6 / 2.8 | 300 / 360 |
| 10:00 AFs / run AGAINST its lean * | 63 / 4 | 2.6 / 2 | 2 / 1.5 | 30.2 / 50 | 34.9 / 25 | 17.5 / 0 | 6.3 / 25 | 11.1 / 0 | 64 / 82.6 | 83.9 / 129 | 35 / 6.5 | 3.2 / 2.5 | 300 / 240 |
| 10:00 CI / run WITH its lean * | 16 / 0 | 2.2 / - | 2 / - | 37.5 / - | 37.5 / - | 12.5 / - | 6.2 / - | 6.2 / - | 69 / - | 145 / - | 23.8 / - | 2.8 / - | 240 / - |
| 10:00 CI / run AGAINST its lean * | 9 / 0 | 3.2 / - | 2 / - | 22.2 / - | 44.4 / - | 0 / - | 0 / - | 33.3 / - | 49.8 / - | 82.4 / - | 20.8 / - | 4.6 / - | 540 / - |
| 10:00 S&D / run WITH its lean * | 50 / 2 | 2.4 / 1.5 | 2 / 1.5 | 40 / 50 | 32 / 50 | 10 / 0 | 4 / 0 | 14 / 0 | 62.9 / 131 | 77.8 / 131 | 20.4 / 50.4 | 2.6 / 1.5 | 270 / 180 |
| 10:00 S&D / run AGAINST its lean * | 44 / 3 | 3 / 2.7 | 2 / 3 | 38.6 / 33.3 | 20.5 / 0 | 13.6 / 33.3 | 6.8 / 33.3 | 20.5 / 0 | 66.1 / 156 | 155 / 144 | 33.4 / 155 | 3.9 / 1.7 | 420 / 180 |

Chance of the next same-side BC:

| group | n | got 2nd BC % | 2nd -> 3rd % | 3rd -> 4th % | 4th -> 5th % |
|---|---|---|---|---|---|
| ALL | 756 / 61 | 63.1 / 63.9 | 62.9 / 71.8 | 63 / 71.4 | 63.5 / 55 |
| bull runs | 419 / 34 | 68.5 / 61.8 | 69.7 / 81 | 65.5 / 70.6 | 65.6 / 66.7 |
| bear runs * | 337 / 27 | 56.4 / 66.7 | 52.6 / 61.1 | 58 / 72.7 | 58.6 / 37.5 |
| run side = 10:00 candle lean | 640 / 54 | 62.3 / 64.8 | 64.4 / 71.4 | 63.4 / 72 | 62 / 61.1 |
| run side AGAINST 10:00 candle lean * | 116 / 7 | 67.2 / 57.1 | 55.1 / 75 | 60.5 / 66.7 | 73.1 / 0 |

### 4.8 1h - run from the first BC after 10:00

Run ended before 16:00: 51% / 37.7%

| group | n | avg BCs | median BCs | 1 BC % | 2 % | 3 % | 4 % | 5+ % | median pts to extreme | avg pts to extreme | median pts to last BC close | avg NBCs in run | median run minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 743 / 61 | 2.7 / 3 | 2 / 2 | 36.6 / 37.7 | 24.8 / 13.1 | 15.3 / 18 | 7 / 16.4 | 16.3 / 14.8 | 64.8 / 98.5 | 106 / 145 | 29.5 / 53.2 | 3.2 / 3.3 | 300 / 360 |
| bull runs | 425 / 30 | 3 / 3.8 | 2 / 3 | 30.4 / 26.7 | 23.3 / 3.3 | 17.9 / 26.7 | 9.6 / 20 | 18.8 / 23.3 | 60.8 / 118 | 91.6 / 151 | 36.8 / 91.4 | 3.5 / 4.3 | 360 / 540 |
| bear runs | 318 / 31 | 2.4 / 2.2 | 2 / 2 | 45 / 48.4 | 26.7 / 22.6 | 11.9 / 9.7 | 3.5 / 12.9 | 12.9 / 6.5 | 72.4 / 84.2 | 126 / 140 | 14.2 / 13 | 2.9 / 2.3 | 240 / 240 |
| run side = 10:00 candle lean | 458 / 40 | 2.7 / 3.4 | 2 / 3 | 37.3 / 32.5 | 23.1 / 12.5 | 15.5 / 22.5 | 7.9 / 12.5 | 16.2 / 20 | 67 / 103 | 104 / 157 | 29.9 / 70.1 | 3.2 / 3.4 | 300 / 360 |
| run side AGAINST 10:00 candle lean * | 285 / 21 | 2.7 / 2.2 | 2 / 2 | 35.4 / 47.6 | 27.4 / 14.3 | 15.1 / 9.5 | 5.6 / 23.8 | 16.5 / 4.8 | 59 / 76.5 | 109 / 122 | 29.5 / 13 | 3.3 / 3 | 300 / 240 |
| 10:00 candle BC+ * | 193 / 20 | 2.9 / 3.5 | 2 / 3 | 28 / 30 | 25.4 / 15 | 19.7 / 10 | 7.3 / 20 | 19.7 / 25 | 79.8 / 101 | 122 / 169 | 48.5 / 66 | 3.4 / 3.6 | 300 / 450 |
| 10:00 candle BC- * | 107 / 8 | 2.8 / 3.8 | 2 / 2 | 41.1 / 50 | 20.6 / 0 | 11.2 / 12.5 | 8.4 / 12.5 | 18.7 / 25 | 60.2 / 138 | 109 / 154 | 26.2 / 71.1 | 3.3 / 4.6 | 300 / 480 |
| 10:00 candle C2 * | 174 / 13 | 2.5 / 2.9 | 2 / 2 | 40.2 / 38.5 | 24.7 / 15.4 | 14.9 / 23.1 | 6.9 / 7.7 | 13.2 / 15.4 | 59.4 / 89 | 91.3 / 148 | 21.4 / 72.2 | 2.9 / 3.1 | 240 / 360 |
| 10:00 candle AFs * | 150 / 15 | 2.6 / 2.3 | 2 / 2 | 39.3 / 40 | 23.3 / 13.3 | 16.7 / 26.7 | 7.3 / 20 | 13.3 / 0 | 65.5 / 76.5 | 93.5 / 109 | 26.5 / 14.5 | 3.4 / 2.7 | 300 / 300 |
| 10:00 candle CI * | 25 / 0 | 2.6 / - | 2 / - | 32 / - | 40 / - | 8 / - | 4 / - | 16 / - | 59 / - | 122 / - | 20.8 / - | 3.4 / - | 300 / - |
| 10:00 candle S&D * | 94 / 5 | 2.7 / 2.2 | 2 / 2 | 39.4 / 40 | 26.6 / 20 | 11.7 / 20 | 5.3 / 20 | 17 / 0 | 64 / 156 | 114 / 139 | 22.8 / 101 | 3.2 / 1.6 | 300 / 180 |
| 10:00 BC+ / run WITH its lean * | 134 / 14 | 3 / 3.9 | 2 / 3.5 | 26.9 / 21.4 | 24.6 / 14.3 | 20.1 / 14.3 | 7.5 / 21.4 | 20.9 / 28.6 | 88.4 / 101 | 118 / 188 | 54.1 / 78.2 | 3.6 / 3.7 | 330 / 450 |
| 10:00 BC+ / run AGAINST its lean * | 59 / 6 | 2.8 / 2.3 | 2 / 1.5 | 30.5 / 50 | 27.1 / 16.7 | 18.6 / 0 | 6.8 / 16.7 | 16.9 / 16.7 | 65.5 / 90.4 | 130 / 125 | 43.8 / 19.9 | 2.9 / 3.5 | 300 / 510 |
| 10:00 BC- / run WITH its lean * | 56 / 5 | 2.9 / 4.4 | 2 / 1 | 42.9 / 60 | 19.6 / 0 | 3.6 / 0 | 12.5 / 0 | 21.4 / 40 | 66.2 / 104 | 108 / 152 | 31.6 / 0 | 3.5 / 5.4 | 300 / 420 |
| 10:00 BC- / run AGAINST its lean * | 51 / 3 | 2.7 / 2.7 | 2 / 3 | 39.2 / 33.3 | 21.6 / 0 | 19.6 / 33.3 | 3.9 / 33.3 | 15.7 / 0 | 57.5 / 172 | 110 / 156 | 19.2 / 142 | 3.1 / 3.3 | 300 / 540 |
| 10:00 C2 / run WITH its lean * | 115 / 8 | 2.4 / 3.5 | 2 / 3 | 39.1 / 25 | 23.5 / 12.5 | 18.3 / 37.5 | 7.8 / 0 | 11.3 / 25 | 61.5 / 186 | 95.5 / 190 | 25.8 / 150 | 2.6 / 2.8 | 240 / 390 |
| 10:00 C2 / run AGAINST its lean * | 59 / 5 | 2.5 / 1.8 | 2 / 1 | 42.4 / 60 | 27.1 / 20 | 8.5 / 0 | 5.1 / 20 | 16.9 / 0 | 49.8 / 50.5 | 83 / 81.8 | 12.5 / 0 | 3.3 / 3.6 | 300 / 240 |
| 10:00 AFs / run WITH its lean * | 87 / 11 | 2.7 / 2.4 | 2 / 3 | 46 / 36.4 | 14.9 / 9.1 | 16.1 / 36.4 | 8 / 18.2 | 14.9 / 0 | 66 / 74.8 | 100 / 102 | 0 / 32.2 | 3.6 / 2.8 | 300 / 360 |
| 10:00 AFs / run AGAINST its lean * | 63 / 4 | 2.6 / 2 | 2 / 1.5 | 30.2 / 50 | 34.9 / 25 | 17.5 / 0 | 6.3 / 25 | 11.1 / 0 | 64 / 82.6 | 83.9 / 129 | 35 / 6.5 | 3.2 / 2.5 | 300 / 240 |
| 10:00 CI / run WITH its lean * | 16 / 0 | 2.2 / - | 2 / - | 37.5 / - | 37.5 / - | 12.5 / - | 6.2 / - | 6.2 / - | 69 / - | 145 / - | 23.8 / - | 2.8 / - | 240 / - |
| 10:00 CI / run AGAINST its lean * | 9 / 0 | 3.2 / - | 2 / - | 22.2 / - | 44.4 / - | 0 / - | 0 / - | 33.3 / - | 49.8 / - | 82.4 / - | 20.8 / - | 4.6 / - | 540 / - |
| 10:00 S&D / run WITH its lean * | 50 / 2 | 2.4 / 1.5 | 2 / 1.5 | 40 / 50 | 32 / 50 | 10 / 0 | 4 / 0 | 14 / 0 | 62.9 / 131 | 77.8 / 131 | 20.4 / 50.4 | 2.6 / 1.5 | 270 / 180 |
| 10:00 S&D / run AGAINST its lean * | 44 / 3 | 3 / 2.7 | 2 / 3 | 38.6 / 33.3 | 20.5 / 0 | 13.6 / 33.3 | 6.8 / 33.3 | 20.5 / 0 | 66.1 / 156 | 155 / 144 | 33.4 / 155 | 3.9 / 1.7 | 420 / 180 |

Chance of the next same-side BC:

| group | n | got 2nd BC % | 2nd -> 3rd % | 3rd -> 4th % | 4th -> 5th % |
|---|---|---|---|---|---|
| ALL | 743 / 61 | 63.4 / 62.3 | 60.9 / 78.9 | 60.3 / 63.3 | 69.9 / 47.4 |
| bull runs | 425 / 30 | 69.6 / 73.3 | 66.6 / 95.5 | 61.4 / 61.9 | 66.1 / 53.8 |
| bear runs | 318 / 31 | 55 / 51.6 | 51.4 / 56.2 | 57.8 / 66.7 | 78.8 / 33.3 |
| run side = 10:00 candle lean | 458 / 40 | 62.7 / 67.5 | 63.1 / 81.5 | 60.8 / 59.1 | 67.3 / 61.5 |
| run side AGAINST 10:00 candle lean * | 285 / 21 | 64.6 / 52.4 | 57.6 / 72.7 | 59.4 / 75 | 74.6 / 16.7 |

### 4.9 1h - ALL runs by the hour they START (whole data, every run)

| start time | n | avg BCs | median BCs | 1 BC % | 2 % | 3 % | 4 % | 5+ % | median pts to extreme | avg pts to extreme | median pts to last BC close | avg NBCs in run | median run minutes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Asia 18:00-02:00 | 1145 / 99 | 2.5 / 2.7 | 2 / 2 | 39.7 / 37.4 | 24.5 / 20.2 | 16.2 / 18.2 | 8 / 10.1 | 11.6 / 14.1 | 25.8 / 66.8 | 56 / 118 | 10.2 / 34.2 | 2.5 / 2.5 | 240 / 240 |
| London 02:00-08:00 | 930 / 67 | 2.5 / 2.4 | 2 / 2 | 39.5 / 40.3 | 24.9 / 31.3 | 15.6 / 13.4 | 7.7 / 1.5 | 12.3 / 13.4 | 40.8 / 77.5 | 91.6 / 152 | 17 / 40.2 | 2.6 / 2.6 | 240 / 180 |
| pre 08:00-09:30 * | 384 / 28 | 2.6 / 3.6 | 2 / 2 | 41.9 / 32.1 | 19.3 / 21.4 | 14.3 / 10.7 | 9.1 / 14.3 | 15.4 / 21.4 | 83.2 / 145 | 122 / 194 | 34.9 / 71 | 2.7 / 4.3 | 240 / 390 |
| NY AM 09:30-11:30 * | 262 / 18 | 2.6 / 2.2 | 2 / 1.5 | 40.5 / 50 | 24.4 / 11.1 | 14.9 / 16.7 | 4.2 / 16.7 | 16 / 5.6 | 64.1 / 70.1 | 111 / 103 | 22.4 / 6.5 | 3.2 / 3.2 | 300 / 240 |
| midday 11:30-14:00 * | 264 / 18 | 2.6 / 3.1 | 2 / 2 | 40.9 / 44.4 | 24.2 / 11.1 | 15.9 / 5.6 | 4.2 / 11.1 | 14.8 / 27.8 | 55.5 / 117 | 93.6 / 159 | 22.2 / 34.8 | 3.2 / 3.6 | 360 / 330 |
| NY PM 14:00-16:00 * | 280 / 22 | 2.5 / 2.2 | 2 / 2 | 37.9 / 40.9 | 27.9 / 22.7 | 14.3 / 22.7 | 8.2 / 4.5 | 11.8 / 9.1 | 43.2 / 55 | 69.5 / 111 | 16.2 / 13.1 | 3 / 2.7 | 360 / 360 |
| after 16:00-18:00 * | 70 / 4 | 2.7 / 1.5 | 2 / 1.5 | 44.3 / 50 | 24.3 / 50 | 11.4 / 0 | 4.3 / 0 | 15.7 / 0 | 37.1 / 56.2 | 60.7 / 64.9 | 6.6 / 6.1 | 3 / 0.8 | 390 / 270 |
| ALL OTHER HOURS | 3073 / 238 | 2.5 / 2.7 | 2 / 2 | 40 / 38.7 | 24.2 / 23.5 | 15.5 / 15.1 | 7.7 / 7.6 | 12.7 / 15.1 | 39 / 82.8 | 79.6 / 138 | 13.5 / 35.9 | 2.7 / 2.8 | 240 / 240 |
| ALL RUNS | 3335 / 256 | 2.5 / 2.6 | 2 / 2 | 40 / 39.5 | 24.3 / 22.7 | 15.4 / 15.2 | 7.4 / 8.2 | 12.9 / 14.5 | 41 / 78.9 | 82 / 136 | 13.8 / 33.2 | 2.7 / 2.8 | 240 / 240 |
| NY AM 09:30-11:30 bull * | 137 / 10 | 2.9 / 2.7 | 2 / 3 | 35 / 30 | 21.9 / 10 | 17.5 / 30 | 5.1 / 20 | 20.4 / 10 | 64 / 96.2 | 95.9 / 123 | 37.8 / 70.6 | 3.4 / 4.2 | 300 / 540 |
| NY AM 09:30-11:30 bear * | 125 / 8 | 2.2 / 1.5 | 2 / 1 | 46.4 / 75 | 27.2 / 12.5 | 12 / 0 | 3.2 / 12.5 | 11.2 / 0 | 64.5 / 64.9 | 127 / 77.2 | 7 / 0 | 3 / 2 | 240 / 210 |

| start time | n | got 2nd BC % | 2nd -> 3rd % | 3rd -> 4th % | 4th -> 5th % |
|---|---|---|---|---|---|
| Asia 18:00-02:00 | 1145 / 99 | 60.3 / 62.6 | 59.4 / 67.7 | 54.9 / 57.1 | 59.1 / 58.3 |
| London 02:00-08:00 | 930 / 67 | 60.5 / 59.7 | 58.8 / 47.5 | 56.2 / 52.6 | 61.3 / 90 |
| pre 08:00-09:30 * | 384 / 28 | 58.1 / 67.9 | 66.8 / 68.4 | 63.1 / 76.9 | 62.8 / 60 |
| NY AM 09:30-11:30 * | 262 / 18 | 59.5 / 50 | 59 / 77.8 | 57.6 / 57.1 | 79.2 / 25 |
| midday 11:30-14:00 * | 264 / 18 | 59.1 / 55.6 | 59 / 80 | 54.3 / 87.5 | 78 / 71.4 |
| NY PM 14:00-16:00 * | 280 / 22 | 62.1 / 59.1 | 55.2 / 61.5 | 58.3 / 37.5 | 58.9 / 66.7 |
| after 16:00-18:00 * | 70 / 4 | 55.7 / 50 | 56.4 / 0 | 63.6 / - | 78.6 / - |
| ALL OTHER HOURS | 3073 / 238 | 60 / 61.3 | 59.6 / 61.6 | 56.8 / 60 | 62.2 / 66.7 |
| ALL RUNS | 3335 / 256 | 60 / 60.5 | 59.6 / 62.6 | 56.9 / 59.8 | 63.6 / 63.8 |
| NY AM 09:30-11:30 bull * | 137 / 10 | 65 / 70 | 66.3 / 85.7 | 59.3 / 50 | 80 / 33.3 |
| NY AM 09:30-11:30 bear * | 125 / 8 | 53.6 / 25 | 49.3 / 50 | 54.5 / 100 | 77.8 / 0 |

## 5. Open UPG gaps on the OTHER side of the target (10:00 to 11:30)

Question: when the 10:00 candle leans one way, is there still an open (never touched) UPG gap on the other side, and does price go to that gap before the target?

- **Gap** = a 3-candle UPG gap (5m, or the same timeframe as the candle) made since 18:00 and not touched before 10:00, fully on the other side of the 10:00 close (below price for a bull lean, above for a bear lean). The closest one counts.
- **Target (TGT)** = the 10:00 candle lean-side extreme. Everything is checked on 1m bars from 10:00 to 11:30.
- Almost all of these gaps point the SAME way as the lean (a bull gap below price on a bull-lean day): an open gap on the wrong side is rare.

**What we found:**
- **Yes, there is usually one.** An open gap sits on the other side 56-78% (2022-25) of days. It is about 36-46 pts away in 2022-25 and about 83 pts in 2026 (bigger moves).
- **It does NOT stop the target.** The target gets hit by 11:30 just as often with the gap as without it.
- **Strong candles ignore it.** After a BC+ or C2 candle, price goes to the gap BEFORE the target only 5% (5m), 12% (15m), 22% (1h), 19% (4h) of the time in 2022-25.
- **Weak candles go to the gap first much more often.** After BC-, AFs, CI or S&D: gap first 15% (5m), 32% (15m), 45% (1h), 52% (4h). On 1h and 4h, a weak 10:00 candle is about a coin flip between the gap and the target. The gap is a good place to wait for those days.
- **After price reaches the gap first, the target still comes by 11:30 only 31-58% of the time.** Do not count on both.

| TF | type | n | gap there % | TGT by 11:30 with gap % | TGT by 11:30 no gap % | gap BEFORE TGT % | TGT after the gap % | gap distance pts |
|---|---|---|---|---|---|---|---|---|
| 5m | ALL | 763 / 61 | 55.7 / 60.7 | 94.6 / 94.6 | 92 / 91.7 | 11.5 / 8.1 | 55.1 / 33.3 | 46.25 / 85.75 |
| 5m | BC+/C2 | 227 / 24 | 59 / 70.8 | 97 / 100 | 95.7 / 100 | 4.5 / 5.9 | 33.3 / 100 | 52 / 85.75 |
| 5m | other | 536 / 37 | 54.3 / 54.1 | 93.5 / 90 | 90.6 / 88.2 | 14.8 / 10 | 58.1 / 0 | 42.75 / 90.62 |
| 15m | ALL | 763 / 61 | 67.8 / 75.4 | 89.2 / 84.8 | 86.6 / 80 | 24.2 / 23.9 | 57.6 / 36.4 | 36.5 / 83.12 |
| 15m | BC+/C2 | 227 / 28 | 87.7 / 92.9 | 96 / 100 | 96.4 / 100 | 11.6 / 7.7 | 65.2 / 100 | 35.5 / 79.38 |
| 15m | other | 536 / 33 | 59.3 / 60.6 | 84.9 / 65 | 85.3 / 76.9 | 32.1 / 45 | 55.9 / 22.2 | 36.5 / 86.38 |
| 1h | ALL | 763 / 61 | 72.7 / 78.7 | 78.6 / 79.2 | 74.5 / 69.2 | 31.5 / 29.2 | 37.7 / 35.7 | 39.25 / 82.12 |
| 1h | BC+/C2 | 377 / 33 | 86.2 / 87.9 | 87.4 / 93.1 | 86.5 / 100 | 22.2 / 17.2 | 44.4 / 60 | 39.25 / 74.25 |
| 1h | other | 386 / 28 | 59.6 / 67.9 | 66.1 / 57.9 | 70.5 / 55.6 | 44.8 / 47.4 | 33 / 22.2 | 39 / 105 |
| 4h | ALL | 763 / 61 | 77.6 / 85.2 | 72.8 / 73.1 | 65.5 / 66.7 | 34.3 / 28.8 | 31 / 33.3 | 40.25 / 82.25 |
| 4h | BC+/C2 | 357 / 31 | 88.8 / 96.8 | 85.5 / 83.3 | 70 / 100 | 18.9 / 20 | 35 / 33.3 | 43.75 / 82.12 |
| 4h | other | 406 / 30 | 67.7 / 73.3 | 58.2 / 59.1 | 64.1 / 62.5 | 52 / 40.9 | 29.4 / 33.3 | 38.25 / 82.25 |

"other" = BC-, AFs, CI and S&D. 2026 rows have few cases (gap-first counts of 1-15): treat them as a guess.

## 6. From the first BC after 10:00 until the opposite candle or 11:30

Start = the first body close (bull or bear) of that timeframe at or after 10:00. We follow it until an **opposite candle** or 11:30 (your stop time). Three ways to call the opposite candle:
- **opp BC** = the first body close the other way.
- **close past BC open** = a close below the open of the LAST bull BC (bear run: above the open of the last bear BC).
- **close past BC low** = a close below the low of the LAST bull BC (bear run: above its high).

Counts: **same BCs** = body closes our way, the first one included. **NBCs** = no-body-close candles before the end. **MFE** = the most points in our favour from the start close. **End pts** = points at the opposite candle close (or 11:30). **Alive** = no opposite candle before 11:30.

**What we found:**
- **The run is short on every timeframe: median 2 same-side BCs** (the first one counts). 1m runs end in about 5-6 minutes, 5m in 25-35 minutes, 15m in about 60-75 minutes.
- **NBCs: about 3 on 5m and 1m, about 2 on 15m** before the opposite candle. A run is BC, NBC, NBC, BC, NBC… then the other side closes.
- **Points our way (MFE): 5m median 30-36 pts (75th pct 61-74), 15m median 36 pts (75th pct 67-70) in 2022-25. In 2026: 5m 36-46, 15m 56 pts.** 1m only 13-15 pts.
- **But waiting for the opposite candle gives it all back.** End pts median is NEGATIVE (5m about -8 to -10, 15m -2 to -5 in 2022-25) and the average is about 0. The move is there; the exit on the opposite candle is too late. Take points, not the full run.
- **Which opposite rule?** "Close past BC LOW" holds longest (5m: 35 min, 11% still alive at 11:30; 15m: 62% alive) and gives the most MFE. "Close past BC open" and "opp BC" end about the same time.
- **The 4H lean does not help the run.** With or against the 4H 06-10 lean, the numbers are almost the same.
- **How often the run gives X points (5m, close past BC low, 2022-25 / 2026):** 10 pts 81 / 85%, 20 pts 68 / 80%, 30 pts 56 / 67%, 50 pts 38 / 48%, 80 pts 22 / 36%. 15m: 20 pts 70 / 87%, 30 pts 59 / 73%, 50 pts 36 / 57%.

### 6.1 1m

| opposite rule | group | n | same BCs median / avg | NBCs avg | MFE median pts | MFE 75th pct | end pts avg | end pts > 0 % | alive at 11:30 % | minutes median |
|---|---|---|---|---|---|---|---|---|---|---|
| opp BC | all | 763 / 61 | 2, 2.44 / 2, 2.26 | 2.9 / 2.79 | 14 / 16 | 31.1 / 39.5 | -1.9 / -7.6 | 35 / 27.9 | 0 / 0 | 5 / 6 |
| opp BC | with 4H lean | 432 / 33 | 2, 2.52 / 1, 2.09 | 3.02 / 2.39 | 14.2 / 10.2 | 33.3 / 26.5 | -1.2 / -9.1 | 35.9 / 27.3 | 0 / 0 | 5 / 5 |
| opp BC | against 4H lean * | 331 / 28 | 2, 2.33 / 2, 2.46 | 2.74 / 3.25 | 13.2 / 26.2 | 28.5 / 45.4 | -2.9 / -5.9 | 33.8 / 28.6 | 0 / 0 | 5 / 6 |
| opp BC | with 4H BC+/C2 * | 212 / 17 | 2, 2.59 / 1, 2.06 | 3.11 / 2.47 | 14.5 / 10 | 34.1 / 44 | -0.9 / -5.5 | 36.8 / 29.4 | 0 / 0 | 5 / 5 |
| close past BC open | all | 763 / 61 | 2, 2.51 / 2, 2.48 | 2.8 / 2.64 | 13.2 / 14.8 | 31.9 / 44 | -1.4 / -1.8 | 34.1 / 32.8 | 0 / 0 | 5 / 5 |
| close past BC open | with 4H lean | 432 / 33 | 2, 2.48 / 1, 2.15 | 2.74 / 1.88 | 13.8 / 10 | 32.9 / 26.5 | -1.3 / -6.8 | 35.2 / 27.3 | 0 / 0 | 5 / 4 |
| close past BC open | against 4H lean * | 331 / 28 | 2, 2.55 / 2, 2.86 | 2.86 / 3.54 | 13 / 26.2 | 30.4 / 49.1 | -1.7 / 4 | 32.6 / 39.3 | 0 / 0 | 5 / 6 |
| close past BC open | with 4H BC+/C2 * | 212 / 17 | 2, 2.5 / 1, 1.94 | 2.73 / 1.94 | 13.1 / 5.5 | 35.1 / 44 | -1.4 / -4 | 34.9 / 29.4 | 0 / 0 | 5 / 4 |
| close past BC low | all | 763 / 61 | 2, 2.93 / 2, 2.72 | 3.84 / 3.67 | 15.2 / 17.8 | 36 / 48.8 | -1.9 / -6.3 | 35.8 / 32.8 | 0 / 0 | 6 / 6 |
| close past BC low | with 4H lean | 432 / 33 | 2, 2.9 / 1, 2.39 | 3.76 / 2.94 | 15.2 / 10.8 | 37.2 / 40.2 | -1.2 / -11 | 36.8 / 30.3 | 0 / 0 | 6 / 6 |
| close past BC low | against 4H lean * | 331 / 28 | 2, 2.96 / 3, 3.11 | 3.94 / 4.54 | 15.2 / 31 | 32.4 / 53.2 | -2.7 / -0.7 | 34.4 / 35.7 | 0 / 0 | 7 / 7.5 |
| close past BC low | with 4H BC+/C2 * | 212 / 17 | 2, 2.85 / 1, 2.35 | 3.65 / 3.41 | 15.5 / 10 | 37 / 55 | -2.4 / -7.6 | 35.8 / 41.2 | 0 / 0 | 6 / 6 |

### 6.2 5m

| opposite rule | group | n | same BCs median / avg | NBCs avg | MFE median pts | MFE 75th pct | end pts avg | end pts > 0 % | alive at 11:30 % | minutes median |
|---|---|---|---|---|---|---|---|---|---|---|
| opp BC | all | 763 / 61 | 2, 2.58 / 2, 2.3 | 2.91 / 2.75 | 29.8 / 36.5 | 63 / 78.2 | -0.2 / -1.9 | 38.4 / 37.7 | 3.5 / 4.9 | 25 / 25 |
| opp BC | with 4H lean | 413 / 30 | 2, 2.58 / 2, 2.17 | 2.86 / 2.67 | 29.2 / 37.8 | 65 / 78.2 | -0.3 / -7.1 | 38.5 / 43.3 | 3.4 / 0 | 25 / 25 |
| opp BC | against 4H lean | 350 / 31 | 2, 2.57 / 2, 2.42 | 2.98 / 2.84 | 31.6 / 35.5 | 61.9 / 85.2 | 0.1 / 3.1 | 38.3 / 32.3 | 3.7 / 9.7 | 25 / 25 |
| opp BC | with 4H BC+/C2 * | 201 / 19 | 2, 2.37 / 2, 2.05 | 2.68 / 2.58 | 28.5 / 32.2 | 60.8 / 78.2 | -4.6 / -11.9 | 37.8 / 36.8 | 3 / 0 | 25 / 25 |
| close past BC open | all | 763 / 61 | 2, 2.65 / 2, 2.38 | 2.77 / 2.59 | 30.8 / 35.5 | 61.2 / 82.5 | 0 / -4 | 38.3 / 27.9 | 5 / 6.6 | 25 / 20 |
| close past BC open | with 4H lean | 413 / 30 | 2, 2.61 / 2, 2.6 | 2.78 / 2.87 | 29.2 / 37.5 | 62.8 / 85.2 | -1.8 / 1.1 | 36.8 / 33.3 | 5.1 / 6.7 | 25 / 30 |
| close past BC open | against 4H lean | 350 / 31 | 2, 2.71 / 2, 2.16 | 2.75 / 2.32 | 32.6 / 35 | 59.8 / 70.2 | 2.2 / -9.1 | 40 / 22.6 | 4.9 / 6.5 | 25 / 20 |
| close past BC open | with 4H BC+/C2 * | 201 / 19 | 2, 2.38 / 1, 2.21 | 2.73 / 2.42 | 28 / 29.5 | 58 / 85 | -8 / -2 | 33.8 / 26.3 | 4.5 / 5.3 | 25 / 25 |
| close past BC low | all | 763 / 61 | 2, 3.07 / 2, 2.98 | 3.85 / 4.03 | 35.8 / 45.5 | 73.8 / 103.2 | 1.3 / 3.3 | 40.8 / 37.7 | 11.4 / 16.4 | 35 / 35 |
| close past BC low | with 4H lean | 413 / 30 | 2, 3 / 2, 3 | 3.77 / 4.03 | 33.2 / 56.9 | 73 / 88.3 | -0.7 / -6.1 | 39.7 / 40 | 11.1 / 16.7 | 35 / 37.5 |
| close past BC low | against 4H lean | 350 / 31 | 3, 3.15 / 2, 2.97 | 3.94 / 4.03 | 38.4 / 42.8 | 73.8 / 139.8 | 3.7 / 12.4 | 42 / 35.5 | 11.7 / 16.1 | 35 / 35 |
| close past BC low | with 4H BC+/C2 * | 201 / 19 | 2, 2.79 / 2, 2.42 | 3.75 / 3.42 | 31 / 32.2 | 72.5 / 85 | -6.5 / -13.8 | 37.8 / 31.6 | 11.9 / 15.8 | 30 / 30 |

### 6.3 15m

| opposite rule | group | n | same BCs median / avg | NBCs avg | MFE median pts | MFE 75th pct | end pts avg | end pts > 0 % | alive at 11:30 % | minutes median |
|---|---|---|---|---|---|---|---|---|---|---|
| opp BC | all | 752 / 60 | 2, 1.98 / 2, 1.92 | 1.74 / 1.58 | 36 / 55.8 | 69.5 / 99.4 | -0.5 / -2.1 | 46.1 / 41.7 | 46.9 / 46.7 | 60 / 60 |
| opp BC | with 4H lean | 435 / 32 | 2, 1.99 / 2, 1.97 | 1.72 / 1.78 | 35.8 / 52.2 | 69.4 / 88.9 | -1.8 / -0.2 | 47.1 / 37.5 | 45.3 / 50 | 60 / 60 |
| opp BC | against 4H lean * | 317 / 28 | 2, 1.97 / 2, 1.86 | 1.77 / 1.36 | 36 / 57.9 | 69.8 / 113.2 | 1.3 / -4.2 | 44.8 / 46.4 | 49.2 / 42.9 | 60 / 60 |
| opp BC | with 4H BC+/C2 * | 217 / 18 | 2, 1.9 / 2, 1.94 | 1.74 / 1.72 | 34.5 / 54.2 | 62 / 96.4 | -7 / -2.1 | 44.2 / 22.2 | 41.9 / 50 | 60 / 60 |
| close past BC open | all | 752 / 60 | 2, 1.98 / 2, 1.98 | 1.57 / 1.43 | 35.4 / 55.8 | 66.8 / 107 | -0 / 4.6 | 44.9 / 45 | 49.6 / 51.7 | 60 / 60 |
| close past BC open | with 4H lean | 435 / 32 | 2, 1.97 / 2, 1.94 | 1.55 / 1.53 | 35.2 / 44.8 | 66.6 / 88.9 | -2.3 / 4.7 | 45.3 / 37.5 | 48.5 / 43.8 | 60 / 60 |
| close past BC open | against 4H lean * | 317 / 28 | 2, 1.98 / 2, 2.04 | 1.6 / 1.32 | 35.5 / 57.9 | 66.8 / 113.2 | 3 / 4.6 | 44.5 / 53.6 | 51.1 / 60.7 | 60 / 60 |
| close past BC open | with 4H BC+/C2 * | 217 / 18 | 2, 1.9 / 2, 1.94 | 1.54 / 1.56 | 34.8 / 49.5 | 60.8 / 102.9 | -6.3 / 2.4 | 43.8 / 33.3 | 47 / 44.4 | 60 / 60 |
| close past BC low | all | 752 / 60 | 2, 2.02 / 2, 2.02 | 1.86 / 1.75 | 36.2 / 55.8 | 69.3 / 107 | -0.3 / 2.3 | 47.2 / 48.3 | 62.5 / 63.3 | 75 / 60 |
| close past BC low | with 4H lean | 435 / 32 | 2, 2.03 / 2, 2 | 1.85 / 2.03 | 36.2 / 52.2 | 69.5 / 88.9 | -2 / 2.5 | 48.3 / 43.8 | 61.6 / 62.5 | 75 / 75 |
| close past BC low | against 4H lean * | 317 / 28 | 2, 2.01 / 2, 2.04 | 1.88 / 1.43 | 36 / 57.9 | 67 / 113.2 | 2.1 / 2.1 | 45.7 / 53.6 | 63.7 / 64.3 | 75 / 60 |
| close past BC low | with 4H BC+/C2 * | 217 / 18 | 2, 1.95 / 2, 2 | 1.84 / 2.11 | 35.5 / 54.2 | 63 / 102.9 | -8.7 / 2.9 | 46.1 / 33.3 | 57.6 / 66.7 | 75 / 75 |

## 7. Fixed 50 pt stop at 1:2 on that first BC (your check)

Entry at the close of the first 5m / 15m BC at or after 10:00, in its direction. Stop 50 pts, target 100 pts, out at 11:30 if neither. 1 pt cost.

| TF | group | n | WR = win rate % | avg RR | PF = profit factor | t-score |
|---|---|---|---|---|---|---|
| 5m | all | 763 / 61 | 46 / 36.1 | 0.061 / -0.089 | 1.13 / 0.86 | 1.47 / -0.53 |
| 5m | with 4H lean | 413 / 30 | 47.2 / 36.7 | 0.081 / -0.119 | 1.17 / 0.82 | 1.43 / -0.51 |
| 5m | against 4H lean | 350 / 31 | 44.6 / 35.5 | 0.037 / -0.059 | 1.08 / 0.91 | 0.61 / -0.25 |
| 5m | first BC is BC+ | 414 / 37 | 47.1 / 35.1 | 0.088 / -0.141 | 1.19 / 0.78 | 1.55 / -0.68 |
| 5m | with 4H BC+/C2 | 201 / 19 | 44.8 / 31.6 | 0.052 / -0.212 | 1.11 / 0.7 | 0.65 / -0.72 |
| 15m | all | 743 / 59 | 44.8 / 42.4 | 0.023 / 0.048 | 1.05 / 1.09 | 0.59 / 0.3 |
| 15m | with 4H lean | 430 / 32 | 45.6 / 37.5 | 0.013 / -0.131 | 1.03 / 0.76 | 0.25 / -0.65 |
| 15m | against 4H lean | 313 / 27 | 43.8 / 48.1 | 0.037 / 0.26 | 1.09 / 1.53 | 0.61 / 0.99 |
| 15m | first BC is BC+ | 454 / 34 | 46.9 / 50 | 0.026 / 0.289 | 1.06 / 1.72 | 0.54 / 1.33 |
| 15m | with 4H BC+/C2 | 215 / 18 | 44.2 / 27.8 | -0.005 / -0.191 | 0.99 / 0.7 | -0.07 / -0.65 |

- **No edge.** Best 2022-25 row: 5m first BC is BC+ at +0.09 avg RR, t 1.55 (under 2 = could be luck), and it is negative in 2026. The first BC after 10:00 alone is not a trade. Use it as the start of the count, not as an entry.

## Files

- `results.json` = every table (more columns than this report).
- `common.py` (loader, classifier), `verify.py` (time and classifier checks), `q1.py` `q2.py` `q3.py` `q4.py` (one per question), `q56.py` + `q5sum.py` + `q6sum.py` (parts 5-6), `q7.py` (part 7), `build_report.py` (this report).
- `q1_*.csv`, `q2_*_gaps.csv`, `q3_*.csv`, `q4_*_firstBC.csv` = one row per case, if you want to check any day by hand.
