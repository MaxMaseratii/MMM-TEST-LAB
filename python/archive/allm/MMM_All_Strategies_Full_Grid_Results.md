# MMM all strategies: the full grid on 4 markets (Oct 30 2026)

The results sheet is the artifact **MMM All Strategies Grid**. It has a strategy board per market and side, and an entry × stop matrix for each strategy.

## What was tested

**Strategies:**
- The 18 EDGE PRO strategies: X.M1–M5, C.M1–M8 and XCS.M1–M5.
- The 22 FVA strategies: FVA.M1–M22.
- FVA.A (1h box fail) and FVA.B (Asia flip-zone fail).
- GMU on 5m, 15m, 1h and 4h.
- The XB FVA after the break, and the XB zones (XBS buy, XBB sell). Both are on 5m, 15m, 1h and 4h.

**Markets:** NQ / MNQ, ES / MES, gold / MGC, crude / MCL.

**Each setup was tested against:**
- **16 entries:**
  - the native entry;
  - market at the signal close;
  - the signal-candle ladder XD 0 · D 12.5 · MD 25 · BAL 50 · MP 75 · P 87.5 · XP 100, measured from the low;
  - the same ladder on the zone (the box or level the setup is built on).
- **6 stops:** native, fixed 50 (ES 20 · gold 12 · crude 0.50), 1.5 × ATR(14), past the signal candle, past the zone's far side, and past the zone 50%.
- **7 targets:** 1:1, 1:1.5, 1:2, 1:3, 1:4, 1:6 and 1:10. 1:10 is rarely hit, so it mostly works as "hold up to 100 candles".
- **4 exits:**
  - stop / target only;
  - a close through the zone (violation);
  - the next session open (02:00, 08:00, 09:30 NY);
  - the first opposite BC close.
- Each pairing was paired one by one. **Bull and bear were tested apart.**

**Periods:**
- **NQ:** NQ 1m Dec 2022 – Dec 2025, then MNQ Dec 2025 – Oct 28 2026.
- **ES, gold, crude:** the first half vs the second half of each chart's own data (Dec 2025 – Oct 2026). 5m data starts in mid-July, and there are few 1m days.

**Grading:**
- Trades are graded on the finest bars. The stop wins a tie.
- A limit only counts its target from the bar after the fill.
- Cost per trade: NQ 1, ES 0.5, gold 0.2, crude 0.02.
- Limits wait 10 candles; native limits use their own wait.
- A trade whose risk is under 8% of the 50-pt stop is skipped.

**PASS** = t-score ≥ 2 in BOTH periods, with at least 30 trades in period 1 and 20 in period 2.

**Random baseline:** random entries on each chart, with the same full grid.

## Short answer

**Passing pairings per market:**

| Market | Pairings that pass | Strategy sides with a pass | Random entries passing |
|---|---|---|---|
| NQ / MNQ | 2,717 | 27 | 0 |
| ES / MES | 9 | 3 | 0 |
| Gold / MGC | 41 | 6 | 0 |
| Crude / MCL | 496 | 6 | 6 on 1h and 22 on 4H (longs) |

**NQ is the edge market:**
- 2,717 pairings pass, while random entries pass 0. That is far more than luck.
- 2,650 of those passes are longs. Only X.M1 and X.M2 also pass short.
- Random longs on NQ pass 0 too, so this is more than the up-trend.

**ES:** nothing to trade. 9 passes, all small: C.M3 long, XB FVA 1h short, GMU 4H short.

**Gold:** the short side holds. 39 of the 41 passes are shorts: GMU 1h short (23 passes), FVA.M18 short, XCS.M2 short and FVA.A short. These are small samples.

**Crude:** every pass is a long while crude went from $59 to $101. Random 4H longs pass 22 pairings too. GMU 4H long (232) and XCS.M2 long (214) are the strongest, but they are mostly the trend.

## The best entry (the question)

Counted over all 2,717 NQ passes. Pairs are period 1 → period 2.

**Entries:**
- **Shallow entries win.**
  - candle XP (the signal high/low) and market at the signal close: 817.
  - candle P (87.5%): 347.
  - the native entry: 337.
  - candle MP (75%): 292.
  - candle BAL: 149.
- **Deep entries rarely pass.** candle XD / D / MD: 220. zone XD / D / MD: 11.
- **Rule:** enter at the signal close, or with a limit at P / MP of the signal candle. Do not wait for the deep pullback; it misses the winners.

**Stops:**
- fixed 50: 859.
- native: 779.
- ATR 1.5×: 568.
- past the zone's far side: 426.
- past the zone 50%: 73.
- **past the signal candle: 12.** It is too tight and gets swept.

**Exits:** all 4 work on NQ.
- stop/target only: 806.
- next session open: 779.
- close through the zone: 745.
- opposite BC: 387.

**Targets:** spread from 1:1.5 to 1:10. There is no single best target.

## Strategies with passing pairings

- **Passes** = the number of passing pairings.
- **Best** = the pairing with the highest lower t-score of the two periods.
- **Top-20 → P2** = the 20 best pairings picked on period 1, averaged in period 2. This is the honest check.


### NQ

| Strategy | Side | Passes | Native avg RR | Best entry · stop · target · exit | Trades | WR | PF | avg RR | t-score | Top-20 → P2 |
|---|---|---|---|---|---|---|---|---|---|---|
| C.M4 (15m) | BULL | 585 | +0.39 → +0.46 | candle P · fixed 50 (scaled) · 1:3 · next session open | 391 → 129 | 51% → 50% | 1.75 → 2.08 | +0.25 → +0.49 | 4.0 / 3.5 | +0.52 |
| C.M5 (15m) | BULL | 352 | +0.19 → +0.12 | candle P · native stop · 1:1.5 · stop / target only | 2280 → 710 | 46% → 47% | 1.24 → 1.30 | +0.13 → +0.16 | 4.9 / 3.4 | +0.13 |
| C.M3 (15m) | BULL | 282 | +0.11 → +0.15 | candle P · ATR 1.5x · 1:10 · next session open | 1877 → 567 | 46% → 46% | 1.29 → 1.36 | +0.14 → +0.18 | 4.2 / 2.7 | +0.17 |
| X.M3 (5m) | BULL | 188 | +0.12 → +0.12 | candle XP · native stop · 1:10 · stop / target only | 2218 → 354 | 45% → 40% | 1.25 → 1.78 | +0.12 → +0.46 | 4.2 / 3.8 | +0.18 |
| X.M4 (15m) | BULL | 183 | +0.23 → +0.22 | candle P · fixed 50 (scaled) · 1:1.5 · first opposite BC close | 343 → 119 | 48% → 54% | 1.71 → 2.01 | +0.16 → +0.25 | 3.7 / 3.1 | +0.22 |
| GMU 5m (5m) | BULL | 167 | +0.03 → +0.03 | candle P · past zone far side · 1:10 · close through the zone (violation) | 20588 → 3201 | 24% → 24% | 1.07 → 1.18 | +0.05 → +0.14 | 3.1 / 3.2 | +0.09 |
| C.M1 (15m) | BULL | 151 | +0.20 → +0.17 | candle MD · native stop · 1:4 · next session open | 1229 → 390 | 39% → 39% | 1.21 → 1.40 | +0.12 → +0.24 | 2.6 / 2.7 | +0.11 |
| C.M2 (15m) | BULL | 145 | +0.09 → +0.07 | zone MP · past zone far side · 1:2 · stop / target only | 3638 → 1122 | 38% → 40% | 1.12 → 1.24 | +0.08 → +0.15 | 3.3 / 3.4 | +0.07 |
| X.M2 (15m) | BULL | 135 | +0.17 → +0.32 | market at signal close · fixed 50 (scaled) · 1:1.5 · close through the zone (violation) | 500 → 174 | 42% → 52% | 1.37 → 1.67 | +0.17 → +0.31 | 3.3 / 3.3 | +0.23 |
| X.M1 (15m) | BULL | 91 | +0.20 → +0.08 | candle P · fixed 50 (scaled) · 1:1.5 · stop / target only | 566 → 214 | 48% → 50% | 1.35 → 1.45 | +0.18 → +0.23 | 3.5 / 2.7 | +0.16 |
| GMU 15m (15m) | BULL | 82 | +0.07 → +0.01 | zone MP · past zone far side · 1:3 · stop / target only | 6618 → 2085 | 29% → 30% | 1.08 → 1.14 | +0.06 → +0.10 | 2.6 / 2.7 | +0.02 |
| X.M5 (15m) | BULL | 82 | +0.17 → +0.52 | candle P · native stop · 1:2 · stop / target only | 337 → 125 | 41% → 48% | 1.33 → 1.80 | +0.20 → +0.42 | 2.5 / 3.1 | +0.08 |
| X.M1 (15m) | BEAR | 64 | +0.38 → +0.50 | candle MD · fixed 50 (scaled) · 1:10 · stop / target only | 345 → 154 | 23% → 21% | 1.60 → 2.05 | +0.47 → +0.84 | 2.7 / 2.7 | +0.44 |
| FVA.M20 (15m) | BULL | 47 | +0.19 → +0.35 | native · fixed 50 (scaled) · 1:2 · close through the zone (violation) | 429 → 109 | 36% → 47% | 1.35 → 1.73 | +0.18 → +0.39 | 2.8 / 2.7 | +0.27 |
| XCS.M1 (15m) | BULL | 38 | +0.14 → +0.25 | candle MP · fixed 50 (scaled) · 1:2 · stop / target only | 564 → 180 | 41% → 44% | 1.32 → 1.52 | +0.19 → +0.30 | 3.1 / 2.7 | +0.23 |
| XB FVA 5m (5m) | BULL | 35 | +0.01 → -0.06 | candle XP · native stop · 1:10 · close through the zone (violation) | 15102 → 2180 | 26% → 26% | 1.07 → 1.22 | +0.03 → +0.11 | 2.9 / 3.0 | +0.10 |
| XB FVA 15m (15m) | BULL | 25 | +0.02 → -0.10 | candle XP · native stop · 1:10 · close through the zone (violation) | 4832 → 1603 | 26% → 24% | 1.15 → 1.25 | +0.08 → +0.17 | 3.4 / 3.0 | +0.05 |
| C.M6 (1m) | BULL | 16 | +0.12 → +0.66 | zone XP · fixed 50 (scaled) · 1:10 · next session open | 422 → 21 | 44% → 48% | 1.55 → 5.53 | +0.38 → +2.75 | 3.4 / 2.7 | +1.53 |
| GMU 4h (4h) | BULL | 11 | +0.12 → +0.06 | zone XP · ATR 1.5x · 1:6 · close through the zone (violation) | 591 → 183 | 23% → 25% | 1.34 → 1.57 | +0.26 → +0.42 | 2.5 / 2.1 | +0.11 |
| XB zone 15m (15m) | BULL | 11 | +0.03 → -0.03 | candle BAL · ATR 1.5x · 1:10 · close through the zone (violation) | 8524 → 2865 | 14% → 14% | 1.11 → 1.18 | +0.07 → +0.11 | 2.6 / 2.5 | +0.04 |
| C.M7 (1m) | BULL | 8 | +0.16 → +0.91 | zone XP · fixed 50 (scaled) · 1:10 · next session open | 422 → 21 | 44% → 48% | 1.55 → 5.53 | +0.38 → +2.75 | 3.4 / 2.7 | +1.40 |
| GMU 1h (1h) | BULL | 8 | +0.15 → +0.03 | zone XP · past zone 50% · 1:2 · close through the zone (violation) | 1957 → 625 | 37% → 38% | 1.13 → 1.19 | +0.08 → +0.12 | 2.5 / 2.0 | +0.03 |
| XCS.M5 (15m) | BULL | 4 | +0.18 → +0.61 | candle P · ATR 1.5x · 1:2 · first opposite BC close | 91 → 29 | 45% → 55% | 1.76 → 2.67 | +0.34 → +0.57 | 2.4 / 2.3 | +0.52 |
| X.M2 (15m) | BEAR | 3 | +0.17 → +0.19 | candle D · native stop · 1:3 · stop / target only | 317 → 126 | 33% → 34% | 1.41 → 1.52 | +0.27 → +0.35 | 2.6 / 2.1 | +0.20 |
| FVA.M17 (15m) | BULL | 2 | +0.17 → +0.25 | candle MD · ATR 1.5x · 1:3 · stop / target only | 381 → 103 | 32% → 38% | 1.28 → 1.71 | +0.20 → +0.45 | 2.1 / 2.4 | +0.16 |
| FVA.M13 (15m) | BULL | 1 | +0.11 → +0.42 | candle BAL · native stop · 1:1 · next session open | 122 → 39 | 61% → 62% | 1.69 → 2.00 | +0.19 → +0.29 | 2.6 / 2.1 | -0.00 |
| FVA.M18 (15m) | BULL | 1 | +0.12 → +0.05 | candle MD · ATR 1.5x · 1:4 · stop / target only | 294 → 72 | 28% → 35% | 1.34 → 1.99 | +0.26 → +0.66 | 2.0 / 2.4 | +0.17 |

### ES

| Strategy | Side | Passes | Native avg RR | Best entry · stop · target · exit | Trades | WR | PF | avg RR | t-score | Top-20 → P2 |
|---|---|---|---|---|---|---|---|---|---|---|
| C.M3 (15m) | BULL | 6 | +0.07 → +0.15 | zone P · ATR 1.5x · 1:10 · first opposite BC close | 238 → 251 | 42% → 37% | 1.51 → 1.66 | +0.12 → +0.21 | 2.2 / 2.2 | -0.02 |
| XB FVA 1h (1h) | BEAR | 2 | +0.09 → +0.06 | candle BAL · fixed 50 (scaled) · 1:1 · next session open | 154 → 129 | 54% → 60% | 1.50 → 1.74 | +0.13 → +0.17 | 2.1 / 2.7 | +0.12 |
| GMU 4h (4h) | BEAR | 1 | -0.34 → +0.14 | zone MP · ATR 1.5x · 1:1.5 · stop / target only | 49 → 32 | 55% → 62% | 1.81 → 2.45 | +0.37 → +0.55 | 2.0 / 2.5 | +0.13 |

### GC

| Strategy | Side | Passes | Native avg RR | Best entry · stop · target · exit | Trades | WR | PF | avg RR | t-score | Top-20 → P2 |
|---|---|---|---|---|---|---|---|---|---|---|
| GMU 1h (1h) | BEAR | 23 | -0.04 → +0.18 | native · ATR 1.5x · 1:2 · stop / target only | 211 → 263 | 41% → 41% | 1.36 → 1.38 | +0.22 → +0.22 | 2.1 / 2.5 | +0.14 |
| FVA.M18 (15m) | BEAR | 8 | +0.30 → +0.46 | candle D · fixed 50 (scaled) · 1:4 · next session open | 44 → 48 | 43% → 52% | 2.29 → 2.52 | +0.73 → +0.65 | 2.2 / 2.5 | +0.36 |
| XCS.M2 (15m) | BEAR | 4 | -0.04 → +0.14 | candle P · ATR 1.5x · 1:3 · stop / target only | 252 → 353 | 33% → 33% | 1.44 → 1.39 | +0.30 → +0.27 | 2.5 / 2.7 | +0.20 |
| FVA.A (1h) | BEAR | 3 | +0.05 → +0.09 | candle XD · past signal candle · 1:3 · stop / target only | 319 → 288 | 33% → 32% | 1.31 → 1.33 | +0.20 → +0.23 | 2.0 / 2.1 | +0.08 |
| X.M5 (15m) | BULL | 2 | +0.07 → -0.19 | candle XP · past signal candle · 1:1.5 · first opposite BC close | 69 → 57 | 52% → 51% | 1.76 → 1.87 | +0.29 → +0.29 | 2.1 / 2.1 | +0.19 |
| GMU 15m (15m) | BEAR | 1 | +0.03 → +0.08 | zone MP · fixed 50 (scaled) · 1:3 · stop / target only | 461 → 506 | 31% → 31% | 1.29 → 1.31 | +0.20 → +0.22 | 2.4 / 2.6 | +0.07 |

### CL

| Strategy | Side | Passes | Native avg RR | Best entry · stop · target · exit | Trades | WR | PF | avg RR | t-score | Top-20 → P2 |
|---|---|---|---|---|---|---|---|---|---|---|
| GMU 4h (4h) | BULL | 232 | +0.02 → +0.13 | zone P · ATR 1.5x · 1:4 · close through the zone (violation) | 90 → 82 | 39% → 39% | 2.41 → 2.42 | +0.86 → +0.86 | 3.4 / 3.3 | +0.46 |
| XCS.M2 (15m) | BULL | 214 | +0.15 → +0.16 | zone MP · native stop · 1:6 · close through the zone (violation) | 490 → 490 | 22% → 20% | 1.73 → 1.50 | +0.43 → +0.36 | 4.0 / 3.0 | +0.24 |
| GMU 5m (5m) | BULL | 30 | +0.00 → +0.10 | candle XD · fixed 50 (scaled) · 1:4 · stop / target only | 609 → 633 | 33% → 31% | 1.32 → 1.30 | +0.22 → +0.21 | 2.8 / 2.7 | +0.16 |
| XB zone 1h (1h) | BULL | 16 | +0.09 → -0.01 | zone MP · ATR 1.5x · 1:10 · stop / target only | 241 → 333 | 24% → 24% | 1.65 → 1.67 | +0.50 → +0.52 | 2.4 / 3.0 | +0.07 |
| XB FVA 1h (1h) | BULL | 3 | +0.06 → -0.05 | candle XD · ATR 1.5x · 1:10 · stop / target only | 93 → 122 | 25% → 25% | 2.14 → 1.91 | +0.88 → +0.69 | 2.2 / 2.3 | -0.06 |
| FVA.M5 (5m) | BULL | 1 | -0.14 → -0.02 | candle XD · fixed 50 (scaled) · 1:4 · stop / target only | 47 → 43 | 47% → 40% | 2.50 → 2.22 | +0.81 → +0.75 | 2.6 / 2.1 | +0.15 |

**Not listed:** the other strategy sides (about 61 on NQ, 60 on ES, 50 on gold, 50 on crude). They had no pairing that passes in both periods. Full numbers are on the sheet.

## What it means

**NQ / MNQ, trade the longs of:**
- C.M4 (585 passes; native +0.39 → +0.46 avg RR);
- C.M5, C.M3, X.M3, X.M4, C.M1, C.M2, X.M2, X.M1;
- FVA.M20 (the only strong FVA.M);
- XCS.M1.

The best tweaks over each native setup:
- a limit at P (87.5%) of the signal candle;
- a fixed 50 or the native stop;
- out at the next session open, or on a close through the zone.

**X.M1 short and X.M2 short** also pass on NQ.

**FVA.M1–M22:**
- Only **FVA.M20 long** holds well: 47 passes, avg RR +0.18 → +0.39 native with the violation exit.
- FVA.M17, M13 and M18 long have 1–2 passes each.
- **The other 18 FVA.M strategies have no pairing that passes in both periods, on any market.**

**GMU, XB FVA and XB zones:**
- They pass on NQ longs (GMU 5m 167, GMU 15m 82, XB FVA 5m/15m 35/25), but with small avg RR (+0.05 to +0.17).
- Shorts: none.

**ES, gold, crude:**
- **ES:** don't trade these strategies.
- **Gold:** only the short-side watch list (GMU 1h short, FVA.M18 short, XCS.M2 short).
- **Crude:** the long passes are the trend.

## Caveats

- **The engines were rebuilt in Python from the Pine code.**
  - EDGE PRO: from the Oct 25 Pine upload (15 strategies). X.M3, XCS.M3/M4, C.M6/M7 and C.M8 come from the written book rules.
  - On NQ, setup counts are within ±30% of the book for all 18 (most within 2%).
  - FVA.M: ported from claude/MMM_EDGE_PRO_FVA.pine. 13 of 22 are within ±30% of the book's trade count. M1, M4, M5, M7, M8 and M18 are 1.3–1.4×, M9 is 1.75× and M15 is 0.62×. The earlier rebuild showed the same gaps.
- **No native trade management:** ½ out, trails, BE and the FVA session rule are not used. The grid's own exits replace them.
- **C.M6 / C.M7 (1m)** have only 21 trades in 2026: too few to trust.
- **ES, gold and crude** have about 11 months. Their periods are halves of that.
- **This is the best of thousands of pairings per strategy.** Use the Top-20 → P2 column and the random baseline to judge. On NQ, the strong ones keep +0.1 to +0.5 avg RR in period 2.

## New entries vs the old (native) entries — honest check (added Oct 30)

Method: the new pairing was picked on period 1 only (the highest t-score in 2022–25), then checked on 2026. Its 2026 result is compared with the native strategy's 2026 result. (The "best" column on the sheet is picked with both periods, so it always looks better: hindsight.)

- **On average: no.** NQ, all 85 strategy sides: native +0.096 avg RR in 2026 vs picked +0.037. The 25 NQ sides that pass: native +0.191 vs picked +0.168 (better in 12 of 25). ES, gold: picked worse. Crude: picked a little better (the trend).
- **Where the new entry really helped (NQ, 2026 avg RR, native → picked on 2022–25):**
  - C.M4 long: +0.46 → +0.53 (limit at candle MP, t 3.1)
  - X.M3 long: +0.12 → +0.17 (candle XP)
  - XCS.M1 long: +0.25 → +0.30 (limit at candle MP)
  - X.M4 long: +0.22 → +0.25 (same native entry, other stop / exit)
  - C.M3 long: +0.15 → +0.16
  - GMU 5m long: +0.03 → +0.10 · XB FVA 5m long: −0.06 → +0.09
- **Where the native entry stays better:** X.M2 long (+0.32 vs +0.19), X.M5 long (+0.52 vs +0.02), X.M1 short (+0.50 vs +0.43), C.M1 long (+0.17 vs +0.10), FVA.M20 long (+0.35 vs +0.30), FVA.M13 / M17, GMU 4h, C.M5 (equal).
- **Keep the native rules** for most strategies. Switch only C.M4, X.M3, XCS.M1 (and the GMU 5m / XB FVA 5m research setups) to the new entry.

## Applied on Oct 30 — and one correction

The grid's "native" has no ½ out. So the check above compared the new pairings with a native that is not the real live rule. Checked again against the **real old rules** (the site's own trades), NQ longs, 2026 avg RR:

| Strategy | Real old rule 2022–25 → 2026 | New rule 2022–25 → 2026 | Applied? |
|---|---|---|---|
| C.M4 | +0.13 → +0.31 (½ out, 1 × ATR) | +0.30 → +0.55 (c3 close, stop 50, full 1:6, out at next session open) | **Yes** |
| XCS.M1 longs | +0.12 → +0.26 (market at close) | +0.19 → +0.30 (limit at candle MP) | **Yes** |
| X.M3 | +0.12 → +0.12 (limit at block top) | +0.12 → +0.17 (market at the birth close) | **Yes** |
| X.M4 longs | +0.18 → +0.33 (½ out, 1.5 ATR) | +0.31 → +0.25 (stop 50, 1:2, next session open) | **No** — worse in 2026 |

- **C.M4 entry did not change.** The grid's "candle MP" pick fills at the c3 close almost every time (t 4.24 vs 4.23). The change is the stop (50), the full 1:6 and the next-session-open exit.
- **NQ / MNQ only.** On ES, gold and crude the new rules did not hold (C.M4 ES +0.05, gold −0.12; XCS.M1 longs ES +0.07, gold −0.13). Those markets keep the old rules. The EDGE PRO indicator switches by itself.
- Updated: the website cards (6 languages), MMM EDGE PRO, claude/MMM_EDGE_PRO_18_Strategies.md and claude/MMM_Strategy_Entries_Oct30.md.

## EDGE PRO FVA (FVA.M1–M22): no change (checked Oct 30)

Same honest check as above: pick the best pairing on 2022–25 only, then compare its 2026 avg RR with the **real book rule** (the site's own numbers, with the FVA trade management: break-even, trail, session rule).

- No picked pairing beats the real rule in 2026 with a t-score of 2+. Most lose to it:
  - FVA.M2 picked +0.17 vs real +0.27 · M3 +0.22 vs +0.32 · M4 +0.24 vs +0.32 · M14 +0.36 vs +1.05 · M16 +0.36 vs +0.81 · M18 +0.21 vs +0.48.
- The only one ahead is **FVA.M5 shorts** (zone MD limit, stop past the signal candle, 1:10, out at the first opposite BC): +0.36 vs the real rule's +0.15 (both sides). But its t-score is 1.7 in 2022–25 and 0.9 in 2026, so it is not proven. Watch only.
- The grid's FVA engine is a rebuild. Its trade counts differ from the book by up to 1.75× on some strategies, so the book's own numbers win when they disagree.
- **Decision: MMM EDGE PRO FVA and the FVA cards stay as they are.**
