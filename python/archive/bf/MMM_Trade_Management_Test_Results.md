# MMM trade management test (Nov 2 2026)

Results sheet: artifact **"MMM Trade Management Test"**. Research only, not advice.

## The rules
**Always on:**
- **One trade at a time.** While a trade is open, new signals are skipped.
- **Out at the next flip.** When a C2 confirms the opposite flip, the trade closes at that C2 close. The new flip can be traded at the same close.

**Tested (9 ways to manage the trade):**
- **No break-even**, as the baseline.
- **Break-even at entry + 1 fee or entry + 2 fees.**
  - It is set when a body close in your direction (BuBC for a long, BeBC for a short) closes past that level.
  - It is used from the next candle.
- **Then trail the stop on structure.** The stop only moves in your favor.
  - No trail.
  - The Body Flip trend line.
  - The wick of each new BC in your direction.
  - The open of each new BC.
- **Fee** = round-turn cost: NQ 1, ES 0.5, gold 0.2, crude 0.02 points.
- **Also tested with each:** the close-past-C1 / C2 exit (none, C2 open, C2 wick, C1 open, C1 wick).

**On top of that:**
- 15 entries, 10 stops, and targets from 1:2 to 1:6 or none (ride to the flip).
- 8 charts from 1m to 4h, on 4 markets, in two periods.
- Random entries run under the same rules.
- With no break-even, every trade matches the earlier grader exactly.

## Short answer
- **No edge with this management either.**
  - 12 of 3.6 million CDS / CDL combos pass (t-score 2+ in both periods).
  - Random entries pass 0 of 2.9 million.
- **All 12 passes are the same gold 15m, 09:45–12:00 pocket**, at 12.5% of the last C1 range, with about 44 trades per period.
- **No NQ, ES or crude combo passes.** The NQ 10m long ATR ×2 ride no longer passes once the flip exit is always on.
- **On NQ the 9 ways to manage the trade are within about 0.01 avg RR of each other.** The entry decides the result, and the entry is like random.

## Trades closed at the next flip do count
NQ, market at C2, PO4 stop, no target, no break-even:

| Chart | Out at the flip | Their avg R | Full stop | Its avg R | Overall avg RR P1 / P2 |
|---|---|---|---|---|---|
| 1m | 63% | +0.47 | 37% | −1.14 | −0.13 / −0.12 |
| 5m | 59% | +0.67 | 41% | −1.10 | −0.05 / −0.09 |
| 15m | 57% | +0.77 | 43% | −1.05 | −0.00 / +0.00 |
| 1h | 51% | +0.95 | 49% | −1.03 | −0.01 / +0.08 |

- **The flip exits are the winners.** They are not "like we never took them".
- **The full stops cancel them out,** so the total stays around 0 or below.

## Break-even at entry + 1 or 2 fees
- **Full losses drop** from 37–49% of trades to about 27–29%.
- **But about half of all trades now end at break-even,** and only 22–25% reach the flip.
  - Most of those break-even trades would have been flip-exit winners.
- **Net avg RR is about the same.**
  - NQ 5m: −0.05 / −0.09 with no break-even, −0.07 / −0.07 with it.
  - NQ 15m: −0.00 / +0.00 with no break-even, −0.02 / −0.02 with it.
- **+1 fee and +2 fees give the same result.**
  - +2 fees just turns the scratches into tiny wins.
  - So WR jumps from about 14% to about 63%, but avg RR does not change.

## Trailing on structure after break-even
- **It makes the result slightly worse.**
  - NQ 15m, no target: break-even with no trail −0.02 / −0.02.
  - With the trend-line trail: −0.03 / −0.05.
  - With the BC-wick or BC-open trail: −0.05 / −0.05.
- **Why:** it turns more trades into small wins (+0.4R on average), but it cuts the big flip-exit winners.
  - Only 10–14% of trades still reach the flip.
  - Those that do are often below 0, because they already gave back to the trail level.

## What it means
- **This is a sound way to manage risk.**
  - It caps full losses at about 27% of trades.
  - It makes sure you are never in two trades.
- **It cannot make an edge from an entry that has none.**
- **The best management for these signals is the simplest: no break-even, out at the flip.** It keeps the big winners. It is still about 0 overall.

## Indicator fix
- **The error:** "Error on bar 21354: historical offset (2093) beyond the buffer (2092)".
  - A BIG C1 line was being drawn from a candle more than 2,092 bars back.
- **The fix:**
  - The indicator now has max_bars_back = 5000.
  - Every line start is clamped to at most 4,900 candles back.

## Files
- **Scripts:**
  - bfgrid4.py: the grader, with fee break-even, structure trail and exit-type counts.
  - bfrun4.py: the driver.
  - agg9.py, mksum4.py and mkdata4.py: the summaries.
- **Results:** g4/*.npz and grid4_all.parquet.
