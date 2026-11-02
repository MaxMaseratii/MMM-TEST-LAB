# Fair Value Area Break 3.0: re-test results (Oct 19, 2026 · corrected Oct 20)

Indicator: "MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.0", default inputs.
How the test was run:
- Claude rebuilt the indicator candle by candle in Python and scored every setup it makes, using the MMM Data Library.
- On the Oct 12–16 MNQ 15m week, the copy reproduces the chart's stats table.

## ⚠ Correction (Oct 20)
- **The first re-test was wrong about ② and ④.** It took a ② / ④ touch only if that same candle did NOT close through the box. The indicator does the same.
- That hides the losers. A trader's limit order is already waiting, so it gets filled even when the candle later breaks the box.
- **Honest rule:** the limit is live from the prior close, so every touch counts.
- After the fix, **④ CDL/CDS+ is flat (avg RR +0.01, −0.10 after fees)** and **② PES/PEL+ loses (−0.13)**. No touch entry has an edge.
- The only setup that passed is in 4.0: **FVA.M1 · Flip Zone Fail (1h, long only)**. See `claude/MMM_FVA_Strategy_Grid_Results.md`.

## Verdict
- The table's **86.9% WR (win rate) at 1:2 is not real.**
- With fills a trader can really get, the indicator as a whole has **WR ~32%, avg RR −0.04, PF 0.94**, and it loses money after fees.
- **No entry ① – ⑥ holds up** with honest fills.

## Why the table is wrong (code bugs in the stats engine)
1. **Graded on the opening candle.**
   - The trade is created at the candle's close, then checked against the same candle's high and low.
   - 50–87% of all results are decided on that candle (NQ 15m: ③ CDL/CDS 86%, ⑤ BuX/BeX 77%, ⑥ LQG 78%).
2. **Target checked before stop.** When one candle touches both, the trade counts as a win.
3. **⑤ BuX/BeX and ⑥ LQG enter at the candle OPEN after the candle closed.**
   - That price is in the past. Low ≤ open is always true, so the trade is "filled" instantly.
   - A bullish candle has already moved away from its open, so the trade starts in profit.
4. **Only the last 500 bars are counted** ("Limit Historical Bars"). On 15m that is about one week.
5. **(found Oct 20) ② / ④ skip a touch when that candle closes through the box.** The box check runs before the entry on the same candle.

Proof (MNQ 15m, Oct 14): four trades whose candle touched both the stop and the target. The indicator counted all four as wins.
- 12:15 ③ long
- 12:30 ⑤ BuX
- 13:45 ⑤ BeX
- 15:15 ③ short

## Copy check (MNQ 15m, Oct 12–16 vs the chart table, Oct 12–19)

| Entry | Chart table | Python copy (indicator math) | Real fills (first re-test) |
|---|---|---|---|
| PES/PEL | 54/23 (70%) | 61/24 (72%) | 23/61 (27%) |
| PES/PEL+ | 6/1 (86%) | 7/4 (64%) | 5/6 (45%) |
| CDL/CDS | 72/9 (89%) | 83/6 (93%) | 28/61 (31%) |
| CDL/CDS+ | 8/7 (53%) | 10/9 (53%) | 6/13 (32%) |
| Nest PES/PEL(+) | 12/4 (75%) | 14/3 (82%) | 4/13 (24%) |
| Nest CDL/CDS(+) | 20/2 (91%) | 27/1 (96%) | 6/22 (21%) |
| BuX/BeX | 143/8 (95%) | 138/7 (95%) | 27/64 (30%) |
| LQG Brk | 42/0 (100%) | 50/4 (93%) | 9/25 (26%) |

## Methods
- **Real fills.**
  - Touch entries ①②③④ fill at the first 1m bar that touches the level. ② / ④ count every touch while the limit is live (Oct 20 fix).
  - If that 1m bar also hits the stop, it is a loss. The target only counts from the next 1m bar.
  - ⑤ and ⑥ enter with a market order at the candle close, with the same stop and the target redrawn at 2R.
- **Limit at open.** ⑤ and ⑥ use a limit order at the candle open, working from the next candle. The order is missed if the target comes first.
- **Fixed stop.** Same real entries, with a 50 pt stop (NQ/MNQ) or a 20 pt stop (MES) at 1:2.
- **Scoring rules.**
  - A 1m bar touching both the stop and the target is a loss. No slippage is added.
  - Fees are $1.50 per micro contract round trip.
  - Sizing is the indicator's own: $225 risk per trade, and a trade is skipped if its risk is above $236.
- **Data.**
  - NQ 1m Dec 2022 – Dec 2025.
  - MNQ and MES 15m Dec 2025 – Oct 2026. Their real-fill rows use only the days that have 1m bars (Mar–May and Sep–Oct 2026).

## Real fills, NQ 15m Dec 2022 – Dec 2025 (honest)

| Entry | Trades | WR | PF | avg RR | t-score | avg RR after fees |
|---|---|---|---|---|---|---|
| All entries | 61,318 | 31.8% | 0.94 | −0.04 | −7.7 | −0.19 |
| ① PES/PEL | 12,832 | 29.5% | 0.84 | −0.11 | −9.4 | −0.32 |
| ② PES/PEL+ | 2,334 | 29.1% | 0.82 | −0.13 | −4.6 | −0.40 |
| ③ CDL/CDS | 13,580 | 31.1% | 0.91 | −0.06 | −4.9 | −0.26 |
| ④ CDL/CDS+ | 2,628 | 33.6% | 1.01 | +0.01 | 0.3 | −0.10 |
| Nest PES/PEL(+) | 3,239 | 30.0% | 0.86 | −0.10 | −4.1 | −0.31 |
| Nest CDL/CDS(+) | 3,761 | 32.8% | 0.99 | −0.01 | −0.2 | −0.23 |
| ⑤ BuX/BeX (market at close) | 16,770 | 33.6% | 1.01 | +0.01 | 0.8 | −0.05 |
| ⑥ LQG (market at close) | 6,174 | 33.7% | 1.02 | +0.01 | 0.6 | −0.04 |

For comparison, the indicator's own math on the same setups says WR 81.3%, avg RR +1.45.
The first re-test said ④ = WR 41%, avg RR +0.23 (t 7.3) and ② = +0.11. That was bug 5.

## ④ CDL/CDS+ everywhere (real fills, box stop, honest)

| Data | Trades | WR | avg RR | t-score | after fees |
|---|---|---|---|---|---|
| NQ 15m 2023 | 887 | 33.7% | +0.01 | 0.2 | −0.12 |
| NQ 15m 2024 | 873 | 32.2% | −0.03 | −0.7 | −0.15 |
| NQ 15m 2025 | 858 | 35.2% | +0.06 | 1.1 | −0.03 |
| NQ 1h 2023-25 | 626 | 33.2% | −0.00 | −0.1 | −0.07 |
| NQ 5m 2023-25 | 8,135 | 32.0% | −0.04 | −2.6 | −0.20 |
| MNQ 15m 2026 (1m days) | 209 | 33.5% | +0.01 | 0.1 | −0.06 |
| MES 15m 2026 (1m days) | 157 | 29.3% | −0.12 | −1.1 | −0.21 |

With the fixed 50 pt stop at 1:2: ④ NQ 15m +0.04 (t 1.5), MNQ 15m 2026 +0.08 (t 0.8). ② NQ 15m +0.03 (t 1.1). Not edges.

## Fixed versions
- **3.1** (`claude/MMM_FVA_Break_3.1.pine`): next-candle grading, stop first, 1m intrabar grading, ⑤⑥ at the close, fees input, 2000-bar history.
- **3.2**: added FVA.M1–M4. **Do not use**: they came from bug 5.
- **4.0** (`claude/MMM_FVA_Break_4.0.pine`): old entries removed. One tested strategy, FVA.M1 (1h, long). MMM Pro-style drawing.
