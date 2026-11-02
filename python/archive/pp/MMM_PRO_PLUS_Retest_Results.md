# MMM PRO PLUS retest on real data (Nov 2 2026)

Replaces the Oct 10 "MMM PRO PLUS — Final Research Report", which was built from TradingView table screenshots (2m = 39 days, 5m = 102 days). Results sheet: artifact **"MMM PRO PLUS Retest"** (https://claude.ai/artifact/LVDg9RfzbNoY4mzzWVF37L). Research only, not advice.

## How it was run
- The PRO PLUS engine was copied line by line from the indicator script into Python (pp/engine.py):
  - SuperTrend 14 × 2
  - stair candles, the EXIT POINT and stall zones
  - EXIT labels and REJ marks
  - the after-EXIT tests: 50% line, ST rejection, resumption BC, GMC, box break
- It runs the 11 Table 3 setups with the same trade rules:
  - The trade ends on the first of: an EXIT label in your direction, a SuperTrend flip against you, or the stop.
  - A limit needs 1 tick through.
  - The stop is hit by a wick. A gap past the stop exits at the open.
  - On the fill candle, only the move against you counts.
- Stop: NQ 50, ES 20, gold 12, crude 0.50.
- Cost per trade: NQ 1, ES 0.5, gold 0.2, crude 0.02. The indicator default is 0.75 on NQ.
- Charts tested: 1m, 2m, 3m, 5m, 10m, 15m, 30m and 1h.
- Periods:
  - NQ: P1 = NQ 1m from Dec 26 2022 to Nov 28 2025 (757 days). P2 = MNQ 2026.
  - ES, gold, crude: the first half vs the second half of each chart's own data, to Oct 28 2026.
  - Gold and crude have no 1m candles, so there are no 1m–3m tests for them.
- Extra runs:
  - windows A–E with daily rules (3 trades, stop after 2 losses)
  - exit on SuperTrend flip only
  - stop at the flip ST line
  - 2R and 3R targets
  - splits: long vs short, VWAP side, VWAP color, stacked, higher-TF SuperTrend bias
  - random-entry controls
- **HOLDS** = avg RR above 0 with a t-score of 2+ in both periods (30+ / 20+ trades).

## Short answer
- **Nothing HOLDS** on any market or chart: 0 of 286 setup × chart cells. Random entries: 0 of 52.
- **The 50% limit is still the best setup, but only on NQ, on 5m to 30m.** It made money in both periods, strongly in 2022–25 and weakly in 2026 (WATCH):

| NQ, 50% limit, all hours | 2022–25 avg pts / t-score | 2026 avg pts / t-score |
|---|---|---|
| 5m | +0.92 / 3.1 | +1.27 / 1.3 |
| 10m | +2.48 / 4.2 | +1.14 / 0.6 |
| 15m | +4.23 / 4.7 | +2.35 / 1.1 |
| 30m | +4.75 / 2.7 | +4.25 / 1.2 |

- **Best NQ version:** the 50% limit with the exit on the **SuperTrend flip only** (ignore EXIT labels):

| Chart | WR | 2022–25 avg pts / avg RR / t-score | 2026 avg pts / t-score |
|---|---|---|---|
| 10m | 32% | +5.28 / +0.11 / 5.7 | +4.24 / 1.3 |
| 15m | 32% | +8.70 / +0.17 / 5.7 | +3.78 / 1.2 |

- **ES / MES:** nothing works. Every 1m–5m setup loses.
- **Gold and crude:** nothing holds. They look like the random entries.
- **Luck check:** a "one period t 2+, other period green" result showed up in 2.4% of setup cells (base run) and 0% of control cells. The setup hits sit on neighbouring NQ charts, which is the believable pattern.

## Old screenshot report vs real data (NQ, P1 2022–25 → P2 2026)

| Old claim | Screenshots said | Real data, P1 → P2 | Result |
|---|---|---|---|
| #1: 50% limit, 2m, all hours | +2.0 (T 2.5) | −0.21 (t −1.8, 36,451 trades) → −0.81 (t −0.9) | did not hold |
| 2m, windows + daily rules | +3.8 (T 2.1) | +0.48 (t 1.6) → +2.78 (t 2.0) | about one fifth of the size; watch |
| 2m, window C | +7.4 | +1.57 (t 2.3, 1,753 trades) → +4.31 (t 1.2, 139) | smaller; watch |
| Window A red on 1m–5m | red | 2m +2.48 (t 2.5) → +5.48; 5m +4.32 (t 3.0) → +4.05 | wrong: A is as good as C |
| Window B London green on 2m | +6.3 | −0.77 (t −2.1) → −0.13 | wrong |
| 1h 50% limit "EDGE" | +7.0 (T 2.4) | +7.32 (t 2.3) → +0.91 (t 0.2) | flat in 2026 |
| 5m flip limit at old ST line, windows on | +6.3 | −1.36 (t −2.1) → +4.52 | did not hold |
| 50% + GMC, 10m, windows on | +12.8 | −2.86 (t −2.0) → +8.47 | did not hold |
| VWAP colored with the trade, 2m | +6.2 (T 2.3) | +0.51 (t 1.2) → +5.90 (t 3.1) | no better than no filter in P1 |
| Under 1m / 1m does not work | — | 1m −0.65 (t −11) → −0.50 | confirmed |
| Box break and retest do not pay | — | 2m box break −1.30 (t −12) → −2.82 | confirmed on every market |
| Ride beats a 2R target | — | 15m ride +4.23 vs 2R +3.03; 1h +7.32 vs +1.08 | confirmed on 10m and up |

## VWAP note (important)
- The old VWAP split read VWAP on the candle that **filled** the 50% order. That candle's close already shows whether the bounce happened, so it is a look-ahead.
- Read that way, "price, VWAP and ST stacked" looked like an edge here too: HOLDS on every NQ chart, t 2–7.
- Read on the **EXIT candle**, when the limit is actually placed, VWAP side, color and stacked stop helping (about 1 HOLD in 500–800 cells).
- Drop the VWAP rule from the old playbook.

## Windows (NQ, 50% limit, windows + daily rules)
- C (08:35–09:45) and A (09:45–11:00) are green on 2m to 15m in both periods:
  - window C, 15m: +12.4 (t 3.4) → +16.4 (t 1.6)
  - window A, 15m: +9.9 (t 3.7) → +14.8 (t 1.7)
- B (London) and D (afternoon) lose or are flat.
- The NY morning to about 11:00 is where it works, which fits the 11:30 stop rule.

## Other splits (NQ, 50% limit)
- **Long vs short:** longs are better on most charts. Both test periods were mostly bull markets.
- **15m SuperTrend bias on 1m–3m:** it helps (with the bias beats against it), but those charts are still around 0.
- **Stop at the flip ST line:** no better than the fixed 50 pt stop.

## Files
- Session folder /home/claude/pp: ppdata.py, engine.py, run.py, agg.py, agg2.py
- trades_*.parquet, all_trades.parquet, tables.pkl
- sheet_tpl.html, MMM_PRO_PLUS_Retest.html
