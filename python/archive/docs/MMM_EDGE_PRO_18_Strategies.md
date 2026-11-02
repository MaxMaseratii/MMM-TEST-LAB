# MMM EDGE PRO · all 18 strategies (updated Oct 30 2026)

One indicator holds every working strategy from maxmaserati.com/strategies. **Only X.M4 is on by default.** You turn the others on in **④ Edges**.

Every strategy comes from one of the 4 MMM indicators:
- **X.M#** = MMM PRO x (zone engine)
- **C.M#** = MMM PRO c (candle order flow)
- **XCS.M#** = MMM PRO XCS (x + c + s together)

> Research only, not advice. Pick ONE strategy. Study it, see if it fits your style, backtest it yourself, then decide.

## New rules (Oct 30 2026)

After the full grid (every entry × stop × target × exit), three strategies got better rules. They run on **NQ / MNQ**. ES, gold and crude keep the old rules (the new ones did not hold there). The indicator switches by itself from the chart's market.

| Code | Entry | Stop | Exit | avg RR 2022–25 → 2026 |
|---|---|---|---|---|
| C.M4 | Market at the c3 close (same) | 50 pts (was 1 × ATR) | Full · 1:6 · out at the next session open (02:00 · 08:00 · 09:30) | +0.30 → +0.55 (old +0.13 → +0.31) |
| XCS.M1 longs | Buy limit at MP of the break candle (low + 75%), 10 candles, fills on touch · closed below MP = buy the close | 50 pts | 1:2 full · 100 candles | +0.19 → +0.30 (old +0.12 → +0.26) |
| X.M3 | Market at the close of the 5m candle where the block is born (was a limit at the block top) | Block top − 50 | 1:2 · 100 candles | +0.12 → +0.17 (old +0.12 → +0.12) |

- XCS.M1 shorts keep the old rule (market at the close) and trade full on NQ. They lost in 2026 (−0.05): watch.
- X.M4 did not change: the grid pick lost to the real ½-out rule in 2026.
- C.M4 now trades the full position on NQ (no ½ out). The Statistics table shows the new rule under FULL and the old ½-out rule beside it.

## New codes (old → new)

| Old | New | From | Name |
|---|---|---|---|
| EP.M1 | **X.M4** | MMM PRO x | Zone T3+ break + daily filter · ½ out |
| EP.M4 | **X.M5** | MMM PRO x | Contraction limit (watch) · ½ out |
| EP.M2 | **C.M3** | MMM PRO c | GMC long + daily filter · ½ out |
| EP.M3 | **C.M4** | MMM PRO c | GMC AFs long + daily + 1h filter · ½ out |
| EP.M5 | **C.M5** | MMM PRO c | BC+ long + daily + 1h filter · ½ out |
| LR.M1 | **C.M6** | MMM PRO c | Level retest A · 1m |
| LR.M2 | **C.M7** | MMM PRO c | Level retest B · 1m · 2-candle exit |
| OC.M1 | **C.M8** | MMM PRO c | 09:30 opening candle |

X.M1–X.M3, C.M1–C.M2 and XCS.M1–XCS.M5 keep their codes.

## What is inside

| Code | Name | Target | Chart |
|---|---|---|---|
| X.M1 | Zone T3+ break | 1:6 RR or the opposite break | 1m–15m |
| X.M2 | Zone T3+ limit (watch) | 1:2 RR | 1m–15m |
| X.M3 | 5m iBlock T4+ long · birth close (watch) | 1:2 RR · market at the birth close (NQ) | 1m–5m |
| X.M4 | Zone T3+ break + daily filter | ½ at +0.5R, rest 1:6 RR | 1m–15m |
| X.M5 | Contraction limit (watch) | ½ at +0.5R, rest 1:2 RR | 1m–15m |
| C.M1 | GMC AFs against | 1:6 RR | 1m–15m |
| C.M2 | GMC long 50 | 1:2 RR or the gap-open exit | 1m–15m |
| C.M3 | GMC long + daily | ½ at +0.75R, rest 1:3 RR | 1m–15m |
| C.M4 | GMC AFs long + daily + 1h | NQ: 1:6 RR full, stop 50, out at the next session open · ES / gold: ½ at +0.5R, rest 1:6 RR | 1m–15m |
| C.M5 | BC+ long + daily + 1h | ½ at +0.5R, rest 1:2 RR | 1m–15m |
| C.M6 | Level retest A · stop 40 (watch) | 1:5 RR | 1m only |
| C.M7 | Level retest B · stop 35 (watch) | 1:5 RR or the 2-candle exit | 1m only |
| C.M8 | 09:30 opening candle · stop 50 | 1:3 RR or a close below the 09:30 low | 1m–15m |
| XCS.M1 | P5+ break | 1:2 RR · NQ longs: limit at MP of the break candle | 1m–15m |
| XCS.M2 | Any break | 1:2 RR | 1m–15m |
| XCS.M3 | 4H GMC AFs → 15m pullback BuBC (watch) | 1:2 RR | 1m–15m |
| XCS.M4 | The same, long only (watch) | 1:2 RR | 1m–15m |
| XCS.M5 | iBlock AFs+ (watch) | 1:2 RR | 1m–15m |

## Changes in this build (Oct 28 2026 · "too many tokens" fix)

- All 18 strategies stay in ONE script. The script was over TradingView's size cap, so the extras were cut:
  - STATISTICS shows ONE strategy (picked in ⑤ Tables): Full and ½ out side by side, WR always with its target RR.
  - PROP SURVIVAL table → one PROP line in LIVE, right under the picked strategy: pass % at your size, days, best size.
  - Removed: HOW TO USE table, the 3-strategy comparison, MMPD comparison rows, pending markers, previous high / low lines.
- ① Risk is minimal: Size (MMM Risk Rule · Prop Survival · Manual), Contracts + type (Chart = auto from the chart symbol · Mini · Micro · Nano), Max Drawdown + type, Daily Loss Limit, Profit Target, Min Days.
- Trade tool: shaded risk / reward, entry · stop · (½) · target lines and ONE label per trade (size, SL and TP in pts and $, RR). A trade that ends leaves the chart at once (Keep Finished keeps the last N).
- Prop sim and survival sizing use ONE strategy (the picked one). No "All on" row anywhere.
- Codes renamed (no Z · G · B · C · M). CE10095 fixed. Only the LIVE table shows by default.
- Backup if TradingView still says "too many tokens": MMM_EDGE_PRO_backup_12.pine (12 strategies) + MMM_EDGE_PRO_2_backup_6.pine (X.M3, XCS.M3, XCS.M4, C.M6, C.M7, C.M8).

## Tested numbers (whole test, best exit)

| Code | Trades | WR · target | Avg RR | PF | t |
|---|---|---|---|---|---|
| X.M3 (new) | 2,572 | 47% · 1:2 RR | +0.13 | 1.27 | 5.4 |
| C.M4 (new) | 520 | 50% · 1:6 RR | +0.36 | 1.98 | 5.3 |
| XCS.M1 (new longs + old shorts) | 1,141 | 40% · 1:2 RR | +0.17 | 1.27 | 3.9 |
| XCS.M3 | 276 | 39% · 1:2 RR | +0.16 | 1.27 | 1.9 |
| XCS.M4 | 165 | 44% · 1:2 RR | +0.29 | 1.50 | 2.5 |
| C.M6 | 266 | 37% · 1:5 RR | +0.41 | 1.66 | 3.2 |
| C.M7 | 299 | 19% · 1:5 RR | +0.30 | 1.78 | 3.0 |
| C.M8 | 276 | 41% · 1:3 RR | +0.40 | 1.69 | 3.7 |

- WR = win rate · Avg RR = average result per trade (1 = one stop) · PF = money won ÷ money lost · t-score 2+ = real edge.
- Oct 30 build: not run through TradingView's compiler here. Load it and check the first day by eye.
