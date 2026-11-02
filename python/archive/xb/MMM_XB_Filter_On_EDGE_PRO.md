# MMM: the higher-timeframe XB as a FILTER on EDGE PRO (Oct 30 2026)

## Verdict: no filter helps across the board
- Every EDGE PRO trade (16 strategies, C.M6 / C.M7 left out; book rule and the 50 pt 1:2 rule) was tagged with the 1h, 4h and daily XB known at the signal close (closed HTF candles only).
- **1,143 filter tests** with enough trades (30+ / 20+): 4 made a strategy clearly better in both periods, 7 made one clearly worse. About what luck gives.
- **No filter helps most strategies.** Best ones help about half the strategies:
  - 1h XB points with the trade: +0.06 / +0.07 avg RR on the kept trades (43% of strategies better in both).
  - Entry already outside the 1h XB on the break side: +0.07 / +0.12 (50%, only 12% of trades).
  - Daily last XB break with the trade: +0.02 / +0.11 (56%).
- Entering inside the 1h Balanced Zone, or in the "right" zone (buy XBS / sell XBB), does not help.
- **Watch (not proven):** X.M3 when the last daily XB break was a CDLx with the trade. 50 pt 1:2: +0.10 → +0.29 (P1), +0.16 → +0.69 (P2), t 3.0 / 3.0, 174 / 42 trades. Book rule: +0.12 → +0.26 / +0.17 → +0.56.
- **Avoid (consistent):**
  - C.M1 entries inside a live 1h / 4h / daily FVA of their own side: −0.07 to −0.32 avg RR (50 pt 1:2), on all three timeframes.
  - X.M4 when the entry is already outside the daily XB on the break side: −0.22 / −0.50. X.M4 when the last daily XB break was internal against: −0.07 / −0.67.
  - X.M1 when the last daily XB break was internal against: −0.13 / −0.15.
- **Decision:** keep the XB as a map in MMM PRO x. Do not add an XB filter to EDGE PRO. Re-check the X.M3 daily-CDLx lead when more 2026 5m data is in.

## Method
- Tags per trade (per HTF 1h, 4h, D): entry location in the live XB (inside Balanced, right zone, wrong zone, outside on the break side, outside against, no live XB) · XB direction vs trade · last XB break with / against · last break kind (flip = CDLx/CDSx, cont = LDx/SDx, internal) · entry inside a live FVA of the trade side.
- Kept vs base (all trades) and kept vs dropped (t diff), per period: NQ 2022–25 (P1), MNQ 2026 (P2).
- Book rule: new Oct 30 rules for C.M4, XCS.M1 longs, X.M3; others native entry / stop / target, stop-target exit, no ½ out.
- Page: artifact "XB Filter Test". Code: /home/claude/allm/xb_filter.py, agg_filter.py.

## Applied (Oct 30 2026) — EDGE PRO + website, NQ / MNQ only
- **X.M4:** skip when the 15m close is already outside the live daily XB on the break side. Real ½-out trades: skipped 84 / 30 made +0.00 / −0.09 avg RR. Kept: n 483 / 159, WR 71% / 81%, avg RR +0.18 / +0.33, PF 1.70 / 2.86, t 4.3 / 4.5. Blended 642 trades, WR 73%, avg +0.22, PF 1.91, t 5.9 (was 756, 72%, +0.18, 1.71, 5.4).
  - Checked on every timeframe: the daily is the one that holds (4h also worse, weaker); on 1h the opposite was true, so only the daily XB is used.
- **C.M1:** skip when the 15m close is inside a live 1h, 4h or daily FVA of its own side. Site trades: skipped 597 / 169 made +0.03 / −0.00. Kept: n 1,727 / 520, avg RR +0.17 / +0.35, t 3.6 / 4.0. Blended 2,247 trades, WR 34%, avg +0.21, PF 1.34, t 5.0 (was 3,012, 33%, +0.16, 1.26, 4.6).
- Pine: switches "X.M4 · skip when already outside the daily XB" and "C.M1 · skip inside a live 1h / 4h / daily FVA" in ④ Edges, ON by default, NQ / MNQ only. The 1h / 4h (18:00 anchor) / daily XB and FVAs are built from the 15m candles inside the 15m core (opposite-side engine).
