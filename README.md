# MMM Test Lab

Test any simple trading idea in your browser, with Max's testing rules built in.

**Open it:** https://maxmaseratii.github.io/MMM-TEST-LAB/

## How to use it
1. **Pick a market and chart:** NQ / MNQ, ES / MES, gold or crude, on 1m to 4h.
2. **Pick an idea:**
   - **Body Flip event:** a flip (CDS / CDL), a trend line or ATR line touch / break, a PO4 touch / break, or an old line touch.
   - **BC candle:** BuBC / BeBC. Optional: a bigger body than ATR, NBCs right before it, or only the Nth BC in a row.
   - **Level touch and reject:**
     - Levels: previous day high / low, London, overnight, Asia range, previous session and previous week volume profile, 30m / 60m supply / demand zones.
     - Reaction: aggressive, or a simple close back.
   - **Initial balance:** failed auction and trend continuation, with her targets.
   - **Opening range:** break, failed break, or break and retest.
   - **Candle at a set time:** for example the 9:55 candle on 5m.
   - **Custom formula:** one line of code. Example: `bc[i] === 1 && bc[i-1] === 0 ? 1 : 0`.
3. **Add filters:** side, time window, weekdays, higher-chart trend, Body Flip trend, first signal per day.
4. **Tick the grid:** entries, stops, targets and exits. Every box is paired with every other box.
5. **Press Run test.**

## What you get
- **Verdict:**
  - How many combos PASS (t-score 2+ in both periods, 30+ trades each).
  - How many random entries passed. That's the luck level.
- **Foundation:** BCs before the opposite BC, BCs in a row before the first NBC, points after 1 / 5 / 10 candles, % up after 5.
- **The full grid:** WR (win rate), avg RR, PF (profit factor), t-score and random avg RR for both periods. The fixed 1:2 test (NQ 50 / ES 20 / gold 12) is always pinned on top.
- **Click any row for:**
  - one account ($ risk, one trade at a time, stop after N losses a day);
  - $ per month, best and worst month, green months;
  - 50k prop evaluation passes;
  - the equity curve, and every trade as a CSV download.
- **Save tests:** "Save as preset" keeps a test in your browser. "Copy share link" makes a link that opens that exact test.

## The rules built in
- **Two periods:**
  - NQ Dec 2022 – Nov 2025 (P1) against MNQ 2026 (P2), run apart.
  - ES, gold and crude: the first half against the second half of their own data.
- **Random twin for every trade:** same side, same stop size, same target in R, random time on the same day (inside your time window if you set one).
- **Same-candle stop and target:** the stop wins.
- **Costs per trade:** NQ 1 pt, ES 0.5, gold 0.2, crude 0.02.
- **Limit orders** must fill within 10 candles.
- **Max hold:** the end of the day (17:00), or 2,000 candles.
- **Hold to next session open:** 18:00 → 02:00, 02:00 → 08:00, 08:30 → 09:30, 09:30 → 16:00.

## Checked against the Python library
The page runs `engine.js`, a JavaScript copy of `python/mmmlab`. On NQ / MNQ it gives the same results:
- **Body Flip events** on MNQ 5m: all 12,691 events match (bar, kind, side, level, PO4).
- **Levels:** every day's previous session POC / VAH / VAL and previous week volume profile.
- **Zones:** all 1,188 30m zones, and all 170 IB signals.
- **Grades:** the full BC grade on NQ 5m (95,283 + 14,686 trades). WR, avg RR and t-score match to 4 decimals.
- **One small difference:** the page tests every live zone. The old Python levels test (`archive/bf/lvtest.py`) only checked zones within 6 stops of the open, to save time.

## Folders
| Path | What it is |
|---|---|
| `index.html`, `engine.js` | The web page and its test engine. |
| `data/*.bin.gz` | Candles for the page (built from the Python data pack). |
| `python/mmmlab/` | The Python toolkit for bigger tests (see `python/README.md`). |
| `python/examples/template_test.py` | Copy this to test an idea in Python. |
| `python/archive/` | Every old MMM test script, Pine file and result doc. `python/archive/INDEX.md` lists them. |
| `python/data/` | The data pack (`fine/*.parquet`) and the original CSVs (`raw_csv.tar.xz`). |
| `python/restore.py` | Brings back every old test exactly as it was. |
| `python/tools/build_web_data.py` | Rebuilds the page's data after you add new candles. |

## Adding new data
```bash
cd python
python -c "from mmmlab import data; data.add_csv('MNQ', 'my_new_bars.csv')"   # time,open,high,low,close,volume (NY time)
python tools/build_web_data.py                                               # refresh the web page's candles
```
Commit and push. The page updates by itself.

## Run it on your computer
```bash
python -m http.server 8000      # in this folder, then open http://localhost:8000
```
