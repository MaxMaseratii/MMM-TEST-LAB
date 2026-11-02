# MMM trade rules test (Nov 2 2026)

Results sheet: artifact **"MMM Trade Rules Test"**. Research only, not advice.

## The rules tested
1. **One trade at a time.**
   - While a trade is open, every new signal is skipped.
   - A new trade can start on the candle the last one ended.
2. **Break-even once in profit.**
   - Once the trade is +0.25R, +0.5R or +1R in profit, the stop moves to entry + cost. A stop-out there = 0 R after costs.
   - Also tested with no break-even.
3. **Exit on a close back past C1 or C2.**
   - Long: a close below the level. Short: a close above it.
   - Levels: C2 open, C2 wick, C1 open, C1 wick. Also tested with no close exit.

## What they were tested on
- **Entries (15):**
  - Market at the C2 close.
  - A limit in the last C1 range or the C2 range at 0, 12.5, 25, 50, 75, 87.5 and 100% depth.
- **Stops (10):**
  - PO4 last C1 wick, and PO4 strongest C1 wick.
  - Trailing ATR line ×0.5 / 1 / 1.5 / 2.
  - Fixed NQ 20 / 40 / 50 / 60 pts. Other markets are scaled the same way: ES 8 / 16 / 20 / 24, gold 4.8 / 9.6 / 12 / 14.4, crude 0.20 / 0.40 / 0.50 / 0.60.
- **Targets:** 1:2 to 1:6, or none. With or without an exit at the next opposite flip.
- **Charts:** 1m, 2m, 3m, 5m, 10m, 15m, 1h and 4h.
- **Markets:** NQ / MNQ, ES / MES, gold and crude.
- **Traders:** 6 separate one-at-a-time traders.
  - Both sides, long only and short only.
  - Each for all hours and for 09:45–12:00.
- **Periods and controls:** two periods per market, with random entries run under the same rules.
- **Check:** with no break-even and no close exit, every trade matches the earlier grader exactly. Only the trade order changes.

## Short answer
- **The rules do not create an edge.**
  - 13 of 3.2 million CDS / CDL combos pass (t-score 2+ in both periods). Random entries: 0 of 2.6 million.
  - All 13 passes are the same gold 15m, 09:45–12:00 pocket at 12.5% of the last C1 range, with about 44 trades per period.
  - No NQ, ES or crude combo passes with any rule.
- **On NQ, each rule moves avg RR by only about 0.01–0.02.** A losing trade stays a losing trade.

## Rule by rule (NQ, market at C2, PO4 last C1 stop, 1:2, both sides, all hours)

avg RR for P1 / P2. WR and trade count are for P1.

| Chart | Before (no rules) | One at a time | + BE +0.25R | + close past C2 open | All 3 |
|---|---|---|---|---|---|
| 1m | −0.13 / −0.13 (34%, 56,212) | −0.13 / −0.14 (34%, 30,521) | −0.13 / −0.13 (9%, 50,064) | −0.13 / −0.12 (27%, 38,221) | −0.13 / −0.13 (9%, 52,861) |
| 5m | −0.08 / −0.06 | −0.07 / −0.07 | −0.08 / −0.05 | −0.06 / −0.06 | −0.08 / −0.05 |
| 15m | −0.04 / −0.02 | −0.06 / −0.07 | −0.04 / −0.05 | −0.04 / −0.06 | −0.04 / −0.04 |
| 1h | −0.01 / +0.01 | +0.07 / +0.09 | +0.01 / +0.07 | +0.02 / +0.14 | −0.01 / +0.06 |

- **One trade at a time:**
  - About half the trades on 1m to 15m, because flips come faster than trades finish.
  - avg RR stays the same, so the skipped trades were not the bad ones.
- **Break-even:**
  - WR drops hard (34% → 9% at +0.25R) because many trades come back to entry and end at 0.
  - avg RR barely moves. The losses it saves are paid for by the winners it cuts early.
  - +0.25R, +0.5R and +1R all give about the same result.
- **Close exit:**
  - The C2 open exits earliest. The C1 wick is the same as the PO4 stop.
  - None of the 4 levels moves NQ avg RR by more than about 0.02 on average.
- **Fixed 40 / 50 stops with the rules:** they stay between about −0.10 and +0.03 on NQ 1m to 1h. 4h is worse.

## NQ 1h: green, but random is too
- **Market at C2 with the PO4 stop** is above 0 in both periods with most rule mixes.
  - Example, one trade at a time only: WR 38% / 38%, avg RR +0.07 / +0.09, PF 1.12 / 1.13, t-score 1.2 / 0.8.
  - About 570 trades in 3 years.
- **Best NQ 1h mix:**
  - The mix: PO4 last C1 stop, 1:5, BE at +0.5R, close past C1 open.
  - avg RR +0.11 / +0.20, t-score 1.8 / 1.8. Still under 2.
  - Random entries with the same rules: −0.10 / −0.06.
- **Share of NQ 1h combos positive in both periods:** 9.6% for CDS / CDL vs 8.8% for random. That is the same.
- **Verdict:** a watch item at best, not an edge.

## The passes (gold 15m, 09:45–12:00, both sides, limit at 12.5% of the last C1 range)
- **Best:** PO4 strongest C1 stop, 1:2 + next-flip exit, no BE, close past C1 open.
  - 44 / 41 trades.
  - WR 52% / 46%, avg RR +0.44 / +0.43, PF 2.67 / 2.44, t-score 2.5 / 2.3.
- **Break-even only fits at +1R.** At +0.25R or +0.5R it drops out of the pass list.
- **The close exit barely changes it.**
- **Over all hours, the same trade loses.**

## What it means
- **The three rules are good risk habits.**
  - One trade at a time limits exposure.
  - Break-even stops a winner turning into a loss.
- **They cannot turn a no-edge entry into an edge.**
  - Break-even trades win rate for scratches.
  - The close exit just ends trades a bit sooner.
- **The Body Flip CDS / CDL entry still tests the same as random,** with or without the rules.

## Files
- **Scripts:**
  - bfgrid3.py: the grader with BE, one-at-a-time and close-exit tracks.
  - bfrun3.py: the driver.
  - agg6.py, agg7.py, agg8.py and mksum3.py: the summaries.
- **Results:** g3/*.npz (raw) and grid3_all.parquet.
