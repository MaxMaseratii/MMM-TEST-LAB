# MMM Xpander Block (XB) + GMU: test results (Oct 30 2026)

Indicator: **MMM PRO x 4.0** (`claude/MMM_PRO_x_4.0.pine`), the new Xpander Block logic.

## Data and rules
- **Data:**
  - NQ 1m from Dec 2022 to Dec 2025 ("old").
  - MNQ from Dec 2025 to Oct 28 2026 ("2026"). Each 2026 day uses the finest bars it has: 1m, then 5m, then 15m.
  - 5m tests in 2026 use only the days that have 1m or 5m bars.
- **Charts:** 5m, 15m, 1h, 4h. Closed candles only.
- **Main trade:** 50 pt stop at 1:2. 1 pt cost per trade.
- **Scoring:**
  - Every trade is replayed on the finest bars.
  - The stop wins when the stop and the target are hit in the same bar.
  - A limit only scores its target from the bar after its fill.
- **Second stops:** 1.5 × ATR(14), and the zone stop (just past the zone).
- **Labels:** WR = win rate, PF = profit factor, avg = average R per trade, t = t-score. Pairs read old → 2026.
- **Random baseline:** random side, entry at the close, 50 pt stop, 1:2.

  | Chart | Random avg (old → 2026) |
  |---|---|
  | 5m | −0.007 → −0.002 |
  | 15m | +0.001 → −0.035 |
  | 1h | −0.046 → −0.047 |
  | 4h | −0.059 → +0.071 |

## Words
- **MU (Momentum Urgency):** a body close (old name MC).
- **GMU (Gap Momentum Urgency):** old name GMC. Candle 2 is a body close and candle 3 leaves a gap of at least 2 ticks with candle 1.
- **XB (Xpander Block):**
  - It starts when an NBC prints after a BC.
  - Its high and low are the last high and low from the BC to the NBCs (they grow with wicks).
  - It lives until a candle CLOSES above the high (bull break) or below the low (bear break).
- **Balanced Zone:** from the highest to the lowest open or close of the candles after the BC.
- **XBB (XB Buying Zone):** from the Balanced top up to the XB high (premium). Max's rule: BUY here.
- **XBS (XB Selling Zone):** from the XB low up to the Balanced bottom (discount). Max's rule: SELL here.
- **Sell in discount, buy in premium** (corrected Oct 30; section 2 below tested the opposite read first, section 7 tests Max's read).
- **BeFVA:** after a bear break, the FIRST NBC of the block, from its body bottom to its high.
- **BuFVA:** after a bull break, the first NBC, from its low to its body top.
- An FVA lives until a close goes through it.

---

## 1. GMU ladder: 3 approaches

**Ladder:** XD 0 · D 12.5 · MD 25 · BAL 50 · MP 75 · P 87.5 · XP 100, measured from the low of the chosen range.

- **Approach A, C3:** the range of candle 3. This is the old approach.
- **Approach B, GMU3:** the range of all 3 candles.
- **Approach C, C1:** the range of candle 1, treated as the entry candle.

**How the limits work:**
- The limit is placed at the c3 close and waits 10 candles. A level the price is already past fills at the c3 close.
- The bear side is mirrored.
- The tables say **"deep"** for the deepest pullback: XD for a bull GMU, XP for a bear GMU.
- **"Shallow"** is the c3 close.

### Results: all GMUs, both sides, 50 pt stop, 1:2

**"Reacts"** = the trade reaches +50 pts before −50 pts. Random reacts 48–50%.

| Chart | Approach | Deep: fill · avg | BAL: fill · avg | Shallow (c3 close): avg (t) | Reacts |
|---|---|---|---|---|---|
| 5m | C3 | 76% · −0.006 → +0.005 | 93% · +0.001 → +0.007 | +0.002 → +0.009 (0.3 / 0.5) | 50% |
| 5m | GMU3 | 34% · −0.017 → −0.036 | 70% · −0.008 → +0.012 | same | 49–50% |
| 5m | C1 | 35% · −0.017 → −0.037 | 47% · −0.003 → −0.027 | — | 48–50% |
| 15m | C3 | 75% · +0.012 → −0.027 | 93% · +0.032 → +0.017 | +0.040 → +0.020 (3.3 / 0.9) | 51–52% |
| 15m | GMU3 | 31% · −0.023 → −0.081 | 67% · +0.002 → −0.046 | same | 50–51% |
| 15m | C1 | 32% · −0.024 → −0.082 | 44% · −0.018 → −0.083 | — | 50% |
| 1h | C3 | 65% · −0.001 → −0.092 | 87% · +0.058 → −0.029 | +0.072 → −0.016 (3.0 / −0.4) | 51–53% |
| 1h | GMU3 | 22% · −0.056 → −0.231 | 55% · −0.033 → −0.099 | same | 46–53% |
| 1h | C1 | 22% · −0.070 → −0.242 | 31% · −0.057 → −0.230 | — | 46–47% |
| 4h | C3 | 46% · +0.004 → −0.246 | 79% · +0.081 → −0.063 | +0.063 → +0.002 (1.4 / 0.0) | 48–54% |
| 4h | GMU3 | 3% · too few | 29% · +0.054 → −0.145 | same | — |
| 4h | C1 | 3% · too few | 7% · too few | — | — |

**Answer: which approach is best?**
- **A (C3) is best, B (GMU3) is second, and C (C1 as the entry candle) is the worst.**
  - The deeper the limit, the more trades it misses.
  - The C1 levels lose in 2026 on every chart.
- **The best "level" is the c3 close itself (no pullback).** But on its own it is only +0.02 to +0.04 on 15m, and it fails in 2026 on 1h and 4h.
- **No GMU entry has an edge** when every c3 shape is mixed together.

### By the shape of candle 3: the only GMU that held in both periods
**15m GMU where c3 = AFs against:** c3 sweeps c2 and closes leaning against the gap (BeAFs for a bull GMU, BuAFs for a bear GMU). This matches the old "Gold GMC" on 15m.

| 15m, c3 AFs against | Fill | Trades | WR | PF | avg | t |
|---|---|---|---|---|---|---|
| C3 close (market) | 100% | 3,225 → 1,030 | 37.1% → 36.7% | 1.13 → 1.12 | +0.085 → +0.080 | 3.34 / 1.78 |
| C3 MD limit (bull 25%, bear 75%) | 98% | 3,155 → 1,013 | 37.0% → 37.0% | 1.13 → 1.14 | +0.081 → +0.090 | 3.16 / 1.97 |
| C3 D limit (bull 12.5%, bear 87.5%) | 94% → 95% | 3,029 → 976 | 36.2% → 37.2% | 1.08 → 1.15 | +0.053 → +0.095 | 2.03 / 2.05 |
| GMU3 BAL limit | 78% → 76% | 2,509 → 785 | 34.7% → 37.2% | 1.01 → 1.14 | +0.008 → +0.091 | 0.29 / 1.77 |
| C1 P limit | 66% → 61% | 2,139 → 630 | 35.0% → 36.8% | 1.03 → 1.12 | +0.019 → +0.079 | 0.61 / 1.38 |

- **1h GMU, c3 = BC+ with the gap, C3 P 87.5% limit:** +0.176 → +0.077 (t 3.88 / 0.96).
  - Strong in 2022–25 but weak in 2026. Watch it, don't trade it.
- **A small edge, not a big one:** +0.08R per trade is about $8 per trade on 1 MNQ with a 50 pt stop, before slippage.

---

## 2. Inside the XB, before the break (does the Balanced Zone rule hold?)

**Setup:** the limit is live from the first NBC close until the break, and follows the zone as it grows. One trade per block per zone. 50 pt stop, 1:2.

| Chart | BUY XBS top (Balanced bottom) | BUY XBS mid | SELL XBB bottom (Balanced top) | SELL XBB mid | BUY Balanced mid | SELL Balanced mid |
|---|---|---|---|---|---|---|
| 5m | +0.004 → −0.046 | +0.004 → −0.032 | −0.040 → +0.017 | −0.041 → +0.032 | −0.018 → −0.085 | −0.071 → −0.038 |
| 15m | +0.023 → −0.033 | +0.023 → −0.053 | −0.034 → −0.016 | −0.045 → −0.026 | −0.016 → −0.130 | −0.088 → −0.116 |
| 1h | −0.009 → −0.031 | +0.003 → −0.067 | −0.063 → −0.035 | −0.050 → −0.062 | −0.114 → −0.163 | −0.162 → −0.174 |
| 4h | +0.010 → −0.015 | −0.161 → −0.213 | −0.075 → −0.005 | −0.038 → −0.094 | −0.180 → −0.348 | −0.278 → −0.299 |

- **"Never buy or sell inside the Balanced Zone" is CONFIRMED.**
  - The Balanced middle was the worst entry on every chart in both periods.
  - On 1h and 4h it lost 0.11–0.35R per trade.
- **XBS (buy) and XBB (sell) are better places than the Balanced Zone**, but on their own they have no edge: about 0 to −0.05.
- **The XB stop** (just past the block high or low) is worse than the 50 pt stop everywhere. The block edge gets swept too often.

---

## 3. After the break: the FVA (wait for a touch? BC or immediate?)

**What price does after a break (all charts, both periods):**
- About 80% of breaks come back to touch the FVA within 50 candles, and about half within 5 candles.
- **The touch candle's close:**
  - **Closes back out (≈50% of touches):** the FVA held. A limit at the edge then made +0.45R → +0.56R on 1h (WR 49% → 53%) and +0.12R → +0.18R on 5m.
  - **Closes inside (≈33%):** the FVA broke within 20 candles 67–85% of the time, and the trade lost (1h: −0.35R → −0.46R). **Max's idea is right:** a close back inside means a deeper pullback, not continuation.
  - **Closes through (12–21%):** the FVA is broken.
- **But you only know at the close.** Entering after the close-back-out (E5) gave no edge (1h −0.02 → −0.11).

**Entries (50 pt stop, 1:2, avg old → 2026):**

| Entry | 5m | 15m | 1h | 4h |
|---|---|---|---|---|
| E0: immediate, market at the break close | −0.015 → −0.016 | +0.018 → −0.001 | +0.012 → +0.035 | +0.100 → −0.065 |
| E1: limit at the FVA near edge (wait for the touch) | −0.015 → +0.003 | −0.001 → −0.057 | −0.034 → −0.046 | −0.048 → +0.012 |
| E2: limit at the FVA middle | −0.017 → +0.023 | −0.022 → −0.057 | −0.050 → −0.055 | −0.131 → +0.008 |
| E3: limit at the FVA far edge | −0.025 → −0.002 | −0.030 → −0.081 | −0.086 → −0.018 | −0.024 → −0.145 |
| E4: touch, then the first BC (market at its close) | −0.013 → +0.020 | +0.022 → −0.006 | −0.043 → +0.065 | +0.088 → +0.022 |
| E5: touch candle closes back out (market at its close) | −0.008 → −0.047 | +0.002 → −0.050 | −0.016 → −0.111 | +0.020 → +0.193 |
| E6: break is a GMU (market at the c3 close) | −0.008 → +0.040 | +0.059 → +0.023 | +0.056 → −0.029 | +0.003 → −0.138 |
| E7: break is a GMU, then a limit at the FVA | −0.018 → +0.036 | −0.010 → −0.097 | −0.044 → −0.116 | −0.138 → −0.087 |

- **No entry passed in both periods.** Immediate, touch, and touch+BC are all close to random.
- **Answer to "touch or not, BC or immediate":**
  - Waiting for the touch does not beat the immediate entry.
  - Adding the BC after the touch is a little better than the touch limit on 1h in 2026 (+0.065), but it is not proven.
- **The FVA zone stop** (just past the far edge) is worse than the 50 pt stop on every chart.
- **Continuation vs reversal breaks:** continuation breaks (in the BC's direction) are a little better (15m E4: +0.066 → 0.000; 1h E0: +0.019 → +0.091). Still not an edge.

---

## 4. GMU + FVA relationship

**Break candle = a GMU** (the next candle leaves a gap): 54–60% of all breaks.

| Chart | Break type | FVA touched | Touched within 5 candles | FVA broken later |
|---|---|---|---|---|
| 5m | plain break | 90% | 71% | 72% |
| 5m | GMU break | 74% | 31% | 56% |
| 1h | plain break | 90% | 70% | 72% |
| 1h | GMU break | 74% | 30% | 56% |
| 4h | plain break | 92% | 78% | 78% |
| 4h | GMU break | 74% | 29% | 60% |

- **A GMU break is the stronger break:** the FVA comes back later and lives longer.
- **Do not trust the "GMU break wins" number.** Looking back, a GMU break entered at the break close made +0.32R → +0.35R on 1h. But that uses the next candle, which you cannot know at the break. The honest entry once the gap is confirmed (E6) is flat.
- **The last opposite GMU at the break:**
  - It was already broken earlier 65–70% of the time.
  - It was broken by this same break 9–10% of the time.
  - It was still alive 20–25% of the time.
  - Results barely change between these three cases.

---

## Verdict
1. **Use the XB as a MAP, not an entry.**
   - Never trade inside the Balanced Zone (proven).
   - XBS / XBB are the better places, but they need another trigger.
2. **After a break, expect the FVA to be retested** (80%). If the touch candle closes back INSIDE, expect a deeper pullback or a failed FVA (about 70%).
3. **GMU ladder:**
   - C3 > GMU3 > C1.
   - The only GMU entry that held in both periods is the 15m GMU with c3 = AFs against: c3 close, or a C3 MD/MP limit at about 98% fill, +0.08 to +0.09R, t 2.0–3.3.
4. **Nothing here beats the live EDGE PRO setups.**

## Files
- **Indicator:** `claude/MMM_PRO_x_4.0.pine`.
- **Engine (session files):** /home/claude/xb/: core.py, xbeng.py, gmu.py, xbtest.py, agg_gmu2.py, agg_xb.py.

---

## 5. GMU full stop grid (added Oct 30): every entry × every stop × every target × every exit

Results sheet (artifact): **MMM GMU Stop Grid**. It has an entry × stop matrix and a full filterable sheet.

**What was paired, one by one:**
- **Entries:** 3 ranges (C3, GMU3, C1) × 7 ladder levels (XD 0 · D 12.5 · MD 25 · BAL 50 · MP 75 · P 87.5 · XP 100).
  - Bear is mirrored, so XD = the deepest pullback.
  - A limit waits 10 candles and is cancelled if a close goes through the GMU open first.
- **Stops (13):**
  - fixed 50 pt;
  - 1.5 × ATR;
  - past the GMU low/high (3 candles);
  - past the GMU open (c2 open);
  - past the gap edge (c1 high/low);
  - past the c3 low/high;
  - past XD + 12.5% of the range;
  - past each deeper ladder level of the same range (XD, D, MD, BAL, MP, P).
  - All stops sit 2 ticks past the level. A risk under 4 pts is skipped.
- **Targets:** 1:1, 1:1.5, 1:2, 1:3, 1:4, 1:6.
- **Exits:**
  - stop/target only (100 candles);
  - violation exit = a close through the GMU open;
  - gap filled = a close through c1;
  - hold to the next session open (02:00, 08:00, 09:30 NY).
- **Groups:** all c3 shapes together, plus each c3 shape (family × with/against) separately.

**Results:**
- **99,480 combos had enough trades (≥100 old, ≥40 in 2026). 90 pass t-score ≥ 2 in both periods.** They fall in 3 groups:
  - **15m, c3 = AFs against (63 combos):**
    - C3 XD limit · 1.5×ATR stop · 1:3: WR 28.8% → 30.4%, PF 1.10 → 1.24, avg RR +0.073 → +0.169, t-score 2.23 / 2.86.
    - GMU3 P · stop past D of the 3-candle range · 1:3 · exit on a close through the GMU open: WR 26.9% → 27.8%, PF 1.12 → 1.23, avg RR +0.082 → +0.148, t-score 2.77 / 2.78.
    - C3 MD limit · stop past the GMU low · 1:3: avg RR +0.080 → +0.141, t-score 2.55 / 2.52.
    - 50 pt stop · 1:2 (C3 D limit): avg RR +0.052 → +0.100, t-score 2.02 / 2.17.
  - **1h, c3 = BC+ with the gap (21 combos):** c3 close · stop past MD of c3 (a tight stop under the strong close) · 1:2: WR 37.7% → 40.5%, PF 1.14 → 1.32, avg RR +0.092 → +0.192, t-score 2.07 / 2.41. 1:3: avg RR +0.114 → +0.221.
  - **4h, c3 = BC− with (6 combos, small):** GMU3 P · stop past the GMU open · 1:1: WR 57.4% → 61.9%, avg RR +0.139 → +0.233, t-score 2.14 / 2.18, only 235 → 84 trades.
- **Stops on the C3 ladder lose.** Past XD, D, MD and so on are too close: they get swept and the cost eats the small risk.
  - 15m AFs against, MD entry, stop past D: avg RR −0.29 → −0.63.
  - **Exception:** after a STRONG c3 (1h BC+ with), a stop under its MD/D works.
- **The best stops overall** are 1.5×ATR, 50 pt, and past the GMU low/high.
- **All c3 shapes together:** nothing passes. The best is 15m GMU3 XP · stop past D · 1:6 · exit on a close through the GMU open: avg RR +0.036 → +0.076, t-score 1.86 / 2.20.
- **Walk-forward test:** the top 200 combos picked on 2022–25 stayed positive in 2026 84% of the time, but their avg RR fell from +0.11 to +0.05. All combos together average −0.09 in 2026.
- **Picking the best of about 100,000 combos fools you.** Trust the 15m AFs-against group most: it was found before (the Gold GMC), it shows up in 63 combos, and 99% of its top 100 stayed positive in 2026.

---

## 6. GMU entry map: bull and bear tested apart (added Oct 30)

The results sheet is the same artifact, **MMM GMU Stop Grid**, now titled "MMM GMU Entry Map" on the page. It has 3 views:
- an entry ranking for each chart, side and c3 type;
- an entry × stop matrix;
- the full sheet.

**What was tested:**
- **Entries (35):**
  - the ladder XD 0 · D 12.5 · MD 25 · BAL 50 · MP 75 · P 87.5 · XP 100 on 4 ranges: GMU3 (all 3 candles), C1, C2 and C3. Names are always measured from the candle LOW, with no mirroring.
  - c1 open, c1 close, c2 open, c2 close, c3 open, c3 close, and the gap middle.
- **Stops (11):**
  - 50 pt;
  - 1.5 × ATR;
  - past the GMU3 low/high;
  - past c1 low/high;
  - past the gap edge (c1 high/low);
  - past the c2 open (GMU open);
  - past c2 low/high;
  - past c3 low/high;
  - past the c3 open;
  - past the entry range's own end;
  - past the GMU3 BAL.
- **Targets:** 1:1 to 1:6.
- **Exits:** stop/target only, a close through the GMU open, gap filled, or hold to the next session open.
- **Groups:** all GMUs, c3 = BC with the gap, c3 = NBC, and the 12 c3 shapes.
- **Limit rules:** a limit waits 10 candles. A level that price is already past fills at the c3 close.

**Random baseline** (market at a candle close, 50 pt, 1:2), avg RR old → 2026:

| Chart | Random longs | Random shorts |
|---|---|---|
| 5m | +0.022 → +0.001 | −0.047 → −0.007 |
| 15m | +0.043 → +0.004 | −0.042 → −0.033 |
| 1h | +0.055 → +0.027 | −0.058 → −0.071 |
| 4h | −0.100 → +0.071 | +0.025 → −0.065 |

**Results:**
- **837 combos pass t-score ≥ 2 in both periods, and all 837 are BULL GMUs.** Not one bear GMU combo passes; the best bear combo has t-score 2.1 / 1.7. Bear GMUs lose at most entries.
- **The best candle is C3.** The winners are the c3 close, or shallow C3 / GMU3 levels. These lose or rarely fill:
  - C1 levels;
  - c1 open and c1 close;
  - c2 open;
  - the gap middle.
- **Max's specific entries:**
  - **c2 open when c3 is NBC:** avg RR at 50 pt, 1:2 is +0.025 → −0.078 on 15m bull, +0.058 → −0.049 on 1h bull, and −0.10 → −0.49 on 4h bull. No.
  - **c3 open when c3 is BC:** +0.037 → −0.026 on 15m bull and +0.064 → −0.076 on 1h bull. No.
  - **c3 low (C3 XD) when c3 is BC:** +0.024 → −0.070 on 15m bull. No.
  - **c3 close when c3 is NBC:** the best is 15m bull, stop past c1 low, 1:3: +0.065 → +0.132, t-score 2.2 / 2.5.

**The best entry per chart (BULL GMU):**

| Chart | Group | Entry | Stop | Target · exit | Trades | WR | PF | avg RR | t-score |
|---|---|---|---|---|---|---|---|---|---|
| 5m | c3 NBC | C3 MD limit (25% of c3) | 50 pt | 1:4 · stop/target | 8,872 → 1,427 | 37.9% → 29.9% | 1.09 → 1.25 | +0.050 → +0.177 | 3.14 / 3.44 |
| 15m | all | GMU3 MP limit (75% of 3 candles) | past c1 low | 1:3 · stop/target | 6,615 → 2,085 | 29.6% → 30.0% | 1.08 → 1.15 | +0.061 → +0.107 | 2.88 / 2.78 |
| 15m | c3 AFs against | C3 XD limit (c3 low) | 1.5×ATR | 1:3 · gap filled | 1,524 → 486 | 19.9% → 20.4% | 1.24 → 1.41 | +0.111 → +0.172 | 3.08 / 2.67 |
| 1h | c3 BC+ with | c3 close | past c2 open (GMU open) | 1:1 · gap filled | 658 → 201 | 56.4% → 59.7% | 1.30 → 1.51 | +0.128 → +0.200 | 3.36 / 2.93 |
| 4h | all | c3 close | 1.5×ATR | 1:6 · gap filled | 590 → 182 | 20.2% → 22.5% | 1.42 → 1.78 | +0.271 → +0.464 | 2.81 / 2.48 |

**Caveats:**
- NQ went up in both periods, so random longs also made money. Compare every bull row with the random-long line: the winners above are 2–5 times the random number.
- The 15m AFs-against GMU from section 1 is a BULL-only edge (87 bull combos pass, 0 bear).


## 7. Max's read: sell in discount (XBS), buy in premium (XBB) — added Oct 30

**Setup:** stop orders live from the first NBC close until the break. SELL stop when price drops into the XBS (at its top = Balanced bottom, or its middle). BUY stop when price rises into the XBB (at its bottom = Balanced top, or its middle). One trade per block per zone. 50 pt stop, 1:2, 1 pt cost. Every XB (4.0 logic).

| Chart | SELL at XBS top | SELL at XBS mid | BUY at XBB bottom | BUY at XBB mid |
|---|---|---|---|---|
| 5m | −0.035 → +0.006 | −0.040 → −0.010 | +0.014 → −0.049 | +0.010 → −0.049 |
| 15m | −0.039 → −0.059 | −0.042 → −0.072 | +0.036 → −0.097 | +0.037 → −0.134 |
| 1h | −0.056 → −0.017 | −0.063 → −0.097 | +0.025 → −0.062 | +0.013 → −0.103 |
| 4h | −0.032 → −0.110 | −0.004 → −0.461 | +0.000 → −0.051 | −0.020 → −0.131 |

(avg RR 2022–25 → 2026; WR 30–40%, PF 0.81–1.06.)

- **No edge either way.** The old read (buy XBS / sell XBB limits) was about 0 to −0.05. Max's read (sell XBS / buy XBB stops) is about the same: −0.02 to −0.13 in 2026.
- **The zones are a map, not an entry.** They show where each side traded. A trade needs a trigger on top (the break, the FVA, a GMU).
- The indicator now uses Max's names and colors: XBS = sell (purple), XBB = buy (teal).
