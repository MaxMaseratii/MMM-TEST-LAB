# MMM XB: trade only WITH the box direction? (Oct 30 2026)

Question (Max): in a BEARISH XB (born from a BeBC) only sell; in a BULLISH XB only buy. Does selling from the XB zones beat selling at the Balanced Zone?

## Answer: no difference
- **0 passes** in the full grid (6 entry places × 3 stops × 3 targets × 3 exits, 5m / 15m / 1h / 4h / daily), WITH or AGAINST the box.
- **Coin flip, both ways.** After a touch, price ran 50 pts the trade's way first: bearish box, sells 48–51% at every entry place (XB high, XBB middle, Balanced top, Balanced middle, Balanced bottom, XBS middle); against-the-box buys 49–50%. Bullish box, buys 46–52%; sells 48–53%.
- **50 pt stop, 1:2, sells in a bearish box, avg RR P1 → P2:** 15m Balanced top −0.003 → +0.001 · Balanced middle −0.021 → +0.048 · XB high −0.046 → −0.067 · XBB middle −0.019 → −0.056. Buys in a bullish box are the same story (15m Balanced bottom +0.008 → −0.015).
- **Range trades (enter at the Balanced edge, target the other XB edge):** WITH the box hits more often (15m bearish 60% / 54% vs against 48% / 46%), but only because of the box shape: in a bearish box the Balanced Zone sits near the XB low, so the target is closer (median 18 vs 27 pts) and the violation edge farther (17 vs 8.5 pts). The money is no better: 15m WITH −2.1 / −4.8 pts a trade vs AGAINST −1.4 / +2.0.
- **Conclusion:** the box direction and the zone do not change the edge. The XB is a map of where the block can break; it is not an entry by itself.

Method: same as MMM_XB_Zone_Test_Results.md and MMM_XB_Range_Odds.md, split by the XB direction (the BC that started it), opposite-side engine, NQ 2022–25 → MNQ 2026. Code: /home/claude/xb/xbzone3.py, xbrange3.py, agg_zone3.py.
