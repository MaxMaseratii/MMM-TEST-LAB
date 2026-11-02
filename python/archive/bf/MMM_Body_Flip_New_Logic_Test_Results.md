# MMM Body Flip: new indicator logic test (Nov 2 2026)

Results sheet: artifact **"MMM Body Flip New Logic Test"**. Research only, not advice.

## What was tested
**The engine copies the indicator as it works now:**
- **Flip:** a C1, then a C2 with a body of 50%+ of C1. Some candle from C1 on must also close beyond the last opposite BC open. Once that happens, it stays done.
- **PO4:** the highest high or lowest low from C1 to the flip.
  - A touch moves it to the wick.
  - A close beyond deletes it.
- **Trend line and ATR line:** they start at the same extreme and step on bigger BCs.
  - A touch moves them to the wick.
  - A close beyond deletes them.
  - The next step starts a new line.
- **Old lines:** the old trend's lines stay alive after a flip.

**Every event the indicator draws was traded:**

| Event | Direction traded |
|---|---|
| FLIP (CDS / CDL) | the new trend |
| Trend line / ATR line touch-and-hold (wick beyond, close back inside) | with the trend |
| PO4 touch-and-hold | away from the PO4 (short at a BePO4) |
| Old trend line / old ATR line touch-and-hold | the old line's side |
| Trend line / ATR line break (close beyond) | against the trend |
| PO4 break | the break direction |

**The trades:**
- **Entries:**
  - Market at the signal close.
  - Limit at the event level.
  - Limit at 50% of the signal candle.
- **Stops:**
  - Structure (the signal candle's wick, or the PO4 for a flip).
  - Fixed NQ 20 / 40 / 50 / 60. ES 8 / 16 / 20 / 24. Gold and crude are scaled the same way.
  - The PO4 of the trade side.
  - The ATR line.
  - The trend line.
- **Targets:** 1:1, 1:2, 1:3, 1:4, 1:6 or none.
- **Exits:**
  - Stop or target only.
  - Out at the next flip.
  - Out at a close past the trend line.
  - Your management: stop to entry + 1 fee after a BC closes in profit, then out at the next flip.

**Scope:**
- Markets: NQ / MNQ, ES / MES, gold and crude.
- Charts: 1m to 4h.
- Two periods per market, with random entries run beside everything.
- MNQ data runs to Oct 16 2026.
- The grader matches a plain loop exactly.

## Short answer
- **The new logic still has no edge on NQ.**
  - 230 of 456,000 event combos pass (t-score 2+ in both periods). Random entries pass 51 of 114,000.
  - Pass rates: 0.05% for events vs 0.045% for random — luck level overall.
  - The flip itself passes 1 of about 62,000.
- **After any event, price moves about 0 in the event direction.**
  - Example: after a flip on NQ, −0.05 pts after 1 candle and −0.16 after 5 (2022–25, all charts).
  - Up-after-5 is about 48–50% for every event.
- **Breaks and flips are followed by slightly more BCs on the same side.**
  - About 1.42 before the first opposite BC, against 1.20 for random candles.
  - The points still go nowhere.
- **The simple trade loses on nearly every NQ chart for every event:** market entry, 50-pt stop, 1:2, out at the next flip.
- **NQ long passes are matched by random long entries.** That includes trend line and ATR touches on 2m–3m and PO4 breaks on 5m–10m. NQ simply went up.

## The one real-looking pocket: old trend line touch on ES
- **The setup:**
  - ES 3m, LONG.
  - Price touches an old bull trend line that is still alive from an older trend, then closes back above it.
  - Market at the close, fixed 20 pts, 1:1, out at the next flip.
- **Results:**
  - 158 / 188 trades.
  - WR 59% / 56%.
  - avg RR +0.15 / +0.13.
  - PF 1.86 / 1.90.
  - t-score 3.1 / 3.3.
- **Random entries with the same stop and exit:** −0.05 / −0.04.
- **It holds across settings:** 107 of ES's passes are this same setup on 2m and 3m, with other stops and targets.
  - Fixed 16 pts, 1:4, out at a close past the trend line: avg RR +0.24 / +0.28, t-score 2.9 / 3.7.
- **Weak spots:**
  - It only works on ES. On NQ the same setup is about 0 on every chart.
  - 3m is the best chart. 2m and 5m are weaker, and 1m is 0.
  - ES has only about 10 months of data, so each period is about 5 months.
- **Verdict:**
  - It is the old bull chain floor holding. That matches what you saw on the chart this morning.
  - Watch it on ES. Retest when more ES data is in.

## Other small pockets (watch only)
- **NQ 2m, 09:45–12:00, long on a touch-and-hold of an old bull ATR line:**
  - Limit at the line, fixed 60 pts, 1:1.
  - avg RR +0.10 / +0.39, t-score 3.4 / 2.9.
  - Only 48 trades in 2026. Random: −0.02 / +0.05.
- **ES 5m, 09:45–12:00, PO4 touch-and-hold (both sides):**
  - Fixed 16 pts, 1:1.
  - avg RR +0.32 / +0.27.
  - Only 47 / 69 trades.

## What it means
- **The new rules make the chart cleaner,** but they don't add an edge to the flip or to the line touches and breaks on NQ.
- **The only signal worth following is the old bull trend line (the chain floor) holding on ES.** It is long only, on 2–3m.

## Files
- **Scripts:**
  - bfeng2.py: engine.
  - bfgrid5.py: grader.
  - bfrun5.py: driver.
  - agg10.py, agg11.py, mksum5.py: summaries.
- **Results:**
  - grid5_NQ / ES / GC / CL.parquet.
  - found5_*.parquet.
