# MMM PRO FVA · HTF level → LTF reversal box · full test results

> Renamed Oct 28 2026: MMM PRO f → **MMM PRO FVA** (Fair Value Area OrderFlow); strategy codes F.M# → **FVA.M#**.

Tested Oct 2026. Data: **NQ 1m Dec 2022 – Dec 2025** (2022–25, 3 years) → **MNQ 1m Mar–May + Sep–Oct 2026** (2026, ~3 months). Results sheet: https://claude.ai/artifact/9rUap4818RCfZBqKua2cgh

## What was tested

- **HTF levels (first touch only):** MMM PRO FVA boxes on M15 / H1 / H4 (T1, T#, P#, R#, internal, CDL, CDS, LD, SD, Bu/Be LEZ) · UPG gaps M15 / H1 / H4 / D / W · daily, RTH and weekly opening gaps · PDH / PDL / PD close · PWH / PWL · prior H4 high / low · Asia, London, London OR, pre-open, Globex/ON, NY AM OR15 / OR30, NY AM session, NY PM OR highs and lows · daily 18:00, midnight, 9:30, weekly and H4 opens.
- **Direction:** bull level / support touched from above → long; bear level / resistance touched from below → short. Lines: side = where price came from.
- **LTF reversal box (1m and 5m):** the first MMM PRO FVA turn box of the trade direction printed after the touch (within 1 hour) whose low/high reached the level.
- **Entries:** M1 your model (proper retest, not the break candle → 2nd BC closes outside the box → next open), split into A touch candle = BC, B touch then BC, C close inside then BC, and PRO FVA type 1 immediate / 2 after NBC / 3 after opposite BC · M2 no pullback, 2nd BC · M3 limit at the box edge · M4 break candle · M5 GMC gap limit.
- **Every entry × every stop × every exit:** stops 20 / 30 / 50 / box edge (20–50) · close past the box = out (on / off) · targets 1:2, 1:3, 1:5, 1:10, runner · trails none, BE after 1 BC, BE after 2 BC, under each BC, after the 1st opposite candle. Session rule: at the next session open (18:00 · 02:00 · 08:00 · 09:30) a losing trade exits at the open, a winning trade trails under each BC; out at the second session open.
- **Filters:** level held (no close through it before the box) · entry session · MMM PRO FVA H1 and M15 trend.
- 1 pt cost per trade. Stops checked before targets inside a candle. Limit fills are checked candle by candle (no target on the fill candle).

**PASS test** = made money in BOTH 2022–25 and 2026. Why it matters: with this many tests, some settings look good by luck in one period. A setup that also makes money in data it never saw is much more likely to be real. The robustness check = the share of all stop/exit settings of one setup that PASS.

## The short answer

1. **Your model as a strict rule is not a money maker on its own.** 1m: about −0.05 to −0.10 RR a trade. 5m: close to zero. Best version: 5m, "touch then BC" (no close inside).
2. **Big RR wins are real but rare.** Runner: 5 RR+ in 1–2 trades out of 100, 10 RR+ in ~3 out of 1,000. Your 1:5–30 days can happen; the small losers between them decide the result.
3. **Best entry = a limit at the 5m reversal box edge.** Half of its settings PASS. Every other entry ≤ 21%.
4. **Best level = UPG gaps (M15, H1).** Then break boxes (CDL/CDS/LD/SD) and the NY PM opening range low.
5. **Best time:** NY PM 12:00–16:00 and NY AM 09:30–12:00 for UPG gaps.
6. **Why the edge is thin:** after the LTF break at the level, price gives ~1.5 BCs and then an opposite BC; 4 times out of 10 the next BC is already opposite. Close to a coin flip, so even the best setups make only +0.06 to +0.3 RR a trade. None reached WR 60% at 1:2.

## Strategies that PASS (F = MMM PRO FVA)

Pick ONE strategy, study it, check it fits your style, backtest it yourself, then decide. Do not trade them all together.

### FVA.M1

- **Entry TF:** 5m · **HTF level:** H1 UPG gap (3-candle gap) · level must hold (no close through it before the LTF box)
- **Entry:** limit order at the reversal box edge (bull box: its top · bear box: its bottom), first touch fills · **Time / filter:** any time
- **Stop:** box edge (min 20, max 50 pts) · **Close back past the box = out:** yes · **Target:** 1:2 RR · **Trail:** after the 1st opposite candle, then a BC in profit → stop to that pullback low/high

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 1293 | 35.4 | 35% | 1.18 | +0.08 | 2.5 | +101.5 | W: +$30,537 · L: −$27,179 · Net: $3,358 | 28.3 | 6 / 15 |
| 2026 | 110 | 37.9 | 46% | 1.63 | +0.30 | 2.3 | +32.6 | W: +$5,172 · L: −$2,733 · Net: $2,439 | 9.0 | 5 / 9 |
| Both | 1403 | 35.6 | 36% | 1.22 | +0.10 | 3.1 | +134.1 | W: +$35,708 · L: −$29,912 · Net: $5,796 | 28.3 | 6 / 15 |

### FVA.M2

- **Entry TF:** 5m · **HTF level:** any UPG gap (M15 · H1 · H4 · D · W)
- **Entry:** limit order at the reversal box edge (bull box: its top · bear box: its bottom), first touch fills · **Time / filter:** entries 12:00–16:00 NY only
- **Stop:** 50 pts · **Close back past the box = out:** yes · **Target:** 1:3 RR · **Trail:** under each new BC in profit

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 1256 | 34.4 | 46% | 1.29 | +0.07 | 3.0 | +87.4 | W: +$38,789 · L: −$30,051 · Net: $8,738 | 12.2 | 8 / 11 |
| 2026 | 82 | 28.3 | 61% | 2.21 | +0.27 | 2.6 | +22.0 | W: +$4,016 · L: −$1,815 · Net: $2,200 | 4.3 | 6 / 5 |
| Both | 1338 | 34.0 | 47% | 1.34 | +0.08 | 3.6 | +109.4 | W: +$42,805 · L: −$31,867 · Net: $10,938 | 12.2 | 8 / 11 |

### FVA.M3

- **Entry TF:** 5m · **HTF level:** M15 UPG gap
- **Entry:** limit order at the reversal box edge (bull box: its top · bear box: its bottom), first touch fills · **Time / filter:** entries 09:30–12:00 NY only
- **Stop:** box edge (min 20, max 50 pts) · **Close back past the box = out:** yes · **Target:** 1:2 RR · **Trail:** under each new BC in profit

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 866 | 23.7 | 43% | 1.24 | +0.12 | 2.8 | +103.1 | W: +$28,457 · L: −$24,553 · Net: $3,904 | 16.4 | 6 / 9 |
| 2026 | 67 | 23.1 | 49% | 1.67 | +0.32 | 1.9 | +21.6 | W: +$3,894 · L: −$2,108 · Net: $1,786 | 8.0 | 5 / 6 |
| Both | 933 | 23.7 | 43% | 1.27 | +0.13 | 3.2 | +124.7 | W: +$32,351 · L: −$26,661 · Net: $5,690 | 16.4 | 6 / 9 |

### FVA.M4

- **Entry TF:** 5m · **HTF level:** NY PM opening range LOW (13:30–13:45)
- **Entry:** limit order at the reversal box edge (bull box: its top · bear box: its bottom), first touch fills · **Time / filter:** any time
- **Stop:** 50 pts · **Close back past the box = out:** yes · **Target:** 1:3 RR · **Trail:** under each new BC in profit

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 352 | 9.6 | 48% | 1.39 | +0.09 | 2.0 | +31.6 | W: +$11,338 · L: −$8,177 · Net: $3,161 | 9.2 | 6 / 13 |
| 2026 | 25 | 8.6 | 60% | 2.42 | +0.32 | 1.7 | +7.9 | W: +$1,341 · L: −$553 · Net: $788 | 2.4 | 8 / 4 |
| Both | 377 | 9.6 | 49% | 1.45 | +0.10 | 2.4 | +39.5 | W: +$12,679 · L: −$8,730 · Net: $3,949 | 9.2 | 8 / 13 |

### FVA.M5

- **Entry TF:** 5m · **HTF level:** any session / range high or low (Asia, London, London OR, pre-open, Globex/ON, NY AM OR15/OR30, NY AM session, NY PM OR)
- **Entry:** limit order at the reversal box edge (bull box: its top · bear box: its bottom), first touch fills · **Time / filter:** only in the MMM PRO FVA H1 trend direction
- **Stop:** box edge (min 20, max 50 pts) · **Close back past the box = out:** yes · **Target:** 1:3 RR · **Trail:** under each new BC in profit

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 1779 | 48.7 | 43% | 1.22 | +0.09 | 3.1 | +157.9 | W: +$43,239 · L: −$38,012 · Net: $5,226 | 24.5 | 7 / 11 |
| 2026 | 129 | 44.5 | 42% | 1.28 | +0.15 | 1.1 | +19.0 | W: +$5,276 · L: −$3,909 · Net: $1,367 | 12.8 | 6 / 6 |
| Both | 1908 | 48.4 | 43% | 1.22 | +0.09 | 3.3 | +176.9 | W: +$48,515 · L: −$41,921 · Net: $6,593 | 24.5 | 7 / 11 |

### FVA.M6

- **Entry TF:** 1m · **HTF level:** MMM PRO FVA M15 internal box
- **Entry:** limit order at the reversal box edge (bull box: its top · bear box: its bottom), first touch fills · **Time / filter:** entries 09:30–12:00 NY only
- **Stop:** 20 pts · **Close back past the box = out:** yes · **Target:** no target (runner) · **Trail:** after the 1st opposite candle, then a BC in profit → stop to that pullback low/high

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 521 | 14.3 | 28% | 1.38 | +0.20 | 2.2 | +101.8 | W: +$14,825 · L: −$10,753 · Net: $4,071 | 27.1 | 4 / 16 |
| 2026 | 34 | 11.7 | 24% | 1.91 | +0.59 | 1.1 | +20.1 | W: +$1,685 · L: −$882 · Net: $803 | 9.9 | 2 / 12 |
| Both | 555 | 14.1 | 28% | 1.42 | +0.22 | 2.4 | +121.8 | W: +$16,510 · L: −$11,636 · Net: $4,874 | 27.1 | 4 / 16 |

### FVA.M7

- **Entry TF:** 1m · **HTF level:** MMM PRO FVA Bu/Be LEZ (M15 · H1 · H4) · level must hold
- **Entry:** limit order at the reversal box edge (bull box: its top · bear box: its bottom), first touch fills · **Time / filter:** entries 02:00–08:00 NY only
- **Stop:** 20 pts · **Close back past the box = out:** yes · **Target:** 1:2 RR · **Trail:** after the 1st opposite candle, then a BC in profit → stop to that pullback low/high

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 185 | 5.1 | 38% | 1.52 | +0.10 | 2.1 | +19.2 | W: +$2,239 · L: −$1,471 · Net: $767 | 4.5 | 5 / 9 |
| 2026 | 31 | 10.7 | 45% | 2.43 | +0.33 | 1.8 | +10.2 | W: +$692 · L: −$284 · Net: $408 | 3.4 | 2 / 6 |
| Both | 216 | 5.5 | 39% | 1.67 | +0.14 | 2.7 | +29.4 | W: +$2,930 · L: −$1,755 · Net: $1,175 | 4.5 | 5 / 9 |

### FVA.M8

- **Entry TF:** 5m · **HTF level:** any UPG gap (M15 · H1 · H4 · D · W) · level must hold
- **Entry:** limit order at the reversal box edge (bull box: its top · bear box: its bottom), first touch fills · **Time / filter:** any time
- **Stop:** box edge (min 20, max 50 pts) · **Close back past the box = out:** yes · **Target:** 1:2 RR · **Trail:** after the 1st opposite candle, then a BC in profit → stop to that pullback low/high

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 5112 | 140.1 | 33% | 1.13 | +0.06 | 3.6 | +285.6 | W: +$111,902 · L: −$101,916 · Net: $9,986 | 43.5 | 8 / 17 |
| 2026 | 418 | 144.1 | 38% | 1.21 | +0.11 | 1.7 | +47.1 | W: +$14,719 · L: −$11,506 · Net: $3,212 | 19.3 | 5 / 10 |
| Both | 5530 | 140.4 | 34% | 1.14 | +0.06 | 4.0 | +332.7 | W: +$126,620 · L: −$113,422 · Net: $13,198 | 43.5 | 8 / 17 |

### FVA.M9

- **Entry TF:** 5m · **HTF level:** any MMM PRO FVA H1 box (T#, P#, R#, internal, break box, LEZ) · level must hold
- **Entry:** your model: proper retest that touches the box with NO close inside, then a BC closing outside the box → enter next open · **Time / filter:** only in the MMM PRO FVA H1 trend direction
- **Stop:** box edge (min 20, max 50 pts) · **Close back past the box = out:** yes · **Target:** 1:5 RR · **Trail:** BE after 1 BC in profit

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 208 | 5.7 | 15% | 1.82 | +0.23 | 2.2 | +47.4 | W: +$7,796 · L: −$4,193 · Net: $3,603 | 10.8 | 4 / 15 |
| 2026 | 22 | 7.6 | 18% | 1.43 | +0.12 | 0.4 | +2.7 | W: +$804 · L: −$512 · Net: $292 | 2.2 | 1 / 6 |
| Both | 230 | 5.8 | 16% | 1.78 | +0.22 | 2.2 | +50.1 | W: +$8,600 · L: −$4,705 · Net: $3,895 | 10.8 | 4 / 15 |

**Notes per strategy**

- FVA.M1 / FVA.M8: steady but thin (+0.06 to +0.1 RR in 2022–25). Every one of the 70 settings PASS. Many trades, small edge: needs low cost and discipline.
- FVA.M2 / FVA.M3: UPG gaps with a time window. WR 43–61%. Every setting PASS for FVA.M2 (NY PM).
- FVA.M4: NY PM opening range low. Few trades (~10 a month), WR 48–60%.
- FVA.M6: runner style (WR 24–28%), the closest to your big-RR days. Long losing streaks (16 in a row).
- FVA.M7 / FVA.M9: small samples. FVA.M9 is your own model (H1 boxes, with the H1 trend, touch then BC) — it PASSes but the 2026 part is only 22 trades.
- 2026 has only ~3 months of 1m data: treat it as a check, not proof.

## What did NOT work

- Your model on **1m** on most levels; the **break-candle** entry (M4) and the **no-pullback 2nd BC** (M2) almost everywhere.
- PO4 T# boxes, LEZ boxes and opens as a group (negative or mixed).
- "Close inside then BC" (retest type C) was the weakest retest type; "touch then BC" (B) the best.

## Next steps worth testing

- Add a reversal-candle quality filter on the 2nd BC (GMC, volume, MMPD extreme) to lift WR.
- Grow the 2026 1m data (the weekly data task) and re-run the PASS test with more fresh trades.
---

# Round 2 · close back inside, retest sequences, entry areas, 15m, order flow, your management

Results page: https://claude.ai/artifact/91xQaxtFDnxaV81cgt8tN4

## What we learned

1. **Your "close back inside" idea is true.** After an LD / SD / CDL / CDS, if none of the next 3 candles closes back inside the broken box: the next break goes the same way ~69–74% of the time (vs ~57–64%), the move with the break is about 2× bigger, and a deep pullback (close through the far edge) happens ~45% (vs ~76%). Same on 1m, 5m, 15m, 1h, in both periods. Measured on the first 3 candles only (no peeking).
2. **Trading it works:** wait 3 candles after the LD / SD; no close back inside → enter with the break (FVA.M10, FVA.M11). 1h LD: enter at the next open (FVA.M12).
3. **2 BCs before the retest** did not help on average; it helped only with UPG gaps (FVA.M14, FVA.M15).
4. **Best retest sequence:** touch → opposite BC → BC with the retest only touching the box (no close inside); next best touch → NBC → BC (touch only). Worst: touch → NBC → opposite BC → BC.
5. **Best entry area:** 15m = limit at the high / low the entry BC broke · 5m = next open or the box edge · 50% of the entry BC = best with UPG gaps.
6. **Your management (BE + fees, re-entries):** BE + fees after the 1st BC makes ~7 out of 10 setups end with no loss but cuts many winners, so the total stays near zero. BE after the 2nd BC or after an opposite candle → BC keeps more winners. Re-entries helped in 2026, flat in 2022–25. Management changes the shape more than the total; the level and the entry decide the money.
7. **PRO FVA order flow on its own chart:** plain break-close and retest entries are flat on 1m / 5m; they work better on 1h (LD) and with the close-back-inside rule.

## New strategies that PASS

Pick ONE, study it, backtest it yourself, then decide.

### FVA.M10  (PASS · 81% of settings made money in both periods)

- **Entry TF:** 5m · **Level / signal:** 5m MMM PRO FVA LD (long only)
- **Entry:** after the LD, wait 3 candles; if none closed back inside the broken box → enter long at the next open
- **Stop:** zone edge (min 20, max 50 pts) · **Close back past the zone = out:** yes · **Target:** 1:10 RR · **Trail:** none

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 947 | 25.9 | 37% | 1.36 | +0.19 | 3.3 | +180.7 | W: +$42,078 · L: −$31,895 · Net: $10,183 | 37.4 | 7 / 15 |
| 2026 | 92 | 31.7 | 37% | 1.99 | +0.59 | 2.2 | +54.4 | W: +$8,844 · L: −$4,053 · Net: $4,792 | 10.8 | 7 / 9 |
| Both | 1039 | 26.4 | 37% | 1.42 | +0.23 | 3.9 | +235.2 | W: +$50,922 · L: −$35,948 · Net: $14,975 | 37.4 | 7 / 15 |

### FVA.M11  (PASS · 97% of settings made money in both periods)

- **Entry TF:** 15m · **Level / signal:** 15m MMM PRO FVA LD / SD
- **Entry:** after the LD/SD, wait 3 candles; if none closed back inside the broken box → enter at the next open
- **Stop:** 50 pts · **Close back past the zone = out:** yes · **Target:** 1:10 RR · **Trail:** after the 1st opposite candle, then a BC in profit → stop to that pullback low / high

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 570 | 15.6 | 36% | 1.41 | +0.17 | 2.4 | +98.8 | W: +$33,848 · L: −$23,970 · Net: $9,878 | 14.2 | 6 / 14 |
| 2026 | 71 | 24.5 | 39% | 1.54 | +0.27 | 1.3 | +19.1 | W: +$5,467 · L: −$3,556 · Net: $1,911 | 8.9 | 3 / 7 |
| Both | 641 | 16.3 | 37% | 1.43 | +0.18 | 2.7 | +117.9 | W: +$39,315 · L: −$27,526 · Net: $11,789 | 14.2 | 6 / 14 |

### FVA.M12  (PASS · 96% of settings made money in both periods)

- **Entry TF:** 1h · **Level / signal:** 1h MMM PRO FVA LD (long only)
- **Entry:** enter long at the open after the LD candle
- **Stop:** zone edge (min 20, max 50 pts) · **Close back past the zone = out:** yes · **Target:** 1:5 RR · **Trail:** under / over each new BC in profit

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 188 | 5.2 | 40% | 1.82 | +0.37 | 2.9 | +69.3 | W: +$12,602 · L: −$6,770 · Net: $5,832 | 10.2 | 7 / 10 |
| 2026 | 24 | 8.3 | 38% | 2.19 | +0.55 | 1.4 | +13.2 | W: +$2,248 · L: −$1,030 · Net: $1,218 | 3.3 | 3 / 5 |
| Both | 212 | 5.4 | 40% | 1.87 | +0.39 | 3.2 | +82.5 | W: +$14,850 · L: −$7,800 · Net: $7,050 | 10.2 | 7 / 10 |

### FVA.M13  (PASS · 89% of settings made money in both periods)

- **Entry TF:** 15m · **Level / signal:** any UPG gap touched, level held → 15m reversal box
- **Entry:** retest that only touches the box (no close inside) → BC out of the box → next open · Asia 18:00–02:00
- **Stop:** zone edge (min 20, max 50 pts) · **Close back past the zone = out:** yes · **Target:** 1:2 RR · **Trail:** none

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 288 | 7.9 | 43% | 1.53 | +0.21 | 3.0 | +59.4 | W: +$9,627 · L: −$6,918 · Net: $2,709 | 6.4 | 8 / 8 |
| 2026 | 29 | 10.0 | 48% | 2.54 | +0.52 | 2.1 | +15.1 | W: +$2,284 · L: −$834 · Net: $1,450 | 4.1 | 3 / 4 |
| Both | 317 | 8.0 | 43% | 1.61 | +0.23 | 3.5 | +74.5 | W: +$11,911 · L: −$7,752 · Net: $4,158 | 8.4 | 8 / 8 |

### FVA.M14  (PASS · 98% of settings made money in both periods)

- **Entry TF:** 5m · **Level / signal:** H1 UPG gap touched, level held → 5m reversal box
- **Entry:** 2nd BC first (box valid) → retest → BC out → limit at 50% of that BC
- **Stop:** zone edge (no cap) · **Close back past the zone = out:** no · **Target:** 1:10 RR · **Trail:** none

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 307 | 8.4 | 36% | 1.63 | +0.38 | 2.8 | +115.5 | W: +$15,985 · L: −$9,899 · Net: $6,085 | 24.5 | 5 / 11 |
| 2026 | 23 | 7.9 | 43% | 3.39 | +1.05 | 1.7 | +24.2 | W: +$2,593 · L: −$682 · Net: $1,911 | 4.8 | 4 / 5 |
| Both | 330 | 8.4 | 36% | 1.72 | +0.42 | 3.2 | +139.7 | W: +$18,578 · L: −$10,582 · Net: $7,996 | 24.5 | 5 / 11 |

### FVA.M15  (PASS · 97% of settings made money in both periods)

- **Entry TF:** 15m · **Level / signal:** any UPG gap touched → 15m reversal box
- **Entry:** 2nd BC first → retest that only touches → BC out → limit at 50% of that BC · London 02:00–08:00
- **Stop:** 50 pts · **Close back past the zone = out:** yes · **Target:** 1:3 RR · **Trail:** under / over each new BC in profit

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 192 | 5.3 | 44% | 1.47 | +0.11 | 1.8 | +20.8 | W: +$6,508 · L: −$4,424 · Net: $2,084 | 7.2 | 7 / 11 |
| 2026 | 24 | 8.3 | 54% | 2.62 | +0.49 | 1.8 | +11.8 | W: +$1,906 · L: −$726 · Net: $1,179 | 2.6 | 3 / 4 |
| Both | 216 | 5.5 | 45% | 1.63 | +0.15 | 2.4 | +32.6 | W: +$8,414 · L: −$5,151 · Net: $3,263 | 7.2 | 7 / 11 |

### FVA.M16  (PASS · 77% of settings made money in both periods)

- **Entry TF:** 5m · **Level / signal:** H1 UPG gap touched, level held → 5m reversal box
- **Entry:** box → a 2nd BC first (valid) → retest → BC out → next open · re-enter up to 3 times on touch → BC out while the box holds
- **Stop:** zone edge (min 20, max 50 pts) · **Close back past the zone = out:** yes · **Target:** no target (runner) · **Trail:** BE + fees after the 1st BC in profit · re-enter up to 3 times (touch → BC out) while the box holds

| Period | Trades | Trades / month | WR = win rate | PF = profit factor | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 362 | 9.9 | 15% | 1.64 | +0.21 | 1.4 | +74.3 | W: +$14,128 · L: −$7,232 · Net: $6,895 | 31.7 | 2 / 19 |
| 2026 | 30 | 10.3 | 30% | 3.22 | +0.81 | 1.4 | +24.2 | W: +$2,806 · L: −$864 · Net: $1,942 | 4.1 | 4 / 7 |
| Both | 392 | 9.9 | 16% | 1.78 | +0.25 | 1.8 | +98.5 | W: +$16,934 · L: −$8,097 · Net: $8,837 | 31.7 | 4 / 19 |

FVA.M16 is counted per setup (all its trades together); its t-score is under 2, so it is weaker proof than FVA.M10–FVA.M15.

---

# Round 3 · before the touch, retest odds, box type, retest + 1st BC

Results page (interactive, with filters): https://claude.ai/artifact/91xQaxtFDnxaV81cgt8tN4

## What we learned

1. **Which breaks come back to retest** (first LTF box after an HTF touch). Candle right after the break: **NBC** → retested 76–86% · **opposite BC** → ~100% (it is usually the retest itself) · **2nd BC** → only 50–70% · **2nd BC → 2nd BC again** → 25–57%. Strong momentum often never comes back.
2. **Box type:** a box **with an NBC** inside is retested 71–83% of the time, a **BC on BC** box (no NBC) only 49–67%. With-NBC boxes trade slightly better on 5m / 15m.
3. **Before the touch** (break candle → ? → touch → 1st BC): best on 15m = **P0, the retest comes straight after the break** (nothing in between). On 1m / 5m the best is P5 (2nd BC + opposite BC before the touch) but the sample is small. Worst: lots of back and forth (P6 / P7) and P1 (2nd BC → touch).
4. **Retest + 1st BC** works at **UPG gaps on 15m** with a wick-only retest (FVA.M17, t 3.2, 71% of settings pass).
5. **Wick touch beats close inside** again on 5m / 15m.
6. **At ALL levels together nothing passes.** The edge only shows at specific levels (UPG gaps, PRO FVA break boxes, M15 internal boxes).
7. **1m / prop firms:** 1m still has no broad edge. BE after the 2nd BC gives a prop-friendly shape (FVA.M22: only 6% full stop-outs, max DD 6.5 RR), but the 2026 sample is tiny (22 trades).

## New strategies that PASS

Pick ONE, study it, backtest it yourself, then decide.

### FVA.M17  (PASS · WR 37% · avg +0.15 RR · PF 1.29 · target 1:3 · 71% of settings pass both periods)

- **Entry TF:** 15m · **Level / signal:** any UPG gap (M15 · H1 · H4 · D · W) touched, level held → 15m reversal box
- **Entry:** retest that only wicks the box (no close inside) → 1st BC out of the box → enter at the next open
- **Stop:** zone edge (20–50 pts) · **Close back past the zone = out:** yes · **Target:** 1:3 RR · **Trail / management:** none

| Period | Trades | Trades / month | WR | PF | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 882 | 24.2 | 37% | 1.29 | +0.14 | 3.0 | +127.5 | W: +$41,755 · L: −$33,940 · Net: +$7,815 | 25.2 | 8 / 11 |
| 2026 | 83 | 28.6 | 33% | 1.31 | +0.18 | 1.0 | +15.0 | W: +$6,104 · L: −$4,442 · Net: +$1,661 | 7.9 | 3 / 9 |
| Both | 965 | 24.5 | 37% | 1.29 | +0.15 | 3.2 | +142.5 | W: +$47,859 · L: −$38,383 · Net: +$9,476 | 25.2 | 8 / 11 |

### FVA.M18  (PASS · WR 25% · avg +0.20 RR · PF 1.30 · target 1:10 · 84% of settings pass both periods)

- **Entry TF:** 15m · **Level / signal:** M15 UPG gap touched, level held → 15m reversal box
- **Entry:** retest that only wicks the box → 1st BC out → limit at the high / low that BC broke
- **Stop:** 20 pts · **Close back past the zone = out:** yes · **Target:** 1:10 RR · **Trail / management:** none

| Period | Trades | Trades / month | WR | PF | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 494 | 13.5 | 26% | 1.27 | +0.18 | 1.7 | +89.2 | W: +$16,988 · L: −$13,421 · Net: +$3,567 | 47.8 | 5 / 22 |
| 2026 | 40 | 13.8 | 20% | 1.62 | +0.48 | 0.9 | +19.4 | W: +$2,019 · L: −$1,244 · Net: +$774 | 9.0 | 1 / 8 |
| Both | 534 | 13.6 | 25% | 1.30 | +0.20 | 1.9 | +108.5 | W: +$19,007 · L: −$14,666 · Net: +$4,342 | 47.8 | 5 / 22 |

### FVA.M19  (PASS · WR 41% · avg +0.14 RR · PF 1.27 · target 1:2 · 70% of settings pass both periods)

- **Entry TF:** 5m · **Level / signal:** any PRO FVA break box (CDL · CDS · LD · SD on M15 / H1 / H4) touched → 5m reversal box that has an NBC inside
- **Entry:** retest → 1st BC out → enter at the next open
- **Stop:** zone edge (20–50 pts) · **Close back past the zone = out:** yes · **Target:** 1:2 RR · **Trail / management:** none

| Period | Trades | Trades / month | WR | PF | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 567 | 15.5 | 41% | 1.27 | +0.14 | 2.5 | +77.0 | W: +$24,871 · L: −$19,615 · Net: +$5,256 | 17.0 | 7 / 10 |
| 2026 | 46 | 15.9 | 41% | 1.34 | +0.17 | 0.9 | +8.0 | W: +$2,628 · L: −$1,846 · Net: +$782 | 9.1 | 9 / 7 |
| Both | 613 | 15.6 | 41% | 1.27 | +0.14 | 2.7 | +85.0 | W: +$27,499 · L: −$21,461 · Net: +$6,038 | 17.0 | 9 / 10 |

### FVA.M20  (PASS · WR 35% · avg +0.08 RR · PF 1.16 · target 1:5 · 82% of settings pass both periods)

- **Entry TF:** 15m · **Level / signal:** any UPG gap touched, level held → 15m reversal box
- **Entry:** the break candle is followed straight away by the retest (no BC, NBC or opposite candle in between) → 1st BC out → next open
- **Stop:** zone edge (20–50 pts) · **Close back past the zone = out:** yes · **Target:** 1:5 RR · **Trail / management:** none

| Period | Trades | Trades / month | WR | PF | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 868 | 23.8 | 35% | 1.16 | +0.08 | 1.6 | +71.4 | W: +$38,755 · L: −$34,888 · Net: +$3,867 | 24.1 | 5 / 18 |
| 2026 | 85 | 29.3 | 28% | 1.15 | +0.09 | 0.5 | +7.7 | W: +$5,387 · L: −$4,654 · Net: +$733 | 8.5 | 2 / 7 |
| Both | 953 | 24.2 | 35% | 1.16 | +0.08 | 1.6 | +79.2 | W: +$44,142 · L: −$39,542 · Net: +$4,600 | 24.1 | 5 / 18 |

### FVA.M21  (PASS · WR 35% · avg +0.11 RR · PF 1.29 · target 1:3 · 66% of settings pass both periods)

- **Entry TF:** 5m · **Level / signal:** M15 UPG gap touched → 5m reversal box
- **Entry:** break → an NBC → then the retest → 1st BC out → next open · after a stop, re-enter once on touch → BC out while the box holds
- **Stop:** 50 pts · **Close back past the zone = out:** no · **Target:** 1:3 RR · **Trail / management:** none · 1 re-entry

| Period | Trades | Trades / month | WR | PF | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 748 | 20.5 | 34% | 1.26 | +0.09 | 2.3 | +70.2 | W: +$33,624 · L: −$26,604 · Net: +$7,020 | 16.0 | 6 / 14 |
| 2026 | 68 | 23.4 | 37% | 1.53 | +0.27 | 1.4 | +18.3 | W: +$5,270 · L: −$3,444 · Net: +$1,826 | 5.1 | 4 / 6 |
| Both | 816 | 20.7 | 35% | 1.29 | +0.11 | 2.7 | +88.5 | W: +$38,894 · L: −$30,048 · Net: +$8,846 | 16.0 | 6 / 14 |

### FVA.M22  (PASS · WR 14% · avg +0.09 RR · PF 1.91 · target 1:3 · 64% of settings pass both periods)

- **Entry TF:** 1m · **Level / signal:** PRO FVA M15 internal box touched → 1m reversal box
- **Entry:** break → 2nd BC, NBC and an opposite candle → retest closes inside the box → 1st BC out → next open
- **Stop:** 50 pts · **Close back past the zone = out:** no · **Target:** 1:3 RR · **Trail / management:** BE after 2 BC in profit

| Period | Trades | Trades / month | WR | PF | avg RR | t-score | Net RR | Money (1 MNQ) | Max DD (RR) | Max wins / losses in a row |
|---|---|---|---|---|---|---|---|---|---|---|
| 2022–25 | 504 | 13.8 | 15% | 1.92 | +0.09 | 3.0 | +46.1 | W: +$9,612 · L: −$4,999 · Net: +$4,613 | 6.5 | 3 / 30 |
| 2026 | 22 | 7.6 | 9% | 1.53 | +0.05 | 0.3 | +1.1 | W: +$322 · L: −$210 · Net: +$112 | 1.6 | 1 / 12 |
| Both | 526 | 13.4 | 14% | 1.91 | +0.09 | 3.0 | +47.2 | W: +$9,934 · L: −$5,210 · Net: +$4,724 | 6.5 | 3 / 30 |

**Notes**

- FVA.M17 = the clean "retest + 1st BC" model. Strongest proof this round (t 3.2).
- FVA.M18 / FVA.M20: t-score under 2 → weaker proof. FVA.M20 is the "retest straight after the break" (P0) finding.
- FVA.M19: WR 41% at 1:2 on PRO FVA break boxes with an NBC box → easiest to follow for prop rules.
- FVA.M22: low WR (14%) because most trades end at BE; only 6% are full stop-outs. 2026 has just 22 trades.

---

# Round 3b · after the retest

Every first LTF reversal box after an HTF level touch that came back for a retest (1m / 5m / 15m, both periods). Entry = retest + 1st BC out → next open. WR at a fixed 50 pt stop, 1:2 (break-even ≈ 34% WR after costs).

1. **Next candle after the touch:** usually an **NBC** (40–63%). The touch candle itself is the BC out 19–27% of the time after a break → 2nd BC, only 2% after a break → NBC. An opposite BC comes next 10–17%.
2. **How retests end:** 4–7 in 10 end with a BC back out (entry); 2–5 in 10 close through the box first.
3. **Break → opposite BC:** retested almost always, but once retested the box breaks about **half the time**.
4. **Entry WR at all levels:** 35–42% at 1:2 with a 50 pt stop → about break-even. No edge without the right level.
5. **Best at UPG gaps:**
   - 5m: break → opposite BC → retest → NBC → BC. WR 46% / 54%, avg RR +0.12 / +0.47.
   - 15m: break → NBC → retest → BC out on the next candle. WR 38% / 46%, avg RR +0.04 / +0.31.
6. **1m:** no pattern stands out.

Interactive tab "After the retest": https://claude.ai/artifact/91xQaxtFDnxaV81cgt8tN4 (also on maxmaserati.com/backtests/pro-f/ once live).
