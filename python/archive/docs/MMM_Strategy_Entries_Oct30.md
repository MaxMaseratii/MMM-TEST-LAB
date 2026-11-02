# MMM Strategy Book · exact entry of every strategy (Oct 30 2026)

Every strategy on maxmaserati.com/strategies, with its exact entry, stop and exit, as the site shows them today.

- **NEW** = rules changed on Oct 30 2026 after the full grid test (every entry × stop × target × exit, picked on NQ 2022–25, checked on MNQ 2026).
- The new rules are for **NQ / MNQ**. On ES, gold and crude the new rules did not hold, so those markets keep the old rules.
- **X.M4 did not change.** Its grid "winner" beat the old rule in 2022–25 but lost to it in 2026 (+0.25 vs +0.33 avg RR), so the old ½-out rule stays.
- Stats: WR = win rate · avg RR = average result per trade (1 = one stop) · PF = money won ÷ money lost · t = t-score (2+ = probably not luck). NQ 2022–25 → MNQ 2026, after costs.

## The 3 new rules

| Code | Entry | Stop | Exit | WR | avg RR 2022–25 → 2026 | t 2022–25 / 2026 |
|---|---|---|---|---|---|---|
| **C.M4** Gap Shakeout Long | Market at the c3 close (same as before) | 50 pts (was 1 × ATR) | Full position · 1:6 · out at the next session open (02:00 · 08:00 · 09:30) | 51% → 48% | +0.30 → +0.55 (old: +0.13 → +0.31) | 4.2 / 3.2 |
| **XCS.M1** Late Trend Break · longs | Buy limit at MP of the break candle (low + 75% of range), waits 10 candles, fills on touch. Closed below MP = buy the close | 50 pts | 1:2 full · out after 100 candles | 41% → 44% | +0.19 → +0.30 (old longs: +0.12 → +0.26) | 3.1 / 2.7 |
| XCS.M1 · shorts | Unchanged: market at the break close | 50 pts | 1:2 · out after 60 candles | 38% → 32% | +0.11 → −0.05 (watch) | 1.4 / −0.4 |
| **X.M3** Block Birth Buy (was Block Top Buy) | Market at the close of the 5m candle where the T4+ iBlock is born (was: limit at the block top) | Block top − 50 (avg risk 66 pts) | 1:2 · out after 100 candles | 48% → 44% | +0.12 → +0.17 (old: +0.12 → +0.12) | 4.9 / 2.3 |

Fixed 50 pt stop at 1:2 (always checked): C.M4 +0.21 → +0.41 (t 2.8 / 3.1) · XCS.M1 longs = the rule above · X.M3 50 from the entry +0.10 → +0.16 (t 3.8 / 2.1).

Other markets with the new rules (longs, both halves of Dec 2025 – Oct 2026): C.M4 ES weak (+0.05) · gold no edge (−0.12). XCS.M1 ES weak · gold no edge · crude weak. X.M3 ES PASS · edge (+0.20, t 2.6) · gold and crude no edge. So ES / gold / crude keep the old rules.

## Every strategy

### C.M8 · Opening Breakout
MMM PRO c · 15m · Long only · status TRADE · WR 41% · avg RR +0.40 (+0.42 → +0.31) · PF 1.69 · t 3.75 · 276 trades

- **Chart:** Any chart from 1m to 15m, MMM EDGE PRO, C.M8 on.
- **Before 09:30:** Mark the pre-open high: the highest price from 08:00 to 09:30 New York.
- **Wait for:** The 09:30 15m candle is a BuBC: it closes above the previous 15m candle’s high.
- **Filter:** It also closes ABOVE the pre-open high. If it closes inside the pre-open range, no trade.
- **Entry:** Buy at its close, 09:45.
- **Stop:** Fixed 50 pts (ES 20).
- **Target:** 1:3 (150 pts).
- **Get out early:** At the first 15m close below the 09:30 candle’s low. Otherwise out at the 16:59 close.

### C.M6 · Level Bounce Max
MMM PRO c · 1m entry, 15m trend · Long only · status WATCH · WR 37% · avg RR +0.42 (+0.42 → +0.47) · PF 1.67 · t 3.25 · 265 trades

- **Chart:** 1 minute, MMM EDGE PRO, C.M6 on. The levels are drawn for you.
- **Before 09:30:** Mark the levels: daily open 18:00, PDH / PDL, overnight high / low (18:00–09:30), Asia high / low (18:00–02:00), 09:30 open, prior 16:00 close, the newest live H1 / H4 GMC.
- **Trend:** The 15m MMM structure is up (the last 15m flip was a CDL) on the last closed 15m candle.
- **Wait for:** A 1m CDL: the 1m structure flips up, and its new PO4 T1 is within 15 pts of a level.
- **Skip if:** A bullish GMC formed between the PO4 T1 and the CDL with its level inside that range (a gap).
- **Entry:** At the CDL close, place a buy limit at the PO4 T1 (fills 1 tick through). Cancel at +80 pts untouched or after 60 candles. A candle closing below the T1 does not cancel it.
- **Stop:** 40 pts below the entry.
- **Target:** 1:5 (200 pts). No early exit. Out at the 16:59 close if nothing hits. One trade at a time.

### C.M7 · Level Bounce Safe
MMM PRO c · 1m entry, 15m trend · Long only · status WATCH · WR 19% · avg RR +0.30 (+0.31 → +0.28) · PF 1.78 · t 2.96 · 299 trades

- **Chart:** 1 minute, MMM EDGE PRO, C.M7 on. The levels are drawn for you.
- **Before 09:30:** Mark the same levels as C.M6.
- **Setup:** Same as C.M6: 15m trend up, 1m CDL with its PO4 T1 within 15 pts of a level, no gap.
- **Entry:** Buy limit at the PO4 T1, placed at the CDL close. Cancel at +70 pts untouched or after 60 candles.
- **Stop:** 35 pts below the entry.
- **Get out early:** Max’s 2-candle exit: after a 1m close below the T1 (candle V), get out when a later candle closes below V’s low. A close back above the T1 resets it.
- **Target:** 1:5 (175 pts). Out at the 16:59 close if nothing hits. One trade at a time.

### X.M4 · Third Break
MMM PRO x · 15m · Long and short · status TRADE · WR 72% · avg RR +0.18 (+0.15 → +0.26) · PF 1.71 · t 5.38 · 756 trades

- **Chart:** 15 minutes, MMM EDGE PRO, X.M4 on. Read only CLOSED candles.
- **Wait for:** A 3rd or later break of the same trend: a 15m candle closes past the expander box (LDx2+ for longs, SDx2+ for shorts). The new PO4 is T3 or higher.
- **Filter:** Yesterday’s daily candle points your way: green for longs, red for shorts.
- **Entry:** Market order at the close of that break candle.
- **Stop:** 1.5 × ATR(14) of the 15m chart, away from the entry.
- **Exit:** Take half off at +0.5R and move the stop to entry. The runner goes to the first opposite break or 1:6.

### C.M3 · Gap Jump Long
MMM PRO c · 15m · Long only · status TRADE · WR 60% · avg RR +0.08 (+0.06 → +0.14) · PF 1.21 · t 3.95 · 2431 trades

- **Chart:** 15 minutes, MMM EDGE PRO, C.M3 on.
- **Wait for:** A bullish GMC: candle 2 closes above candle 1’s high and candle 3’s low stays above candle 1’s high (a gap).
- **Filter:** Yesterday’s daily candle is green.
- **Entry:** Market order at the close of candle 3.
- **Stop:** 1 × ATR(14) of the 15m chart below the entry.
- **Exit:** Half off at +0.75R, stop to entry. The runner goes to 1:3.

### C.M4 · Gap Shakeout Long · **NEW Oct 30**
MMM PRO c · 15m · Long only · status TRADE · WR 50% · avg RR +0.36 (+0.30 → +0.55) · PF 1.98 · t 5.3 · 520 trades

- **Chart:** 15 minutes, MMM EDGE PRO, C.M4 on.
- **Wait for:** A bullish GMC where candle 3 makes a new high but closes back INSIDE candle 2 (AFs against the gap).
- **Filter:** Yesterday’s daily candle is green AND the 1h box trend is up.
- **Entry:** Market order at the close of candle 3.
- **Stop:** Fixed 50 pts below the entry (NQ / MNQ).
- **Target:** Full position, no half off. Target 1:6.
- **Exit:** Out at the open of the next session (02:00, 08:00 or 09:30 New York) if the stop or the target did not hit first.
- **Other markets:** ES and gold keep the old rule: stop 1 × ATR(14), half off at +0.5R, runner to 1:6. The new exit did not hold there.

### C.M5 · Power Candle Long
MMM PRO c · 15m · Long only · status TRADE · WR 63% · avg RR +0.07 (+0.06 → +0.07) · PF 1.25 · t 5.08 · 3029 trades

- **Chart:** 15 minutes, MMM EDGE PRO, C.M5 on.
- **Wait for:** A BC+ bull candle: it closes above the previous high, makes no new low and closes in its upper half.
- **Filter:** Yesterday’s daily candle is green AND the 1h box trend is up.
- **Entry:** Market order at the close of that candle.
- **Stop:** Fixed 50 pts (ES 20).
- **Exit:** Half off at +0.5R, stop to entry. The runner goes to 1:2.

### X.M5 · Breakout Pullback Long
MMM PRO x · 15m · Long only · status WATCH · WR 62% · avg RR +0.07 (+0.08 → +0.06) · PF 1.35 · t 2.33 · 363 trades

- **Chart:** 15 minutes, MMM EDGE PRO, X.M5 on (contraction boxes).
- **Wait for:** A bullish continuation break of a contraction box (LDx).
- **Filter:** Yesterday’s daily candle is green.
- **Entry:** Buy limit at 75% down the break candle (MP). It fills 1 tick through. Cancel after 20 candles, at the next session open, on the next break, if the target prints first, or on a close below the break candle.
- **Stop:** Fixed 50 pts (ES 20).
- **Exit:** Half off at +0.5R, stop to entry. The runner goes to 1:2.

### X.M1 · Third Break · Asia + NY AM
MMM PRO x · 15m · Long and short · status TRADE · WR 42% · avg RR +0.23 (+0.20 → +0.29) · PF 1.49 · t 5.19 · 1290 trades

- **Chart:** 15 minutes, MMM PRO x, box engine G1 (expander). Also runs inside MMM EDGE PRO.
- **Wait for:** A 3rd or later break: a 15m close past the box (LDx2+ / SDx2+), new PO4 T3 or higher.
- **Entry:** Market order at the close of the break candle.
- **Stop:** 1.5 × ATR(14) of the 15m chart.
- **Exit:** The whole position: out at the first opposite break (X5 OPP) or at 1:6.

### X.M2 · Third Break Pullback
MMM PRO x · 15m · Long and short · status WATCH · WR 43% · avg RR +0.12 (+0.14 → +0.04) · PF 1.26 · t 2.91 · 827 trades

- **Chart:** 15 minutes, MMM PRO x, contraction boxes. Also runs inside MMM EDGE PRO.
- **Wait for:** A T3+ continuation break of a contraction box (LDx2+ / SDx2+).
- **Entry:** Limit at 75% back into the break candle (MP for longs, MD for shorts), 1 tick through.
- **Stop:** Fixed 50 pts (ES 20).
- **Exit:** Target 1:2, whole position.

### X.M3 · Block Birth Buy · **NEW Oct 30**
MMM PRO x · 5m · Long only · status WATCH · WR 47% · avg RR +0.13 (+0.12 → +0.17) · PF 1.27 · t 5.38 · 2572 trades

- **Chart:** 1m to 5m chart, MMM EDGE PRO, X.M3 on (it reads 5m candles). Or MMM PRO x on 5m, iBlocks on.
- **Wait for:** A bullish iBlock of a T4 or higher PO4 (the 3rd continuation or later).
- **Entry:** Market order at the close of the 5m candle where the block is born (the T4+ break candle). No limit, no waiting.
- **Stop:** 50 pts below the TOP of the block (ES 20). Your risk is a bit more than 50 pts: about 66 on average.
- **Exit:** Target 1:2. Out after 100 candles if nothing hits.
- **Other markets:** ES, gold and crude keep the old rule: buy limit at the block top, stop 50, 1:2.

### C.M1 · Gap Shakeout
MMM PRO c · 15m · Long and short · status TRADE · WR 33% · avg RR +0.16 (+0.13 → +0.26) · PF 1.26 · t 4.62 · 3012 trades

- **Chart:** 15 minutes, MMM PRO c. Also runs inside MMM EDGE PRO.
- **Wait for:** A GMC where candle 3 sweeps past candle 2 and closes back inside it (AFs against the gap).
- **Entry:** Market order at the close of candle 3, in the GMC direction.
- **Stop:** 1 × ATR(14) of the 15m chart.
- **Exit:** Out at the first confirmed opposite body close (X1) or at 1:6.

### C.M2 · Gap Jump · Fixed Stop
MMM PRO c · 15m · Long only · status TRADE · WR 42% · avg RR +0.07 (+0.06 → +0.12) · PF 1.17 · t 4.65 · 5186 trades

- **Chart:** 15 minutes, MMM PRO c. Also runs inside MMM EDGE PRO.
- **Wait for:** Any bullish GMC (candle 2 closes above candle 1, candle 3 keeps the gap).
- **Entry:** Market order at the close of candle 3.
- **Stop:** Fixed 50 pts (ES 20).
- **Exit:** Target 1:2. Get out early on a confirmed close below the gap candle’s open (X3-O).

### XCS.M1 · Late Trend Break · **NEW Oct 30**
MMM PRO XCS (x + c + s) · 15m · Long and short · status TRADE · WR 40% · avg RR +0.17 (+0.17 → +0.17) · PF 1.27 · t 3.86 · 1141 trades

- **Chart:** 15 minutes, MMM EDGE PRO, XCS setups on (engines x, c and s together).
- **Wait for:** The 5th or later break of the same trend: a candle closes past P5, P6… (LD5+ / SD5+). The new PO4 is T6 or higher.
- **Entry · longs:** Buy limit at MP of the break candle: its low + 75% of its range (25% down from the high). It waits 10 candles and fills on a touch. If the candle closed below MP, buy at its close.
- **Entry · shorts:** Market order at the close of the break candle (unchanged).
- **Stop:** Fixed 50 pts (ES 20).
- **Exit:** Target 1:2, full position. Longs: out after 100 candles if nothing hits. Shorts: out after 60 candles.
- **Other markets:** ES, gold and crude keep the old rule: market order at the close, both sides.

### XCS.M2 · Any Trend Break
MMM PRO XCS (x + c + s) · 15m · Long and short · status TRADE · WR 37% · avg RR +0.05 (+0.06 → +0.04) · PF 1.08 · t 3.45 · 8653 trades

- **Chart:** 15 minutes, MMM EDGE PRO, XCS setups on.
- **Wait for:** A candle closes past any P# of the current trend (LD / SD, first one or later).
- **Entry:** Market order at the close of the break candle.
- **Stop:** Fixed 50 pts (ES 20).
- **Exit:** Target 1:2 (1:1 also works). Out after 60 candles.

### XCS.M3 · 4H Green Light
MMM PRO XCS (x + c + s) · 4H filter, 15m entry · Long and short · status WATCH · WR 40% · avg RR +0.17 (+0.18 → +0.09) · PF 1.27 · t 1.86 · 276 trades

- **Chart:** Any chart from 1m to 15m, MMM EDGE PRO, XCS.M3 on. The 4H filter and the 15m entry are built inside.
- **Filter:** On 4H, price touches a bull GMC (the gap edge = candle 1 high) and, on that candle or within 3 candles, prints a bullish AFs. No 4H close below the GMC open. The filter lives 6 four-hour candles and dies on a 4H close below the AFs low. Mirror for shorts.
- **Wait for:** On 15m: a CDL of engine x, c or s, then a bearish BC (the pullback).
- **Entry:** Market order at the close of the next 15m BuBC (the first bull body close after the pullback).
- **Stop:** Fixed 50 pts (ES 20).
- **Exit:** Target 1:2. Out after 60 four-hour candles.

### XCS.M4 · 4H Green Light Long
MMM PRO XCS (x + c + s) · 4H filter, 15m entry · Long only · status WATCH · WR 44% · avg RR +0.29 (+0.25 → +0.48) · PF 1.5 · t 2.49 · 165 trades

- **Chart:** Any chart from 1m to 15m, MMM EDGE PRO, XCS.M4 on. The 4H filter and the 15m entry are built inside.
- **Filter:** On 4H, price touches a bull GMC and prints a bullish AFs within 3 candles. No 4H close below the GMC open. The filter lives 6 four-hour candles.
- **Wait for:** On 15m: a CDL of engine x, c or s, then a bearish BC (the pullback).
- **Entry:** Market order at the close of the next 15m BuBC.
- **Stop:** Fixed 50 pts (ES 20).
- **Exit:** Target 1:2. Out after 60 four-hour candles.

### XCS.M5 · Pre-Market Sweep
MMM PRO XCS (x + c + s) · 15m · Long and short · status WATCH · WR 43% · avg RR +0.25 (+0.21 → +0.36) · PF 1.42 · t 2.41 · 205 trades

- **Chart:** 15 minutes, MMM EDGE PRO, XCS setups on, iBlocks on.
- **Wait for:** The first touch of an iBlock (the origin box of a T2 or higher PO4).
- **Then:** Within 10 candles, an AFs+ in the block direction: it sweeps the previous candle, closes back inside it, in the good half. No close through the PO4 line first.
- **Entry:** Market order at the close of the AFs+ candle.
- **Stop:** 1 tick past the AFs+ candle’s low (long) / high (short).
- **Exit:** Target 1:2. Out after 60 candles.

### FVA.M1 · Goalkeeper · 1H Gap
MMM PRO FVA · 5m · Long and short · status TRADE · WR 36% · avg RR +0.10 (+0.08 → +0.30) · PF 1.22 · t 3.11 · 1403 trades

- **Chart:** MMM PRO FVA on the 5m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the H1 UPG gap for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 5m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level.
- **Filter:** No candle closed through the level before the box printed (the level held).
- **Entry:** Limit order at the reversal box edge: its top for longs, its bottom for shorts. The first touch fills.
- **Stop:** 1 tick past the reversal box low (long) / high (short), at least 20 and at most 50 pts.
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:2 RR.
- **Trail:** After the first opposite candle, wait for a BC in profit, then move the stop to that pullback low / high.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M2 · Goalkeeper · NY Afternoon
MMM PRO FVA · 5m · Long and short · status TRADE · WR 47% · avg RR +0.08 (+0.07 → +0.27) · PF 1.34 · t 3.64 · 1338 trades

- **Chart:** MMM PRO FVA on the 5m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the UPG gap (M15 · H1 · H4 · D · W) for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 5m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level.
- **Filter:** Only take fills from 12:00 to 16:00 New York.
- **Entry:** Limit order at the reversal box edge: its top for longs, its bottom for shorts. The first touch fills.
- **Stop:** Fixed 50 pts (ES 20).
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:3 RR.
- **Trail:** Once in profit, move the stop under each new BC (over it for shorts).
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M3 · Goalkeeper · NY Morning
MMM PRO FVA · 5m · Long and short · status TRADE · WR 43% · avg RR +0.13 (+0.12 → +0.32) · PF 1.27 · t 3.21 · 933 trades

- **Chart:** MMM PRO FVA on the 5m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the M15 UPG gap for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 5m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level.
- **Filter:** Only take fills from 09:30 to 12:00 New York.
- **Entry:** Limit order at the reversal box edge: its top for longs, its bottom for shorts. The first touch fills.
- **Stop:** 1 tick past the reversal box low (long) / high (short), at least 20 and at most 50 pts.
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:2 RR.
- **Trail:** Once in profit, move the stop under each new BC (over it for shorts).
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M4 · Goalkeeper · PM Range Low
MMM PRO FVA · 5m · Long only · status WATCH · WR 49% · avg RR +0.10 (+0.09 → +0.32) · PF 1.45 · t 2.44 · 377 trades

- **Chart:** MMM PRO FVA on the 5m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the NY PM opening range low (13:30–13:45 New York) for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 5m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level.
- **Entry:** Limit order at the reversal box edge: its top for longs, its bottom for shorts. The first touch fills.
- **Stop:** Fixed 50 pts (ES 20).
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:3 RR.
- **Trail:** Once in profit, move the stop under each new BC (over it for shorts).
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M5 · Goalkeeper · Session High/Low
MMM PRO FVA · 5m · Long and short · status TRADE · WR 43% · avg RR +0.09 (+0.09 → +0.15) · PF 1.22 · t 3.33 · 1908 trades

- **Chart:** MMM PRO FVA on the 5m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the session or range high / low (Asia, London, pre-open, Globex, NY AM, NY PM) for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 5m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level.
- **Filter:** Trade only in the MMM PRO FVA H1 trend direction.
- **Entry:** Limit order at the reversal box edge: its top for longs, its bottom for shorts. The first touch fills.
- **Stop:** 1 tick past the reversal box low (long) / high (short), at least 20 and at most 50 pts.
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:3 RR.
- **Trail:** Once in profit, move the stop under each new BC (over it for shorts).
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M6 · Morning Runner
MMM PRO FVA · 1m · Long and short · status TRADE · WR 28% · avg RR +0.22 (+0.20 → +0.59) · PF 1.42 · t 2.4 · 555 trades

- **Chart:** MMM PRO FVA on the 1m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the MMM PRO FVA M15 internal box for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 1m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level.
- **Filter:** Only take fills from 09:30 to 12:00 New York.
- **Entry:** Limit order at the reversal box edge: its top for longs, its bottom for shorts. The first touch fills.
- **Stop:** Fixed 20 pts.
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** No target: a runner.
- **Trail:** After the first opposite candle, wait for a BC in profit, then move the stop to that pullback low / high.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M7 · Goalkeeper · London
MMM PRO FVA · 1m · Long and short · status TRADE · WR 39% · avg RR +0.14 (+0.10 → +0.33) · PF 1.67 · t 2.67 · 216 trades

- **Chart:** MMM PRO FVA on the 1m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the MMM PRO FVA Bu / Be LEZ (M15 · H1 · H4) for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 1m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level.
- **Filter:** No candle closed through the level before the box printed (the level held).
- **Filter:** Only take fills from 02:00 to 08:00 New York.
- **Entry:** Limit order at the reversal box edge: its top for longs, its bottom for shorts. The first touch fills.
- **Stop:** Fixed 20 pts.
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:2 RR.
- **Trail:** After the first opposite candle, wait for a BC in profit, then move the stop to that pullback low / high.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M8 · Goalkeeper · Any Gap
MMM PRO FVA · 5m · Long and short · status TRADE · WR 34% · avg RR +0.06 (+0.06 → +0.11) · PF 1.14 · t 3.97 · 5530 trades

- **Chart:** MMM PRO FVA on the 5m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the UPG gap (M15 · H1 · H4 · D · W) for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 5m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level.
- **Filter:** No candle closed through the level before the box printed (the level held).
- **Entry:** Limit order at the reversal box edge: its top for longs, its bottom for shorts. The first touch fills.
- **Stop:** 1 tick past the reversal box low (long) / high (short), at least 20 and at most 50 pts.
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:2 RR.
- **Trail:** After the first opposite candle, wait for a BC in profit, then move the stop to that pullback low / high.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M9 · 1H Box Retest
MMM PRO FVA · 5m · Long and short · status WATCH · WR 16% · avg RR +0.22 (+0.23 → +0.12) · PF 1.78 · t 2.21 · 230 trades

- **Chart:** MMM PRO FVA on the 5m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the MMM PRO FVA H1 box (T#, P#, R#, internal, break box or LEZ) for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 5m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level.
- **Filter:** No candle closed through the level before the box printed (the level held).
- **Filter:** Trade only in the MMM PRO FVA H1 trend direction.
- **Retest:** Price comes back and touches the reversal box, but no candle closes inside it.
- **Entry:** A BC closes out of the box: enter at the next open.
- **Stop:** 1 tick past the reversal box low (long) / high (short), at least 20 and at most 50 pts.
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:5 RR.
- **Trail:** After 1 BC in profit, move the stop to entry.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M10 · Open Door Long
MMM PRO FVA · 5m · Long only · status TRADE · WR 37% · avg RR +0.23 (+0.19 → +0.59) · PF 1.42 · t 3.88 · 1039 trades

- **Chart:** MMM PRO FVA on the 5m chart. Read only CLOSED candles.
- **Wait for:** An LD: a 5m candle closes above the last bull box (a continuation break).
- **Then:** Count the next 3 candles. None of them may close back inside the broken box.
- **Entry:** Buy at the open of the 4th candle.
- **Stop:** 1 tick past the reversal box low (long) / high (short), at least 20 and at most 50 pts.
- **Get out early:** A candle closes back below the broken box: out at that close.
- **Target:** 1:10 RR.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M11 · Open Door · 15m
MMM PRO FVA · 15m · Long and short · status TRADE · WR 37% · avg RR +0.18 (+0.17 → +0.27) · PF 1.43 · t 2.66 · 641 trades

- **Chart:** MMM PRO FVA on the 15m chart. Read only CLOSED candles.
- **Wait for:** An LD (long) or SD (short): a 15m candle closes past the last box in the trend direction.
- **Then:** Count the next 3 candles. None of them may close back inside the broken box.
- **Entry:** Enter at the open of the 4th candle.
- **Stop:** Fixed 50 pts (ES 20).
- **Get out early:** A candle closes back below the broken box (above it for shorts): out at that close.
- **Target:** 1:10 RR.
- **Trail:** After the first opposite candle, wait for a BC in profit, then move the stop to that pullback low / high.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M12 · 1H Breakout Ride
MMM PRO FVA · 1h · Long only · status WATCH · WR 40% · avg RR +0.39 (+0.37 → +0.55) · PF 1.87 · t 3.22 · 212 trades

- **Chart:** MMM PRO FVA on the 1h chart. Read only CLOSED candles.
- **Wait for:** An LD: a 1h candle closes above the last bull box.
- **Entry:** Buy at the open of the next 1h candle.
- **Stop:** 1 tick past the reversal box low (long) / high (short), at least 20 and at most 50 pts.
- **Get out early:** A 1h candle closes back below the broken box.
- **Target:** 1:5 RR.
- **Trail:** Once in profit, move the stop under each new BC (over it for shorts).
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M13 · Asia Wick Retest
MMM PRO FVA · 15m · Long and short · status WATCH · WR 43% · avg RR +0.23 (+0.21 → +0.52) · PF 1.61 · t 3.53 · 317 trades

- **Chart:** MMM PRO FVA on the 15m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the UPG gap (M15 · H1 · H4 · D · W) for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 15m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level.
- **Filter:** No candle closed through the level before the box printed (the level held).
- **Filter:** Only take entries from 18:00 to 02:00 New York.
- **Retest:** Price comes back and only wicks into the box: no candle closes inside it.
- **Entry:** A BC closes out of the box: enter at the next open.
- **Stop:** 1 tick past the reversal box low (long) / high (short), at least 20 and at most 50 pts.
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:2 RR.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M14 · Half-Candle Dip
MMM PRO FVA · 5m · Long and short · status WATCH · WR 36% · avg RR +0.42 (+0.38 → +1.05) · PF 1.72 · t 3.23 · 330 trades

- **Chart:** MMM PRO FVA on the 5m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the H1 UPG gap for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 5m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level. Then a 2nd BC must close in your direction before any retest.
- **Filter:** No candle closed through the level before the box printed (the level held).
- **Retest:** Price comes back and touches the box.
- **Entry:** A BC closes out of the box: place a limit at 50% of that BC. Cancel if price closes back past the box first.
- **Stop:** 1 tick past the reversal box low (long) / high (short), at least 10 pts (ES 4 · gold 2.4 · crude 0.10), no cap.
- **Target:** 1:10 RR.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M15 · Half-Candle Dip · London
MMM PRO FVA · 15m · Long and short · status WATCH · WR 45% · avg RR +0.15 (+0.11 → +0.49) · PF 1.63 · t 2.42 · 216 trades

- **Chart:** MMM PRO FVA on the 15m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the UPG gap (M15 · H1 · H4 · D · W) for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 15m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level. Then a 2nd BC must close in your direction before any retest.
- **Filter:** Only take entries from 02:00 to 08:00 New York.
- **Retest:** Price comes back and only wicks into the box.
- **Entry:** A BC closes out of the box: place a limit at 50% of that BC.
- **Stop:** Fixed 50 pts (ES 20).
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:3 RR.
- **Trail:** Once in profit, move the stop under each new BC (over it for shorts).
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M16 · Max Re-entry
MMM PRO FVA · 5m · Long and short · status WATCH · WR 16% · avg RR +0.25 (+0.20 → +0.81) · PF 1.78 · t 1.82 · 392 trades

- **Chart:** MMM PRO FVA on the 5m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the H1 UPG gap for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 5m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level. Then a 2nd BC must close in your direction before any retest.
- **Filter:** No candle closed through the level before the box printed (the level held).
- **Retest:** Price comes back and touches the box.
- **Entry:** A BC closes out of the box: enter at the next open.
- **Stop:** 1 tick past the reversal box low (long) / high (short), at least 20 and at most 50 pts.
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** No target: a runner.
- **Manage:** After the 1st BC in profit, move the stop to entry + 1 pt (fees).
- **Re-enter:** Stopped or out at BE and the box still holds? Wait for touch → BC out again and re-enter. Up to 3 times.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M17 · Clean Gap Retest
MMM PRO FVA · 15m · Long and short · status TRADE · WR 37% · avg RR +0.15 (+0.14 → +0.18) · PF 1.29 · t 3.17 · 965 trades

- **Chart:** MMM PRO FVA on the 15m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the UPG gap (M15 · H1 · H4 · D · W) for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 15m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level.
- **Filter:** No candle closed through the level before the box printed (the level held).
- **Retest:** Price comes back and only wicks into the box: no candle closes inside it.
- **Entry:** The 1st BC that closes out of the box: enter at the next open.
- **Stop:** 1 tick past the reversal box low (long) / high (short), at least 20 and at most 50 pts.
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:3 RR.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M18 · Sniper 1:10
MMM PRO FVA · 15m · Long and short · status WATCH · WR 26% · avg RR +0.20 (+0.18 → +0.48) · PF 1.3 · t 1.88 · 534 trades

- **Chart:** MMM PRO FVA on the 15m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the M15 UPG gap for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 15m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level.
- **Filter:** No candle closed through the level before the box printed (the level held).
- **Retest:** Price comes back and only wicks into the box.
- **Entry:** The 1st BC that closes out of the box: place a limit at the high it broke (low for shorts).
- **Stop:** Fixed 20 pts.
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:10 RR.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M19 · Box Retest 1:2
MMM PRO FVA · 5m · Long and short · status TRADE · WR 41% · avg RR +0.14 (+0.14 → +0.17) · PF 1.27 · t 2.66 · 613 trades

- **Chart:** MMM PRO FVA on the 5m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the MMM PRO FVA break box: CDL, CDS, LD or SD on M15 / H1 / H4 for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 5m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level. The box must hold an NBC inside it (not BC on BC).
- **Retest:** Price comes back and touches the box.
- **Entry:** The 1st BC that closes out of the box: enter at the next open.
- **Stop:** 1 tick past the reversal box low (long) / high (short), at least 20 and at most 50 pts.
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:2 RR.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M20 · Fast Retest
MMM PRO FVA · 15m · Long and short · status WATCH · WR 35% · avg RR +0.08 (+0.08 → +0.09) · PF 1.16 · t 1.63 · 953 trades

- **Chart:** MMM PRO FVA on the 15m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the UPG gap (M15 · H1 · H4 · D · W) for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 15m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level. The very next candle after the break candle is already the retest: no 2nd BC, NBC or opposite candle in between.
- **Filter:** No candle closed through the level before the box printed (the level held).
- **Retest:** The candle right after the break touches the box.
- **Entry:** The 1st BC that closes out of the box: enter at the next open.
- **Stop:** 1 tick past the reversal box low (long) / high (short), at least 20 and at most 50 pts.
- **Get out early:** A candle closes back below the reversal box (long) / above it (short): out at that close.
- **Target:** 1:5 RR.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M21 · Pause, Then Retest
MMM PRO FVA · 5m · Long and short · status TRADE · WR 35% · avg RR +0.11 (+0.09 → +0.27) · PF 1.29 · t 2.68 · 816 trades

- **Chart:** MMM PRO FVA on the 5m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the M15 UPG gap for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 5m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level. After the break candle, an NBC prints before price comes back to the box.
- **Retest:** Price comes back and touches the box.
- **Entry:** The 1st BC that closes out of the box: enter at the next open.
- **Stop:** Fixed 50 pts (ES 20).
- **Target:** 1:3 RR.
- **Re-enter:** Stopped out and the box still holds? Wait for touch → BC out again and re-enter once.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.

### FVA.M22 · 1m Safe Retest
MMM PRO FVA · 1m · Long and short · status WATCH · WR 14% · avg RR +0.09 (+0.09 → +0.05) · PF 1.91 · t 2.97 · 526 trades

- **Chart:** MMM PRO FVA on the 1m chart, with the HTF boxes / levels on (H1 or M15 → your chart). Read only CLOSED candles.
- **HTF level:** Price touches the MMM PRO FVA M15 internal box for the first time.
- **Wait for:** The first MMM PRO FVA reversal box in your direction prints on 1m: for longs a BuBC that closes above the last bearish candles, with the box low at or inside the level. Before the retest you see a 2nd BC, an NBC and an opposite BC.
- **Retest:** Price comes back and a candle closes inside the box.
- **Entry:** The 1st BC that closes out of the box: enter at the next open.
- **Stop:** Fixed 50 pts (ES 20).
- **Target:** 1:3 RR.
- **Trail:** After 2 BCs in profit, move the stop to entry.
- **Time out:** At the next session open (18:00 · 02:00 · 08:00 · 09:30 New York): losing → out at the open, winning → trail under each BC. Out at the 2nd session open.
