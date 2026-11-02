# Archive index

Every script, Pine file and doc from the MMM test work, copied as it was. Folder = one project.
Run `python restore.py` first so the old hard-coded paths (/home/claude/<folder>) and data files exist again.

## allm/
All-strategies full grid: EDGE PRO 18 strategies, PRO FVA 22, FVA Break, GMU, XB break, XB filter. One grid engine for every entry x stop x target x exit.

| File | What it does |
|---|---|
| allm/MMM_All_Strategies_Full_Grid_Results.md | Doc: MMM all strategies: the full grid on 4 markets (Oct 30 2026) |
| allm/MMM_EDGE_PRO_FVA.pine | Pine: MMM EDGE PRO FVA @MaxMaserati |
| allm/agg.py | Aggregate the grid accumulators into tables. |
| allm/agg_filter.py | (helper / summary script) |
| allm/agg_xbbrk.py | Aggregate the grid accumulators into tables. |
| allm/build_cdl_page.py | (helper / summary script) |
| allm/build_page.py | (helper / summary script) |
| allm/grade1.py | Grade ONE rule per signal, trade by trade (same logic as grid.kernel). Returns a DataFrame of trades. |
| allm/grid.py | Full grid for any signal table: every entry x every stop x every target x every exit, bull/bear and periods apart. |
| allm/mdata.py | Market data for the all-strategy full-grid test. |
| allm/mk_new.py | (helper / summary script) |
| allm/rank.py | (helper / summary script) |
| allm/run_all.py | (helper / summary script) |
| allm/run_new.py | (helper / summary script) |
| allm/run_xbbrk.py | (helper / summary script) |
| allm/sig_edge.py | Signals (setups) for the 18 MMM EDGE PRO strategies (X.M1-X.M5, C.M1-C.M8, XCS.M1-XCS.M5). |
| allm/sig_fva.py | Signal generator for the 22 MMM PRO FVA strategies (FVA.M1 - FVA.M22). |
| allm/sig_misc.py | Signals for FVA.A / FVA.B (FVA Break 4.x), the GMU (all charts), the new XB FVA (after the break) and the XB zones (XBS / XBB). |
| allm/sig_xbbrk.py | XB break signals by kind (Oct 30 2026), opposite-side XB engine (x 4.0 default), x zone engine for the kind: |
| allm/tables.md | Doc:  |
| allm/xb_filter.py | Does the higher-timeframe Xpander Block improve the EDGE PRO strategies when used as a FILTER? (Oct 30 2026) |

## bf/
MMM Body Flip tests 1-5 (C1 / C2 retest, trade rules, management, new logic), the IB strategy check and her levels.

| File | What it does |
|---|---|
| bf/IB_Strategy_Check_Results.md | Doc: "Boring levels" IB strategy check (Nov 2 2026, updated with all her levels) |
| bf/MMM_Body_Flip_New_Logic_Test_Results.md | Doc: MMM Body Flip: new indicator logic test (Nov 2 2026) |
| bf/MMM_Body_Flip_Test_Results.md | Doc: MMM Body Flip Trend: full test (Nov 2 2026) |
| bf/MMM_C1_C2_Retest_Results.md | Doc: MMM Body Flip: C1 / C2 retest test (Nov 2 2026) |
| bf/MMM_Trade_Management_Test_Results.md | Doc: MMM trade management test (Nov 2 2026) |
| bf/MMM_Trade_Rules_Test_Results.md | Doc: MMM trade rules test (Nov 2 2026) |
| bf/agg10.py | (helper / summary script) |
| bf/agg11.py | (helper / summary script) |
| bf/agg3.py | (helper / summary script) |
| bf/agg4.py | (helper / summary script) |
| bf/agg5.py | (helper / summary script) |
| bf/agg6.py | (helper / summary script) |
| bf/agg7.py | (helper / summary script) |
| bf/agg8.py | (helper / summary script) |
| bf/agg9.py | (helper / summary script) |
| bf/bfeng.py | MMM Body Flip Trend engine, mirrored from the Pine (Nov 2 2026), numba. |
| bf/bfeng2.py | MMM Body Flip Trend engine v2 (Nov 2 2026) - mirrors the CURRENT Pine logic (numba). |
| bf/bffound.py | A: foundation stats for every CDS / CDL (and failed setups ✕), with a random control. |
| bf/bfgrid.py | Full trade grid for the Body Flip CDS / CDL signals (numba). |
| bf/bfgrid2.py | Retest grid for Body Flip CDS / CDL (Nov 2 2026, test 2). |
| bf/bfgrid3.py | Test 3: trade-management rules on the Body Flip CDS / CDL retest (Nov 2 2026). |
| bf/bfgrid4.py | Test 4: Max's trade management (Nov 2 2026). Always: one trade at a time + exit at the close of the next opposite flip (new C2). |
| bf/bfgrid5.py | Grader for test 5 (new Body Flip logic): every event type x entry x stop x target x exit, independent trades. |
| bf/bfprop.py | E2 / F: daily rules and prop checks on the best Body Flip candidates (single trades exported from the grid engine). |
| bf/bfrun.py | Driver: Body Flip signals -> full grid (B/E) + random controls, every market x timeframe, two periods. |
| bf/bfrun2.py | Driver for test 2: C1 / C2 range retest entries, PO4 / ATR stops, 1:2-1:6 or next-flip exit; every market x chart, two periods, random controls. |
| bf/bfrun3.py | Driver for test 3 (trade rules: BE, one trade at a time, close-past-C1/C2 exit). Saves raw stat arrays per market x chart. |
| bf/bfrun4.py | Driver for test 4 (Max trade management: flip exit always, fee BE on a BC, structure trail). Saves raw stat arrays per market x chart. |
| bf/bfrun5.py | Test 5 driver: the new Body Flip logic. Every event type through the grid, every market x chart, two periods, random controls. |
| bf/bfvar.py | C/D: every rule / trend-line setting variant through the full grid (all hours + 09:45-12:00, no controls). |
| bf/fsplit.py | (helper / summary script) |
| bf/ibagg.py | (helper / summary script) |
| bf/ibagg2.py | (helper / summary script) |
| bf/ibtest.py | Test of the 'boring levels strategy' from the video (Nov 2 2026). |
| bf/ibtest_v1.py | Test of the 'boring levels strategy' from the video (Nov 2 2026). |
| bf/lvagg.py | (helper / summary script) |
| bf/lvagg2.py | (helper / summary script) |
| bf/lvtest.py | Her LEVELS, coded (Nov 2 2026). Adds to ibtest.py (IB + Tokyo setups). |
| bf/mkdata.py | (helper / summary script) |
| bf/mkdata2.py | (helper / summary script) |
| bf/mkdata3.py | (helper / summary script) |
| bf/mkdata4.py | (helper / summary script) |
| bf/mksum3.py | (helper / summary script) |
| bf/mksum4.py | (helper / summary script) |
| bf/mksum5.py | (helper / summary script) |
| bf/mksum6.py | (helper / summary script) |
| bf/mksum7.py | (helper / summary script) |
| bf/t1.py | (helper / summary script) |
| bf/t2.py | (helper / summary script) |
| bf/t3.py | (helper / summary script) |
| bf/varsum.py | (helper / summary script) |

## course/
MMM Mastery Course files.

| File | What it does |
|---|---|
| course/MMM_Certificate_Mailer.gs | MMM_Certificate_Mailer.gs |
| course/MMM_Course_Certificate_Email_Setup.md | Doc: MMM Mastery Course: certificate email setup (maxmaserati.com) |

## docs/
Docs.

| File | What it does |
|---|---|
| docs/MMM_EDGE_PRO_18_Strategies.md | Doc: MMM EDGE PRO · all 18 strategies (updated Oct 30 2026) |
| docs/MMM_Gamma_Bias_TradingView_Description.md | Doc: Gamma Walls @MaxMaserati |
| docs/MMM_Strategy_Entries_Oct30.md | Doc: MMM Strategy Book · exact entry of every strategy (Oct 30 2026) |

## dw/
Daily / weekly order tests: target-first vs 50%-first.

| File | What it does |
|---|---|
| dw/MMM_Candle_Bias_Daily_Weekly_Odds.md | Doc: MMM Candle Bias Pro · Daily and Weekly odds |
| dw/dw.py | (helper / summary script) |
| dw/order4.py | Fill TGT-first and 50%-first for 1h / Daily / Weekly on NQ, ES, GC, CL from finer bars of the same source. |

## edge/
MMM EDGE PRO Pine patches from the test findings.

| File | What it does |
|---|---|
| edge/MMM_EDGE_PRO.pine | Pine: MMM EDGE PRO @MaxMaserati |
| edge/MMM_EDGE_PRO_orig.pine | Pine: MMM EDGE PRO @MaxMaserati |
| edge/MMM_EDGE_PRO_pre_avoid.pine | Pine: MMM EDGE PRO @MaxMaserati |
| edge/patch_avoid.py | EDGE PRO: two 'avoid' rules from the XB filter test (Oct 30 2026), NQ / MNQ only (where they were tested). |
| edge/patch_new.py | MMM EDGE PRO: new NQ rules for C.M4, XCS.M1 (longs) and X.M3 (Oct 30 2026 full-grid findings). |

## fva/
FVA Break 3.x bar-by-bar replica, edge grids, honest re-runs and strategy checks.

| File | What it does |
|---|---|
| fva/MMM_FVA_Best_2_Edges.md | Doc: MMM Fair Value Area Break — the 2 best edges, rules and honest results (Oct 25 2026) |
| fva/MMM_FVA_Break_3.1.pine | Pine: MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.1 |
| fva/MMM_FVA_Break_ReTest_Results.md | Doc: Fair Value Area Break 3.0: re-test results (Oct 19, 2026 · corrected Oct 20) |
| fva/MMM_FVA_Strategy_Grid_Results.md | Doc: Fair Value Area Break: strategy grid results (Oct 20, 2026 · corrected) |
| fva/cmp_h.py | (helper / summary script) |
| fva/eval_i.py | (helper / summary script) |
| fva/final/cands.py | (helper / summary script) |
| fva/final/fva_final.py | FVA final: 1 MNQ, one trade at a time, $ results, exact engine rules (market at close, stop first on 1m, 1 pt cost). |
| fva/final/hours_rows.py | (helper / summary script) |
| fva/final/patch_fva.py | (helper / summary script) |
| fva/final/tables.py | (helper / summary script) |
| fva/final/write_doc.py | (helper / summary script) |
| fva/fva_grid.py | FVA Break 3.1 edge grid, run through the established MMM test engine (rt/eng/core.simulate). |
| fva/fva_grid_c.py | Honest CONFIRMATION entries on the flip zones: the touch candle must CLOSE and hold the box |
| fva/fva_grid_h.py | Honest re-run of the flip-zone entries: same engine, setups from replica3 (limit live from the prior close). |
| fva/fva_grid_i.py | IDEA GRID: honest close-decided FVA events through the MMM engine. |
| fva/grid_eval.py | (helper / summary script) |
| fva/grid_years.py | (helper / summary script) |
| fva/mirror2.py | (helper / summary script) |
| fva/mirror_check.py | Mirror of the Pine 4.0 trade manager (bar by bar, 1m intrabars) vs the test engine, old NQ 1h. |
| fva/pesx/tbl.py | (helper / summary script) |
| fva/pine/MMM_FVA_Break_3.1.pine | Pine: MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.1 |
| fva/pine/MMM_FVA_Break_3.2.pine | Pine: MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.2 |
| fva/pine/MMM_FVA_Break_4.0.pine | Pine: MMM Perfect Entry: Fair Value Area Break @MaxMaserati 4.0 |
| fva/pine/MMM_FVA_Break_4.1.pine | Pine: MMM Perfect Entry: Fair Value Area Break @MaxMaserati 4.1 |
| fva/pine/MMM_FVA_Break_4.2.pine | Pine: MMM Perfect Entry: Fair Value Area Break @MaxMaserati 4.2 |
| fva/pine/MMM_FVA_Break_4.3.pine | Pine: MMM Perfect Entry: Fair Value Area Break @MaxMaserati 4.3 |
| fva/pine/MMM_PRO_f.pine | Pine: MMM PRO f: FVA Order Flow @MaxMaserati |
| fva/pine/build41.py | (helper / summary script) |
| fva/pine/fva_3.0.pine | Pine: MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.0 |
| fva/pine/patch31.py | Fair Value Area Break 3.0 -> 3.1: honest trade grading. |
| fva/pine/patch32.py | Fair Value Area Break 3.1 -> 3.2: only the strategies that passed the grid (FVA.M1-M4). |
| fva/prof/eng.py | (helper / summary script) |
| fva/prof/eng2.py | (helper / summary script) |
| fva/prof/eng3.py | (helper / summary script) |
| fva/prof/look.py | (helper / summary script) |
| fva/prof/look2.py | (helper / summary script) |
| fva/rank_all.py | Re-check every passing idea-grid combo per trade (one trade per candle per side) and rank. |
| fva/replica.py | Bar-by-bar replica of 'MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.0' (default inputs). |
| fva/replica2.py | Bar-by-bar replica of 'MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.0' (default inputs). |
| fva/replica3.py | Bar-by-bar replica of 'MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.0' (default inputs). |
| fva/replica4.py | Bar-by-bar replica of 'MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.0' (default inputs). |
| fva/replica_h.py | Bar-by-bar replica of 'MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.0' (default inputs). |
| fva/report.py | (helper / summary script) |
| fva/report_h.py | Rebuild summary.csv + years.csv for the dashboard: IND from the original replica (matches the chart), |
| fva/run1.py | (helper / summary script) |
| fva/run_all.py | (helper / summary script) |
| fva/run_all_h.py | (helper / summary script) |
| fva/sim.py | Two ways to score the replica's setups. |
| fva/strat_eval.py | Per-trade results of the honest box-failure strategies (1h), old NQ 2023-25 and new MNQ 2026. |
| fva/strat_eval2.py | Per-trade check of grid picks (replica4 events), old NQ + new MNQ, one trade per candle per side. |

## gamma/
Gamma Walls free version builder.

| File | What it does |
|---|---|
| gamma/MMM_Gamma_Walls_Free.pine | Pine: Gamma Walls @MaxMaserati |
| gamma/gb_v4.pine | Pine: Gamma Walls and Institutional Bias @MaxMaserati |
| gamma/mk_free.py | Gamma Walls free version: no arrows, no direction, no bias. Walls, flip, magnets, histogram, level map, market type. |

## gamma-levels/
Gamma levels and news calendar extractors for the gamma-levels site.

| File | What it does |
|---|---|
| gamma-levels/README.md | Doc: gamma-levels |
| gamma-levels/gex_extract.py | MMM Gamma Levels Extractor  (@MaxMaserati) |
| gamma-levels/news_extract.py | MMM News Calendar Extractor  (@MaxMaserati) |

## lez/
Levels / opening-candle / MMM PRO f level tests (sim engines, analyses, pages).

| File | What it does |
|---|---|
| lez/MMM_PRO_f_Level_Test_Results.md | Doc: MMM PRO FVA · HTF level → LTF reversal box · full test results |
| lez/analyze.py | (helper / summary script) |
| lez/analyze2.py | (helper / summary script) |
| lez/analyze3.py | (helper / summary script) |
| lez/analyze4.py | (helper / summary script) |
| lez/analyze5.py | (helper / summary script) |
| lez/analyze6.py | (helper / summary script) |
| lez/analyze7.py | (helper / summary script) |
| lez/build_page.py | (helper / summary script) |
| lez/build_page2.py | (helper / summary script) |
| lez/build_sheet.py | (helper / summary script) |
| lez/cfgscan.py | (helper / summary script) |
| lez/data.py | (helper / summary script) |
| lez/eng4.py | (helper / summary script) |
| lez/export_site.py | (helper / summary script) |
| lez/final.py | (helper / summary script) |
| lez/final2.py | (helper / summary script) |
| lez/final3.py | (helper / summary script) |
| lez/final4.py | (helper / summary script) |
| lez/found.py | (helper / summary script) |
| lez/levels.py | (helper / summary script) |
| lez/merge_tr.py | (helper / summary script) |
| lez/merge_tr2.py | (helper / summary script) |
| lez/of.py | (helper / summary script) |
| lez/of_k.py | (helper / summary script) |
| lez/pick.py | (helper / summary script) |
| lez/post7.py | (helper / summary script) |
| lez/post8.py | (helper / summary script) |
| lez/refsim.py | (helper / summary script) |
| lez/run.py | (helper / summary script) |
| lez/run2.py | (helper / summary script) |
| lez/run3.py | (helper / summary script) |
| lez/run4.py | (helper / summary script) |
| lez/sim.py | (helper / summary script) |
| lez/sim2.py | (helper / summary script) |
| lez/sim3.py | (helper / summary script) |
| lez/sim4.py | (helper / summary script) |
| lez/summ.py | (helper / summary script) |
| lez/tables.py | (helper / summary script) |
| lez/trend.py | (helper / summary script) |

## pp/
MMM PRO PLUS points test (Pine mirror) and the MMM Body Flip Trend Pine indicator.

| File | What it does |
|---|---|
| pp/MMM_Body_Flip_Trend.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_prev.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_v_before_c2open.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_v_before_cdsline.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_v_before_chain.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_v_before_connect.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_v_before_dyn.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_v_before_flipjoin.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_v_before_keepfix.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_v_before_lines.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_v_before_oldlines.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_v_before_oppdone.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_v_before_rejoin.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_v_before_sidejoin.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_Body_Flip_Trend_v_before_width.pine | Pine: MMM Body Flip Trend @MaxMaserati |
| pp/MMM_PRO_PLUS.pine | Pine: MMM PRO PLUS @MaxMaserati |
| pp/MMM_PRO_PLUS_Retest_Results.md | Doc: MMM PRO PLUS retest on real data (Nov 2 2026) |
| pp/agg.py | Aggregate PRO PLUS trades into stat rows. Every row: P1, P2 and both together, with a verdict. |
| pp/agg2.py | (helper / summary script) |
| pp/engine.py | MMM PRO PLUS points test (Table 3 / Table 4) mirrored in Python from the Pine script (Nov 2 2026). |
| pp/mk_standalone.py | MMM PRO PLUS standalone: remove every test / statistics / points-test part, add white NBC candles and the HTF SuperTrend bias. |
| pp/ppdata.py | Candles for the MMM PRO PLUS points test (Nov 2 2026). |
| pp/proplus.pine | Pine: MMM PRO PLUS @MaxMaserati |
| pp/proplus_full.pine | Pine: MMM PRO PLUS @MaxMaserati |
| pp/run.py | Run the PRO PLUS points test on every market x timeframe x run. Output: trades.parquet, counts.parquet. |
| pp/t1.py | (helper / summary script) |

## rt/
The original MMM test engine (rt/eng/core.py simulate) and its experiments.

| File | What it does |
|---|---|
| rt/eng/agg.py | (helper / summary script) |
| rt/eng/agg2.py | (helper / summary script) |
| rt/eng/build_sheets.py | Collect every result table into sheets.json for the HTML research sheet. |
| rt/eng/core.py | MMM research engine (Oct 2026 test). |
| rt/eng/data.py | Datasets. OLD = NQ 1m Dec 2022 - Dec 2025 (back-adjusted T). FRESH = MNQ Jul - Oct 2026 (raw V/Y). |
| rt/eng/exp_a.py | A. Entry location: MMCB candle types, every entry x stop x target x exit. |
| rt/eng/exp_abs.py | B. Absorption inside boxes and at their edges (MNQ footprint Jul 8 - Oct 16 2026, 5m / 10m / 15m). |
| rt/eng/exp_b.py | Balance study (exit question) + BC flow per candle type. |
| rt/eng/exp_g.py | GMC (3 candles with a gap) on every timeframe: entries XU / c3 close / c3 low / gap 50% / c1 high / c2 ladder / POC, |
| rt/eng/exp_live.py | Live balance-zone control: at EVERY candle that closes inside a live MMM x box (what an indicator sees in real time), |
| rt/eng/exp_m.py | HTF signal, LTF entry ('magnifier'). |
| rt/eng/exp_p.py | Pullback map: for every MMCB candle, does the next candle(s) take its target (bull: the high)? |
| rt/eng/exp_z.py | Zone x box breaks (CONTRACTION G1 and EXPANDER G1): entries at close / break-candle ladder / broken level / box 50% / POC. |
| rt/eng/mag_an.py | (helper / summary script) |
| rt/eng/mag_an2.py | (helper / summary script) |
| rt/eng/rows.py | Generic row builder + runner: every entry x every stop for a set of signal bars. |
| rt/eng/screen.py | (helper / summary script) |
| rt/eng/themes.py | (helper / summary script) |
| rt/eng/verify.py | Independent slow check of the simulator on random rows (fresh 15m, 5m replay). |
| rt/eng/zone.py | Port of the MMM Zone engine (x, Concepts Pro+) f_zoneEngine, gate off. |
| rt/lib/tools/load.py | MMM Data Library loader. |
| rt/out/MMM_Pullback_Exit_Lab_Results.md | Doc: MMM Pullback & Exit Lab — Results (Oct 18 2026) |

## ten/
09:30-11:30 testing studies and the 10 AM study (candle odds, UPG gaps, BC runs).

| File | What it does |
|---|---|
| ten/MMM_0930_1130_Testing_Studies.md | Doc: 9:30 AM to 11:30 AM Testing Studies |
| ten/MMM_10AM_Study.md | Doc: 10:00 NY Study: MMCB candles, opening gaps, 10-14 pullback, BC runs, other-side gaps, runs to 11:30 |
| ten/REPORT.md | Doc: 10:00 NY Study: MMCB candles, opening gaps, 10-14 pullback, BC runs, other-side gaps, runs to 11:30 |
| ten/add_q567.py | (helper / summary script) |
| ten/build_report.py | Merge q1..q4 json into results.json and write REPORT.md (both periods side by side: 2022-25 / 2026) |
| ten/build_study.py | Build '9:30 AM to 11:30 AM Testing Studies': site page + standalone artifact + markdown, from one content list. |
| ten/common.py | (helper / summary script) |
| ten/edit_ind.py | (helper / summary script) |
| ten/edit_ind2.py | (helper / summary script) |
| ten/odds.py | MMCB odds per candle type: what the NEXT candle does (all sessions). |
| ten/q1.py | Q1: candles that close at 10:00 NY (4H 06-10, 1h 09-10, 15m 09:45, 5m 09:55) |
| ten/q2.py | Q2: UPG gaps made 09:30-10:00 on 5m and 1m |
| ten/q3.py | Q3: pullback inside the 10:00-14:00 4H candle |
| ten/q4.py | Q4: BC runs (same-side body closes until the first opposite BC) on 5m, 15m, 1h |
| ten/q56.py | Q5: open UPG gaps on the opposite side of the 10:00 candle target. Q6: runs from 10:00 to 11:30 until an 'opposite candle'. |
| ten/q5sum.py | (helper / summary script) |
| ten/q6sum.py | (helper / summary script) |
| ten/q7.py | Fixed 50 pt stop, 1:2 (100 pt target), entry at the close of the first 5m/15m BC at or after 10:00, out at 11:30. Cost 1 pt. |
| ten/q8.py | 09:30-11:30 window profile: when the high/low is made, range, the 09:30 candle (5m/15m), the 09:30-10:00 opening range break. |
| ten/render_study.py | (helper / summary script) |
| ten/verify.py | (helper / summary script) |

## v35/
MMM PRO 3.5 / Order Flow Suite Pine patch builders.

| File | What it does |
|---|---|
| v35/MMM_Concepts_Pro_Plus_3.5.pine | Pine: MMM Concepts Pro+ @MaxMaserati |
| v35/MMM_Order_Flow_Suite_3.5.pine | Pine: MMM Market Structure & Order Flow Suite @MaxMaserati 3.5 |
| v35/MMM_Pro_3.5.pine | Pine: MMM Pro @MaxMaserati |
| v35/concepts_orig.pine | Pine: MMM Concepts Pro+ @MaxMaserati |
| v35/news_module.py | (helper / summary script) |
| v35/ofs.pine | Pine: MMM Market Structure & Order Flow Suite @MaxMaserati 3.4 |
| v35/patch_concepts.py | (helper / summary script) |
| v35/patch_concepts2.py | (helper / summary script) |
| v35/patch_ofs.py | (helper / summary script) |
| v35/patch_pro.py | (helper / summary script) |
| v35/pro_orig.pine | Pine: MMM Pro @MaxMaserati |

## v36/
MMM PRO 3.6 / 3.7 module builders.

| File | What it does |
|---|---|
| v36/MMM_Concepts_Pro_Plus_3.6.pine | Pine: MMM Concepts Pro+ @MaxMaserati 3.6 |
| v36/MMM_Concepts_Pro_Plus_3.7.pine | Pine: MMM Concepts Pro+ @MaxMaserati 3.7 |
| v36/MMM_Order_Flow_Suite_3.6.pine | Pine: MMM Market Structure & Order Flow Suite @MaxMaserati 3.6 |
| v36/MMM_Order_Flow_Suite_3.7.pine | Pine: MMM Market Structure & Order Flow Suite @MaxMaserati 3.7 |
| v36/MMM_Pro_3.6.pine | Pine: MMM Pro @MaxMaserati |
| v36/MMM_Pro_3.7.pine | Pine: MMM Pro @MaxMaserati 3.7 |
| v36/MMM_Pro_36regen.pine | Pine: MMM Pro @MaxMaserati |
| v36/build.py | (helper / summary script) |
| v36/build37.py | (helper / summary script) |
| v36/concepts37_template.pine | Pine: MMM Concepts Pro+ @MaxMaserati 3.7 |
| v36/concepts_template.pine | Pine: MMM Concepts Pro+ @MaxMaserati 3.6 |
| v36/make_concepts37.py | (helper / summary script) |
| v36/make_ofs37.py | (helper / summary script) |
| v36/modules.py | (helper / summary script) |
| v36/modules_37a_backup.py | (helper / summary script) |
| v36/ofs37_parts.py | (helper / summary script) |
| v36/ofs37_template.pine | Pine: MMM Market Structure & Order Flow Suite @MaxMaserati 3.7 |
| v36/ofs_template.pine | Pine: MMM Market Structure & Order Flow Suite @MaxMaserati 3.6 |
| v36/patch_pro36.py | (helper / summary script) |
| v36/patch_pro36_regen.py | (helper / summary script) |
| v36/patch_pro37.py | (helper / summary script) |
| v36/pro_render.pine | Pine: pro_render.pine |

## v40/
MMM PRO U 4.0 builder.

| File | What it does |
|---|---|
| v40/MMM_PRO_U_4.0.pine | Pine: MMM PRO U @MaxMaserati 4.0 |
| v40/MMM_Pro_XCS_One.pine | Pine: MMM Pro XCS One @MaxMaserati |
| v40/body_a.pine | Pine: body_a.pine |
| v40/body_b.pine | Pine: body_b.pine |
| v40/body_c.pine | Pine: body_c.pine |
| v40/gmtab.pine | Pine: gmtab.pine |
| v40/make_u40.py | Builds MMM_PRO_U_4.0.pine from the template, the shared 3.7/3.8 modules and the new 4.0 parts. |
| v40/palette.pine | Pine: palette.pine |
| v40/stats38.pine | Pine: stats38.pine |
| v40/u40_template.pine | Pine: MMM Pro XCS One @MaxMaserati |

## xb/
Xpander Block (XB) and GMU ladder tests: zones, range trades, box direction, CDLx break.

| File | What it does |
|---|---|
| xb/MMM_PRO_x_4.0.pine | Pine: MMM PRO: Xpander Block Orderflow @MaxMaserati 4.0 |
| xb/MMM_XB_Box_Direction_Test.md | Doc: MMM XB: trade only WITH the box direction? (Oct 30 2026) |
| xb/MMM_XB_CDLx_Break_Test.md | Doc: MMM XB Break Test by kind: CDLx / CDSx and the rest (Oct 30 2026) |
| xb/MMM_XB_Filter_On_EDGE_PRO.md | Doc: MMM: the higher-timeframe XB as a FILTER on EDGE PRO (Oct 30 2026) |
| xb/MMM_XB_Range_Odds.md | Doc: MMM XB Range Trade Odds (Oct 30 2026) |
| xb/MMM_XB_Zone_Test_Results.md | Doc: MMM XB Zone Test: do XBS / XBB / Balanced / FVA work as predicted? (Oct 30 2026) |
| xb/MMM_Xpander_Block_GMU_Test_Results.md | Doc: MMM Xpander Block (XB) + GMU: test results (Oct 30 2026) |
| xb/agg2.py | (helper / summary script) |
| xb/agg_gmu.py | (helper / summary script) |
| xb/agg_gmu2.py | (helper / summary script) |
| xb/agg_grid.py | (helper / summary script) |
| xb/agg_range.py | (helper / summary script) |
| xb/agg_range2.py | (helper / summary script) |
| xb/agg_xb.py | (helper / summary script) |
| xb/agg_zone2.py | (helper / summary script) |
| xb/agg_zone3.py | (helper / summary script) |
| xb/core.py | Core for the GMU ladder + new Xpander Block (XB) tests. |
| xb/gmu.py | GMU ladder test: 3 approaches x 7 levels x C3 shape, per TF and period. |
| xb/grid.py | GMU full grid: every ladder entry x every stop x every target x every exit, accumulated in numba. |
| xb/grid2.py | GMU entry map: bull and bear SEPARATE. Ladder names from each range's LOW (Max's convention, no mirroring). |
| xb/maxread.py | Max's read of the XB zones: SELL in discount (XBS, price drops into it) · BUY in premium (XBB, price rises into it). |
| xb/mkfresh.py | (helper / summary script) |
| xb/pine/MMM_PRO_x_4.0.pine | Pine: MMM PRO: Xpander Block Orderflow @MaxMaserati 4.0 |
| xb/pine/MMM_PRO_x_4.0_pre_opp.pine | Pine: MMM PRO: Xpander Block Orderflow @MaxMaserati 4.0 |
| xb/pine/patch_xb.py | (helper / summary script) |
| xb/pine/xb_orig.pine | Pine: MMM PRO: Xpander Block Orderflow @MaxMaserati |
| xb/rank2.py | (helper / summary script) |
| xb/xbeng.py | New Xpander Block engine (Max, Oct 30 2026), closed candles, grow-with-wicks. |
| xb/xbrange.py | XB range trades (Max, Oct 30 2026): enter at a zone of a LIVE Xpander Block, target the other side. |
| xb/xbrange3.py | XB range trades (Max, Oct 30 2026): enter at a zone of a LIVE Xpander Block, target the other side. |
| xb/xbtest.py | Tests of the new Xpander Block: inside zones (before the break) and FVA entries (after the break). |
| xb/xbzone2.py | Do the XB zones work as Max predicts? (Oct 30 2026) |
| xb/xbzone3.py | Do the XB zones work as Max predicts? (Oct 30 2026) |

## (top level)

| File | What it does |
|---|---|
| MMM_Order_Flow_Suite_3.4.pine | Pine file |
| build_sheet.py | script |

## cf/
Chart Fanatics strategies (Fabio Valentini, JJ Simon, Candace Lau, Dhesi, Okala, Marci Silfrain) coded and tested against their claims (Nov 2 2026).

| File | What it does |
|---|---|
| cf/cfstrat.py | Signal rules for all six strategies |
| cf/cfrun.py | Runs every entry x stop x target x exit with random twins |
| cf/cfagg.py | Claims-vs-test summaries |
| cf/Chart_Fanatics_Strategy_Check.md | Doc: results and verdict |
