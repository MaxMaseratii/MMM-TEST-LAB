# MMM Pullback & Exit Lab — Results (Oct 18 2026)

Data: NQ 1m Dec 2022 – Dec 11 2025 (old, back-adjusted, 1m replay). MNQ 5m/10m/15m + footprint Jul 8 – Oct 16 2026 (new, raw). MNQ 1h/4H/D built from 15m, Jan – Oct 2026 (new). 1 pt cost, limits 1 tick through (5-candle wait, cancel at 1:2), stop wins ties, 100-candle max.
Grid: 16 MMCB types, GMC by c3 type, Zone x box breaks (CONTRACTION / EXPANDER G1) × entries (C, P, MP, BAL, MD, D, XD, O, POC, VA near/far) × stops (fixed 50, structure, ATR×1, ATR×1.5, daily ATR×0.15) × targets (1:1–1:6, candle TGT) × 11 exits. 652,872 combos compared old vs new.

## Answers
- **Pullback location:** plus candles that take their target pull back to P/MP first. Daily BuBC+ (old): takes the high 89%, median pullback to 81% of range; P fills 89% → high after 79%; MP 76% → 62%; BAL 43% → 37%. Same shape 15m–4H.
- **POC is not the best pullback:** BC+ takers filled the POC first only 5–11%. POC fills 57–62%, target after 36–41%; MP fills ~80%, target ~50%; VA near edge ≈ MP. As trades every entry is within ±0.02 RR (fixed 50 1:2: POC −0.016, BAL −0.010, close −0.021, WR 34%). Max-delta price not in the export.
- **Magnifier (HTF signal, LTF entry):** LTF trigger stops make 2R+ targets common (Daily→15m 92%) but WR collapses (19%; Daily→1m 6%), avg RR −0.09 / −0.38. All pairs/triggers ≈ 0 or below (best +0.03). Plain limit at the HTF level with the HTF stop ≈ 0. Pocket: 4H BC− limit at the candle OPEN, HTF stop, target candle extreme: bull +0.35 → +0.40 (94 → 21), bear +0.20 → +0.72 (95 → 26). 4H BuBC− BAL 50: WR 58% → 56%, +0.09 → +0.10.
- **GMC entries by TF:** XU worst on 1h only (c3 BC+: XU −0.07 vs c3 close +0.11 old; −0.01 vs +0.05 new). 5m all negative; 15m all ≈ 0. 4H c3 BC− LONG best: c2 P +0.29, c3 low +0.24, c3 close +0.19 old; c3 close +0.15 new. Daily too few.
- **Best single setup (independently re-verified):** 4H GMC LONG, c3 BC− with the gap, c3 close, ATR×1.5, 1:2, exit after 2 NBCs: 130 trades WR 55% +0.19 → 41 trades WR 56% +0.22. With candle stop + 2-NBC-with-rejection exit: WR 55% → 61%, +0.27 → +0.31.
- **Exits:** no close-based exit beats stop+target on avg RR. 2-NBC exit: WR +10/+11 pts (33% → 45–47%) for −0.002/−0.004 RR. Stall EXIT any close/flip −0.009/−0.005; body-close −0.006/−0.005; SuperTrend flip only 0.000. Early exits cost most at 1:4–1:6.
- **Candle types inside the balance:** next BC continues 51% after 2 NBCs; with an AFs+ rejection WITH the run 56–57%, rejection AGAINST 46–47%, all closes against 43%. Move to next BC ≈ 0 ATR in every group, so type variants (XN2A/XN2R/XN2W) change the exit result by ≤ 0.003 RR.
- **Absorption:** box break direction is set by where the last candle closes in the box: top third 81% up, middle 50%, bottom 19% (7,825 boxes; separate 5m check 86/47/13). Inside the same location footprint adds 1–5 pts (top third, net delta > 0: 82% vs 78%). Big volume/small move at the top with buyers → breaks UP 63% overall (aggressor wins), noise inside location.
- **Prop goal (WR > 60% at ≥ 1:2):** not met in both periods; closest is the 4H GMC c3 BC− line above.
- **Luck check:** 2,217 single combos passed old t ≥ 2.5 + positive new; luck alone ≈ 2,000. Trust themes, not single combos.

## Themes positive in both periods (median over all stop × target × exit)
| Theme | Entry | old → new |
|---|---|---|
| 4H GMC LONG c3 BC− | c3 close | +0.19 → +0.15 |
| 1h GMC SHORT c3 BC−, Asia + NY AM | c3 close | +0.17 → +0.13 |
| 1h GMC LONG c3 AFs against | c3 close | +0.08 → +0.09 |
| 15m Zone x EXPANDER LDx T3+, Asia + NY AM | close | +0.09 → +0.09 |
| 4H BuBC− | BAL 50 | +0.13 → +0.07 |
| Daily BuBC+ | close | +0.07 → +0.18 |

Full results: artifact "MMM Pullback & Exit Lab" (sheet), Docs "MMM Pullback & Exit Lab: Lessons", MMM_full_grid_old_vs_new.csv.gz.

## Added Oct 18 (follow-up)
- **LTF flip entry (CDLc/CDSc after the touch, stop = new LTF T1):** negative on NQ 2022–25 at the HTF target: D→1m −0.24, 4H→1m −0.18, 1h→1m −0.13, 15m→1m −0.20. In 61–68% of signals the HTF target is taken before the LTF flip prints. D→15m +0.20 in 2026 (129) but −0.02 old: not reliable. With the HTF stop or fixed 50 ≈ 0.
- **Live box control (every close inside a live x box, CONTRACTION G1):** top third → breaks up 68–71% (NQ) / 66–72% (MNQ); middle 52–56% / 49–54%; bottom 37–38% / 32–36%. Top third after 7+ inside candles 72% / 79%; bottom 7+ 33% / 32% up. Edges hold more than a random walk (close at 94% of box → 74% up). Delta within location ±3 pts, inconsistent. The 81/19 split above uses the candle before the break (hindsight); use the live numbers in indicators.
- **Universal indicator design direction:** balance control = close location in the box + time spent there (tug-of-war flag), delta only a tie-breaker; pullback zones P/MP after plus candles, BAL after minus candles; HTF stop for HTF ideas (no LTF stop); 2-NBC exit as optional WR mode; Pro Plus stall exit off by default.
