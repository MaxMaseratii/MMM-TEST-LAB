# MMM XB Break Test by kind: CDLx / CDSx and the rest (Oct 30 2026)

## Verdict
- **CDLx / CDSx (XB break that is also a zone-engine flip) is not a trade on its own.** 0 of 19,852 pairings passed on NQ (t-score 2+ in both periods), on 5m, 15m, 1h or 4h, either side. Random candles: 0 too.
- **50 pt stop, 1:2, market at the break close:** no timeframe and side made money in both periods (15m CDLx −0.08 → −0.04 avg RR · 15m CDSx −0.14 → +0.27 · 5m CDLx −0.09 → −0.06 · 5m CDSx −0.08 → +0.05).
- **Walk-forward:** the best 2022–25 pairing faded in 2026 on every timeframe (15m CDLx, limit at the FVA top, ATR stop, 1:6: +0.63 → +0.21, t 2.4 → 0.6).
- **After a CDLx / CDSx:** the next candle is an NBC 2 times out of 3; only about 1.4 more BCs come before the first opposite BC (about 4 candles); the close 10 candles later is on the break side about half the time (47–56%; 1h 2026 only 35% on 40 breaks). Points moved before the first opposite BC (median): 5m 15 / 27 · 15m 28 / 56 · 1h 58 / 91 · 4h 65 / 142 (P1 / P2).
- **The one lead: LDx (continuation XB break), 5m, longs.** 50 pt stop, market at the break close, 1:10 (or out on a close back through the FVA): +0.12 → +0.45 avg RR, t 3.0 / 2.9, 1,940 / 323 trades. Random 5m longs with the same rule: +0.07 → +0.07. 58 pairings pass, all long, all 5m. It rides the 2022–26 uptrend; SDx shorts do not hold. Not on ES / gold / crude. Watch only.
- **Other markets:** ES: 15 passes (internal cdlx/cdsx), gold: 0, crude: passes include random candles (the trend).
- **Balanced Zone or not:** the zone tests already showed it makes no difference to direction: buy / sell zones, Balanced Zone and the wrong zone all give the same coin flip. Balanced targets are only closer.

## Method
- Break kinds (MMM PRO x 4.0 labels): CDLx / CDSx = XB break close is also a zone-engine flip · LDx / SDx = also a continuation · small cdlx / cdsx / ldx / sdx = internal breaks (no engine event) · all XB breaks · RANDOM candles.
- XB engine: opposite side only. Zone engine: Python port of f_zoneEngine (gate off).
- FVA zone: bear = first NBC body bottom → XB high · bull = XB low → first NBC body top.
- Full grid: 16 entries (native = market at the break close, market, break-candle ladder XD..XP, FVA ladder XD..XP; limits wait 10 candles) × 6 stops (native = 2 ticks past the FVA far edge, fixed 50 scaled, 1.5 ATR, past the break candle, past the FVA far side, past the FVA 50%) × 7 targets (1:1 → 1:10) × 4 exits (stop / target, close through the FVA (violation), next session open, first opposite BC close). Bull and bear apart.
- NQ 1m Dec 2022 – Dec 2025 (P1) → MNQ 2026 (P2); ES / gold / crude = their own Dec 2025 – Oct 2026 data in two halves. Stop wins ties, cost per trade, limits fill when price trades the level.
- Page: artifact "CDLx CDSx Break Test". Code: /home/claude/allm/sig_xbbrk.py, run_xbbrk.py, agg_xbbrk.py, build_cdl_page.py.
