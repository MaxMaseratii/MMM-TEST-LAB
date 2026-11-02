# Fair Value Area Break: strategy grid results (Oct 20, 2026 · corrected)

Indicator: MMM Perfect Entry: Fair Value Area Break @MaxMaserati. Version **4.1** (`claude/MMM_FVA_Break_4.1.pine`) keeps only what passed: FVA.M1 and FVA.M2.

## ⚠ What changed since the first grid (same day)
- The first grid said 4 strategies passed on the flip zones (3.2 FVA.M1–M4, ② PES/PEL+ and ④ CDL/CDS+ touches).
- **That was a bug.** A ② / ④ touch only counted if that same candle did not close through the box. A waiting limit order would have been filled on those candles, and most of them are losers.
- **Honest rule:** the limit is live from the prior close, so every touch counts.
- Re-run: **0 of ~30,000 ② / ④ combos pass**, same as random trades. The 3.2 strategies are dropped.

| 15m, fixed 50 pt stop | First test (bug) NQ 23-25 → MNQ 26 | Honest NQ 23-25 → MNQ 26 |
|---|---|---|
| 3.2 M1 ② POC · 1:2 · 2-NBC exit | WR 57% · avg RR +0.14 (t 7.5) → +0.22 | WR 48% · avg RR −0.01 (t −0.4) → −0.01 |
| 3.2 M2 ④ edge · 1:2 · 2-NBC exit | WR 55% · +0.11 (t 6.5) → +0.21 | WR 48% · +0.00 (t 0.1) → 0.00 |
| 3.2 M3 ② POC · flip TGT · opp-BC exit | WR 67% · +0.09 (t 9.6) → +0.18 | WR 49% · −0.03 (t −3.9) → −0.02 |
| 3.2 M4 ② POC · 1:2 · opp-BC exit | WR 46% · +0.13 (t 7.5) → +0.16 | WR 34% · −0.03 (t −2.0) → −0.05 |

**Also tested, honest:** wait for the touch candle to CLOSE and hold the box, then enter at that close, or with a new limit for 5 candles. **0 combos pass** on 5m, 15m and 1h.

## Test setup (the established MMM engine)

**Entries:**
- ① PES/PEL, ② PES/PEL+, ③ CDL/CDS, ④ CDL/CDS+, Nested: limit orders at the level (honest touch rule for ② ④).
- ② / ④ "hold": enter after the touch candle closes and holds the box.
- ⑤ BuX/BeX and ⑥ LQG: market at the close, or a limit at the candle open.
- "Fail" and "Fail+": a close through an FVA box / a flip zone, traded in the break direction at that close.
- RANDOM trades as the luck check.

**Split by:** long / short / both × Asia 18–02 / London 02–08 / NY 08–13:30 / PM 13:30–18 / All.

**Stops:** fixed 50 · the indicator's box stop · the swing stop · ATR×1 · ATR×1.5 · daily ATR×0.15.
**Targets:** 1:1, 1:1.5, 1:2, 1:3, 1:4, 1:6, flip candle high / low.
**Exits (12):** none · opposite BC · 2 / 3 / 4 NBC · 3 NBC variants · 3 stall / SuperTrend exits · hold to the next session open.

**Engine rules:** limits need 1 tick through · stop wins when one candle touches both · 1 pt cost · 100-candle limit · stops under 2 pts skipped.

**Data:** NQ Dec 2022 – Dec 2025 (5m / 15m / 1h, 1m replay) · MNQ 2026 (1m replay, 5m where 1m is missing).

**Pass rule:** positive with a t-score of 2+ in BOTH periods (NQ ≥ 100 trades, MNQ ≥ 30).

## Pass rate by entry (honest)

| Entry | 15m | 5m | 1h |
|---|---|---|---|
| **Fail+ (flip zone broken)** | 0% | 0% | **2.7%** (longs) |
| Fail (FVA box broken) | 0.06% | 0.02% | 0.5% (longs) |
| ② PES/PEL+ / ④ CDL/CDS+ touch | 0% | 0% | 0% |
| ② / ④ hold (close, then enter) | 0% | 0% | 0% |
| ⑤ BuX/BeX | 0.02% | 0.02% | 0.04% |
| ① ③ nested ⑥ | ~0% | ~0% | ~0% |
| **RANDOM (luck)** | **0%** | **0%** | **0%** |

## Idea grid: 12 more entries (all decided at a candle close)

Each with 6 stops × 8 targets (1:0.5, 1:1, 1:1.5, 1:2, 1:3, 1:4, 1:6, candle target) × 12 exits × side × session, on 5m / 15m / 1h / 4h. Same pass rule.

| Idea | What it is | 5m | 15m | 1h | 4h |
|---|---|---|---|---|---|
| **Fail+C** | close through a flip zone, trade the break | 0% | 0% | **3.3%** | 0% |
| **FailC** | close through an FVA box, trade the break | 0% | 0.09% | **1.1%** | **1.2%** |
| Fail+C RT / FailC RT | limit back at the broken edge, 5 candles | 0% | 0% | ~0% | 0% |
| FlipBC | the flip candle itself | 0% | 0% | 0% | 0% |
| BrkBC | the BC that breaks an FVA box | 0.03% | 0.03% | 0.09% | 0.05% |
| Rej Zone / Rej FVA | first retest wicks in and closes back out | 0% | 0% | 0% | 0% |
| G3 Zone / G3 FVA | grey-phase rejection (the green / red border) | 0% | 0% | 0% | — |
| Sig Zone / Sig FVA | a nested box breaks out | 0.07% | 0% | 0% | 0% |
| RANDOM | luck check | 0% | 0% | 0% | 0% |

**Verdict:** the only edge in this indicator is **failure**. When price CLOSES through a box, trade with the break, on 1h (and 4h). Touches, rejections, retests and the BCs themselves are luck.

**WR above 50% that passed:**
- 48 combos. Almost all are 1h Fail+C in Asia (both sides) or 1h / 4h FailC.
- After keeping one trade per candle:

| Pick | Trades | WR | PF | avg RR | t-score | Note |
|---|---|---|---|---|---|---|
| **1h Fail+C · Asia · both · zone stop · 1:1.5 · no exit (FVA.M2)** | 153 | **56%** | 1.81 | **+0.37** | 3.6 | 2023 +0.18 · 2024 +0.23 · 2025 +0.50 · 2026 +0.45 |
| 1h Fail+C · Asia · both · fixed 50 · 1:1.5 · 2-NBC stall (M2 fixed) | 153 | 56% | 1.86 | +0.34 | 3.6 | 2026 WR 65% |
| 1h Fail+C · Asia · both · zone stop · 1:1 · 4 NBC | 153 | 65% | 1.68 | +0.24 | 3.2 | highest WR, smaller RR |
| 1h FailC · Asia · both · fixed 50 · 1:1.5 · hold to next session | 578 | 51% | 1.41 | +0.13 | 3.5 | 2026 t 1.7: watch |
| 4h FailC · Asia · both · daily ATR × 0.15 · 1:0.5 · hold | 126 | 73% | 1.81 | +0.15 | 3.0 | 2026 only 23 trades: watch |
| 4h FailC · long · swing stop · 1:1 | 405 | 57% | 1.30 | +0.13 | 2.6 | stops ≈ 300 pts: not practical |

- FVA.M2: longs and shorts both made money in both periods (2026 shorts WR 71%).
- A Python copy of the M2 rules matched the test engine on all 119 NQ trades (zone stop and fixed).

## Strategies that passed

### FVA.M2 · Asia Flip Zone Fail · BOTH (1h) — WR above 50%
- Asia only: the 1h candle that opens 18:00 – 01:00 New York.
- A close ABOVE a PES+ zone → buy at that close. A close BELOW a PEL+ zone → sell at that close.
- Stop = the far side of the zone ± 4 ticks (≈ 46 pts 2023–25, ≈ 99 pts 2026). Target 1:1.5. No early exit. 100-candle limit.
- NQ 2023-25: 119 trades · WR 55% · PF 1.73 · avg RR +0.34 · t 3.0.
- MNQ 2026: 34 trades · WR 59% · PF 2.08 · avg RR +0.45 · t 2.1.
- Both: 153 trades · WR 56% · PF 1.81 · avg RR +0.37 · t 3.6 · max 6 wins / 6 losses in a row · max DD 8.0 avg RR.
- Per 1 MNQ contract: W: +$14,206 · L: −$8,313 · Net: +$5,893.
- Fixed 50 option (2-NBC stall exit): WR 56% · PF 1.86 · avg RR +0.34 · t 3.6 · W: +$11,428 · L: −$6,152 · Net: +$5,275 · max DD 5.1 avg RR.
- Watch-outs: only about 3 trades a month, and only 34 trades in 2026.

### FVA.M1 · Flip Zone Fail · LONG (1h)

**Rule:**
- A bearish flip zone (PES+ box) = the body of the last bullish BC before sellers flipped the trend.
- A 1h candle CLOSES ABOVE the top of that box → the sellers failed → **buy at that close**.
- Stop = yesterday's daily ATR(14) × 0.15 (≈ 46 pts in 2023–25, ≈ 82 pts in 2026).
- Target = 1:4.
- Early exit = at the close of the 2nd neutral candle (NBC) in a row when both close in their upper half (the push stalls). The check starts on the 2nd candle after the entry.
- Time limit 100 candles. One trade per candle.
- Only a close ABOVE the box counts. 36 odd test rows where a "significant" box broke DOWN were removed.

**Results (honest, market at the close, stop first on 1m, 1 pt cost):**

| Data | Trades | WR | PF | avg RR | t-score |
|---|---|---|---|---|---|
| NQ 2023-25 | 402 | 36% | 1.47 | +0.30 | 3.1 |
| MNQ 2026 | 51 | 45% | 2.22 | +0.63 | 2.2 |
| **Both 2023-26** | **453** | **37%** | **1.54** | **+0.33** | **3.7** |
| NQ 2023 | 141 | 35% | 1.39 | +0.25 | 1.5 |
| NQ 2024 | 142 | 37% | 1.63 | +0.40 | 2.4 |
| NQ 2025 | 119 | 37% | 1.38 | +0.23 | 1.4 |

- Both periods: max wins in a row 8, max losses in a row 15, max DD 18.8 avg RR.
- Per 1 MNQ contract, both periods: **W: +$43,885 · L: −$27,492 · Net: +$16,393**.
- Positive in every session (Asia, London, NY, PM).
- Random 1h longs with the same stop / target / exit: NQ −0.03 → MNQ +0.11.
- **Fixed 50 pt stop:** at 1:4, +0.20 → +0.45 (2026 t 1.5); at 1:2, +0.13 (t 2.0) → +0.20 (t 1.0). Weaker than the daily ATR stop.

**Not edges:** the short mirror (bull flip zone broken down = short): 0 passes. Fail+ on 15m / 5m: 0 passes. The FVA-box failure long (Fail) passed on 1h with a 1:6 target, but drops to t 1.5 when one trade per candle is kept, and 2025 was flat. It is not added.

**Watch-outs:**
- Long only, 1h only.
- Only 51 trades in 2026.
- Plan on about half of the tested avg RR.

## What 4.1 does (4.0 + FVA.M2)
- **Removed:** entries ① – ⑥, nested entries, LQG labels and entries, BuX/BeX entries, FVA.M1–M4 of 3.2, MMPD / trend filters, entry cycle limits, prop-firm $ sizing, the volume-profile drawing.
- **Strategies FVA.M1 and FVA.M2** as above. They trade on a 1h chart only (input to allow other charts, marked untested). M2 has a stop choice: zone (tested best) or fixed 50 / 20. Alerts on every buy, sell and exit.
- **Grading:** 1m intrabar, stop first, the same rules as the test. A Python mirror of the trade rules matched the test engine on all 402 NQ trades.
- **Drawing (MMM Pro style):** everything is redrawn from state on the last bar.
  - Flip zones PEL+ / PES+: max per side (default 3), newest first. A zone dies with its trigger line, POC, flip label, target and swing lines when a candle closes through it.
  - PES+ zones show "PES+ · M1·M2" and a trigger line "M1·M2 ▲ close > price". PEL+ zones show "M2 ▼ close < price (Asia)".
  - FVA boxes: max per side (default 2) plus the forming box.
  - Trades: open trades always drawn, plus separate keep counts for winners and losers.
  - One "ALL Labels" size switch plus per-item sizes, and line extension in candles.
- **Tables (FVA 3.0 look: black, dark grey rows, gold headers):**
  - LIVE (top right, the only one on by default): each strategy shows only when ARMED, IN TRADE, or DONE TODAY (M2 is armed only in Asia).
  - INFO: one column per strategy: the rule, the tested numbers (blended 2023–26) and this chart's numbers (WR, PF, avg RR, t-score, streaks, max DD, W: +$ · L: −$ · Net).
  - GUIDE: how to read it.
- **Input order:** Account & Risk → Strategy → Trades → Flip Zones → FVA boxes → Candles → Labels → Tables.

## Ranking check (Oct 25): are M1 and M2 the most profitable?
All 222 idea-grid passes were re-run one trade per candle. 89 still pass. 72 of those are also positive in every NQ year. Each was compared with random trades that use the same stop, target and exit.

| Strategy (1h unless noted) | Trades / month | WR | avg RR | Profit / month (avg RR) | Profit ÷ worst DD | Edge over random (2023-25 → 2026) |
|---|---|---|---|---|---|---|
| **FVA.M2** Asia Flip Zone Fail · both · 1:1.5 | 3.8 | **56%** | +0.37 | 1.3 | 7.0 (fixed 50 + stall exit: 10–15) | +0.31 → +0.53 |
| **FVA.M1** Flip Zone Fail · long · 1:4 | 11.2 | 38% | +0.35 | 3.9 | 8.5 | +0.33 → +0.64 |
| FVA Box Fail · long · NY 08-13:30 · daily ATR × 0.15 · 1:6 · 2-NBC stall | 14.9 | 34% | +0.33 | **4.9** | 7.7 | +0.16 → +0.66 |
| FVA Box Fail · long · all · ATR × 1 · 1:6 · hold to next session | **37.2** | 43% | +0.15 | **5.7** | 7.2 | +0.09 → +0.28 |
| 4h FVA Box Fail · long · ATR × 1.5 · 1:6 (stop ≈ 200 pts) | 9.9 | 27% | **+0.50** | 5.0 | 5.6 | +0.27 → +1.13 |
| Flip Zone Fail · long · zone stop · 1:6 · SuperTrend exit | 11.4 | 27% | +0.38 | 4.3 | 8.2 | +0.36 → +0.97 |
| Break BC · long · daily ATR · 1:6 | 69.8 | 30% | +0.12 | 8.4 | 4.0 | +0.10 → +0.14 (mostly market drift) |
| 5m Sig FVA · long · fixed 50 · 1:6 | 276 | 38% | +0.06 | 16.6 | 3.1 | +0.01 → +0.21 (rejected: drift only) |

**Answer:**
- **WR above 50%:** M2 is #1. Nothing else with WR above 50% beats its avg RR. The fixed 50 + stall exit version has the best profit ÷ DD of all 72.
- **avg RR:** M1 is near the top. Only the 4h box-fail long (+0.50, stops ≈ 200 pts) and the same flip-zone family with a 1:6 target (+0.38) are higher.
- **Total profit at the same risk per trade:** M1 and M2 are NOT the biggest. FVA Box Fail longs on 1h trade 1.5–3× more often and make more per month (4.9 – 5.7 avg RR a month, vs M1 3.9).
