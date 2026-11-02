# MMM Test Lab

Every tool from the MMM backtests, saved in one place. With it you can test a new idea in about 20 lines, or rerun any old test exactly as it was.

## What's inside
| Folder | What it is |
|---|---|
| `mmmlab/` | The clean toolkit you use for new tests (see below). |
| `examples/template_test.py` | Copy this to test a new idea. Change only the SIGNALS part. |
| `archive/` | Every old script, Pine file and result doc, by project (329 files). `archive/INDEX.md` says what each one does. |
| `data/fine/` | All the candles: NQ 1m Dec 2022 – Nov 2025, MNQ / MES / MGC / MCL 2026 (1m, else 5m, else 15m). |
| `data/raw_csv.tar.xz` | The original CSV files (including MNQ footprint), used by `restore.py`. |
| `restore.py` | Puts every old test back exactly as it was, so the old scripts run again. |

## The toolkit (`mmmlab/`)
- **data**: candles for any market and chart.
  - `bars('MNQ', 5)` gives 5m candles.
  - `series('NQ', 5)` gives both periods (P1 = NQ 2022–25, P2 = MNQ 2026).
  - `SPEC` holds the fixed stop, cost, tick and $ per point. `add_csv()` adds new data.
- **candles**:
  - BuBC / BeBC / NBC and ATR.
  - **foundation stats**: BCs before the opposite BC, BCs before the first NBC, and points after 1 / 5 / 10 candles.
- **grade**:
  - Pairs every entry × stop × target × exit. No hand-picking.
  - Every trade gets a **random twin**: same side, same stop size, same target, random time.
  - Gives a stats table (WR = win rate, avg RR, PF = profit factor, t-score) and the **PASS rule** (t-score 2+ in both periods).
  - The fixed 1:2 stop (NQ 50 / ES 20) is always in.
- **money**:
  - One trade at a time, and stop the day after 2 losses. A loss counts only once that trade has closed, so there's no peeking ahead.
  - Gives $ per month and the 50k prop evaluation pass rate.
- **levels**: volume profile (POC / VAH / VAL), previous day and previous week levels, London high / low, supply / demand zones, VWAPs, and a touch-and-reject finder.
- **sessions**: initial balance setups (failed auction, trend continuation) and Tokyo range setups.
- **flip**: the MMM Body Flip Trend engine (C1 / C2 flip, PO4, trend line, ATR line, every event). It copies the Pine.
- **compat**: old-style `mdata` / `ppdata` reading the new data pack. Call `mmmlab.use_compat()` and the archived engines import cleanly.

## Quick start
```bash
pip install numpy pandas numba pyarrow
python examples/template_test.py        # Body Flip test: foundation, full grid, PASS count, $ per month
python restore.py                       # bring back every old test into /home/claude (or --root /my/folder)
```

## The testing rules built in
- **Two periods:**
  - NQ 2022–25 against MNQ 2026, run apart.
  - ES and gold: the first half against the second half of their own data.
- **PASS** = t-score 2+ in **both** periods, with 30+ trades in each.
- **Always compare to random entries.** If random passes as often, it's luck.
- **Costs per trade:** NQ 1 pt, ES 0.5, gold 0.2, crude 0.02.
- **Same-candle stop and target:** the stop wins.
- **Fixed 1:2 test stop:** NQ / MNQ 50 pts, ES / MES 20, gold 12.
- **Hold exits** mean hold to the next session open (18:00 → 02:00, 02:00 → 08:00, 08:30 → 09:30). Use `exits=[('time', minute_of_day)]`.

## Old tests and where they live
| Test | Script(s) | Result doc |
|---|---|---|
| Body Flip tests 1–5 (flip, C1 / C2 retest, trade rules, management, new logic) | `archive/bf/bfeng*.py`, `bfgrid*.py`, `bfrun*.py` | `archive/bf/MMM_*_Results.md` |
| IB "boring levels" strategy + her levels | `archive/bf/ibtest.py`, `lvtest.py` | `archive/bf/IB_Strategy_Check_Results.md` |
| All strategies full grid (EDGE PRO 18, PRO FVA 22, FVA Break, GMU, XB) | `archive/allm/grid.py`, `sig_*.py` | `archive/allm/MMM_All_Strategies_Full_Grid_Results.md` |
| XB filter on EDGE PRO | `archive/allm/xb_filter.py` | `archive/xb/MMM_XB_Filter_On_EDGE_PRO.md` |
| Xpander Block / GMU (zones, range odds, box direction, CDLx break) | `archive/xb/*.py` | `archive/xb/MMM_XB_*.md` |
| FVA Break 3.x replica and grids | `archive/fva/replica4.py`, `fva_grid*.py` | `archive/fva/MMM_FVA_*.md` |
| MMM PRO PLUS points test | `archive/pp/engine.py`, `run.py` | `archive/pp/MMM_PRO_PLUS_Retest_Results.md` |
| MMM PRO f levels / opening candles | `archive/lez/*.py` | `archive/lez/MMM_PRO_f_Level_Test_Results.md` |
| 09:30–11:30 studies, 10 AM study | `archive/ten/q*.py` | `archive/ten/MMM_0930_1130_Testing_Studies.md`, `MMM_10AM_Study.md` |
| Daily / weekly candle order | `archive/dw/*.py` | `archive/dw/MMM_Candle_Bias_Daily_Weekly_Odds.md` |
| Original engine (opening range, speed rule, etc.) | `archive/rt/eng/*.py` | the project docs |

## Data notes
- **MNQ 1m** covers about 2 months of 2026. 5m runs to Oct 28 2026.
- **Before March 2026,** MNQ and MES have 15m only. Gold has 15m only before July 2026.
- **MGC** has no 1m data.
- **Timestamps** are New York time. A trading day starts at 18:00.
