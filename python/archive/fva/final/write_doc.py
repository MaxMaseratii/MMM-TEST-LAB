import pandas as pd, numpy as np
T = pd.read_pickle('tables.pkl')
EXN = {'XH': 'hold to next session open', 'X0': 'stop / target only (100 candles)', 'XN2W': '2-NBC stall exit', 'XSA': 'Pro Plus stall exit'}
STN = {'atr1': 'ATR(14) × 1', 'fix': 'fixed 50', 'box': 'zone stop'}
def m(v): return ('−$' if v < 0 else '$') + f"{abs(v):,.0f}"
def tab(df):
    h = '| Stop | Exit | Target | Trades | Trades/Month | WR | Avg win $ | Avg loss $ | avg RR | PF | t-score | Net profit $ | $/Month | Max wins in a row | Max losses in a row | Max DD $ | Net/DD | Months up | 2026 trades | 2026 $ |\n|' + '---|' * 20 + '\n'
    for _, r in df.iterrows():
        h += f"| {STN[r.Stop]} | {EXN[r.Exit]} | {r.Target} | {r.Trades} | {r['Trades/Month']:.1f} | {r.WR*100:.0f}% | {m(r['AvgWin$'])} | {m(r['AvgLoss$'])} | {r.AvgRR:+.2f} | {r.PF:.2f} | {r['t-score']:.2f} | {m(r['NetProfit$'])} | {m(r['$/Month'])} | {r.MaxConsWins} | {r.MaxConsLoss} | {m(-r['MaxDD$'])} | {r['Net/DD']:.1f} | {r.MonthsUp*100:.0f}% | {r['2026 trades']} | {m(r['2026 $'])} |\n"
    return h
def steps(df):
    h = '| Step | Trades | Trades/Month | WR | avg RR | PF | t-score | Net profit $ | Max DD $ | Net/DD | 2026 trades | 2026 $ |\n|' + '---|' * 12 + '\n'
    for _, r in df.iterrows():
        h += f"| {r.Step} | {r.Trades} | {r['Trades/Month']:.1f} | {r.WR*100:.0f}% | {r.AvgRR:+.2f} | {r.PF:.2f} | {r['t-score']:.2f} | {m(r['NetProfit$'])} | {m(-r['MaxDD$'])} | {r['Net/DD']:.1f} | {r['2026 trades']} | {m(r['2026 $'])} |\n"
    return h
A, B, S, F, RB = T['A'], T['B'], T['steps'], T['final'], T['random']
fa, fb = F[F.Setup == 'A'].iloc[0], F[F.Setup == 'B'].iloc[0]
ra, rb = RB[RB.Setup == 'A'].iloc[0], RB[RB.Setup == 'B'].iloc[0]
doc = f"""MMM Fair Value Area Break — the 2 best edges, rules and honest results (Oct 25 2026)

Data: NQ 1-min Dec 2022 – Dec 2025 (35.5 months) + MNQ 2026 (5.3 months of real 1-min / 5-min data: Mar–Apr and Jul–Oct). 40.8 months in all.
Rules of the test: 1h chart · signal on a CLOSED 1h candle · market order at that close · stop and target read on 1-min candles, the stop wins when both are in the same minute · 1 pt cost on every trade · 1 MNQ ($2 a point) · one trade at a time · 100-candle time limit.

FINAL RULES — summary (honest fills)
- 1h chart only. The 15m and 5m charts did not pass any test.
- The only edge in this indicator is a box FAILING. When a 1h candle CLOSES through a box, trade WITH the break.
- Touches, retests, rejections, POC entries and the BC candles themselves did no better than random trades. They are removed.
- A · Max Profit: FVA Box Fail · LONG. Stop ATR(14) × 1. Exit at the next session open (target 1:6, rarely reached).
  {fa.Trades} trades ({fa['Trades/Month']:.1f} a month) · WR {fa.WR*100:.0f}% · PF {fa.PF:.2f} · avg RR {fa.AvgRR:+.2f} · t-score {fa['t-score']:.2f} · net {m(fa['NetProfit$'])} · {m(fa['$/Month'])} a month · max DD {m(-fa['MaxDD$'])}.
- B · High WR / Small Loss: Asia Flip Zone Fail · BOTH sides. Stop fixed 50 pts, target 1:1.5 (75 pts), MMM Pro Plus stall exit.
  {fb.Trades} trades ({fb['Trades/Month']:.1f} a month) · WR {fb.WR*100:.0f}% · PF {fb.PF:.2f} · avg RR {fb.AvgRR:+.2f} · t-score {fb['t-score']:.2f} · net {m(fb['NetProfit$'])} · max 4 losses in a row · max DD only {m(-fb['MaxDD$'])}.

What holds
- Failure, not touch. The old entries ① – ⑥ only looked good because of two bugs: grading on the opening candle, and dropping touch candles that closed through the box. With honest fills, 0 of about 30,000 touch combos passed.
- Asia is special for flip zones. Every flip-zone fail (both sides, all sessions): PF 1.11, t 1.38. The same trade in Asia only: PF 2.12, t 4.00.
- Box fails work LONG only. Both sides: PF 1.09, t 1.22. Long only: PF 1.33, t 3.02.
- Random check, same rules, random entry candle:
  - A: random longs made {m(ra['NetProfit$'])} (t {ra['t-score']:.2f}, avg RR {ra.AvgRR:+.2f}, max DD {m(-ra['MaxDD$'])}), from the market going up. Per trade, random longs made {ra.AvgRR:+.2f} avg RR and A made {fa.AvgRR:+.2f}. The market going up helps A, but most of A's result per trade is edge.
  - B: random trades lost {m(rb['NetProfit$'])}. All of B is edge.
- The 4h box fail (avg RR +0.50 in the overlap test) fails one-at-a-time: t 1.53, 2026 −0.08. Dropped.

The 2 best honest versions (1 MNQ, one trade at a time, 40.8 months)

|  | A · Max Profit | B · High WR / Small Loss |
|---|---|---|
| Setup | FVA Box Fail · LONG | Asia Flip Zone Fail · BOTH |
| Entry (market at the 1h close) | close ABOVE a live bearish FVA box | Asia 1h candle closes ABOVE a PES+ zone (buy) or BELOW a PEL+ zone (sell) |
| Filter | long only · any session | Asia only (the 1h candle opens 18:00 – 01:00 New York) |
| Stop | ATR(14) × 1 (avg {fa.AvgStop:.0f} pts) | 50 pts |
| Exit | the next session open (18:00 / 02:00 / 08:00 close) · target 1:6 | target 1:1.5 (75 pts) · Pro Plus stall exit |
| Trades (per month) | {fa.Trades} ({fa['Trades/Month']:.1f}) | {fb.Trades} ({fb['Trades/Month']:.1f}) |
| WR | {fa.WR*100:.0f}% | {fb.WR*100:.0f}% |
| Avg win / avg loss | {m(fa['AvgWin$'])} / {m(fa['AvgLoss$'])} | {m(fb['AvgWin$'])} / {m(fb['AvgLoss$'])} |
| avg RR | {fa.AvgRR:+.2f} | {fb.AvgRR:+.2f} |
| PF | {fa.PF:.2f} | {fb.PF:.2f} |
| t-score (all · 2022–25) | {fa['t-score']:.2f} · {fa['t 2022-25']:.2f} | {fb['t-score']:.2f} · {fb['t 2022-25']:.2f} |
| Net profit | {m(fa['NetProfit$'])} | {m(fb['NetProfit$'])} |
| $ / month | {m(fa['$/Month'])} | {m(fb['$/Month'])} |
| Max consecutive wins / losses | {fa.MaxConsWins} / {fa.MaxConsLoss} | {fb.MaxConsWins} / {fb.MaxConsLoss} |
| Max drawdown | {m(fa['MaxDD$'])} | {m(fb['MaxDD$'])} |
| Net ÷ max drawdown | {fa['Net/DD']:.1f} | {fb['Net/DD']:.1f} |
| Profit / month if max drawdown = $1,000 | {m(fa['$/mo @DD$1000'])} | {m(fb['$/mo @DD$1000'])} |
| Months up | {fa.MonthsUp*100:.0f}% | {fb.MonthsUp*100:.0f}% |
| Years (avg RR, trades) | {fa.years.replace(' | ', ' · ')} | {fb.years.replace(' | ', ' · ')} |
| 2026: trades · avg RR · $ | {fa['2026 trades']} · +0.16 · {m(fa['2026 $'])} | {fb['2026 trades']} · +0.56 · {m(fb['2026 $'])} |
| Random entries, same rules | {m(ra['NetProfit$'])} (t {ra['t-score']:.2f}) | {m(rb['NetProfit$'])} (t {rb['t-score']:.2f}) |

B by side: longs {83} trades, WR 57%, avg RR +0.27 · shorts 64 trades, WR 53%, avg RR +0.44.

Honest verdict
- B is the stronger edge: t-score 4.00, every year positive, the best profit at the same drawdown ({m(fb['$/mo @DD$1000'])} a month at a $1,000 max drawdown), and random trades lose. But it trades only about 3.6 times a month.
- A makes the most money ({m(fa['$/Month'])} a month on 1 MNQ) because it trades about 28 times a month. But avg RR is only +0.14, and random longs alone made +0.03 per trade in this rising market. If NQ trends down for a year, expect A to make much less, or lose.
- Both were picked from about 30,000 tested combos. Treat them as LEADS. Paper-trade first.
- vs the other MMM edges: the Level Retest (R1) makes $242 a month at a $1,000 max drawdown and EDGE PRO with protections $252. FVA B: {m(fb['$/mo @DD$1000'])}. FVA A: {m(fa['$/mo @DD$1000'])}.

Every target, every exit — A · FVA Box Fail · LONG (1 MNQ, one trade at a time, 40.8 months)

ATR(14) × 1 stop:

{tab(A[A.Stop == 'atr1'])}
Fixed 50 pt stop:

{tab(A[A.Stop == 'fix'])}
Every target, every exit — B · Asia Flip Zone Fail · BOTH

Fixed 50 pt stop:

{tab(B[B.Stop == 'fix'])}
Zone stop (the far side of the broken zone ± 4 ticks):

{tab(B[B.Stop == 'box'])}
How each rule changes the results (final stop / target / exit)

{steps(S)}
THE 2 SETUPS TO TRADE

Words used
- BC = body close: a candle that closes above the previous high (BuX) or below the previous low (BeX). NBC = neither (a neutral candle).
- FVA box = the bodies of the NBC candles before a BC. A bearish FVA box is one that a BeX broke DOWN.
- Flip zone = the body of the last opposite BC before a flip. PES+ = the last bullish BC body before sellers flipped the trend. PEL+ = the last bearish BC body before buyers flipped it.
- A box or zone is LIVE until a 1h candle closes through it. A nested box (an NBC closed inside it) must first close below it before a close above counts.

A · FVA Box Fail · LONG (Max Profit)
1. Chart: 1h. Any session.
2. Setup: a live bearish FVA box (BeFVA).
3. Trigger: a 1h candle CLOSES ABOVE the top of that box.
4. Entry: buy at that close. One trade at a time, one per candle.
5. Stop: ATR(14) × 1 of the 1h chart, below the entry (about 60 pts).
6. Target: 6 × the stop. It is rarely reached (26 of {fa.Trades} trades).
7. Exit: at the close of the 1h candle that ends at the next session open: 18:00, 02:00 or 08:00 New York. 09:30 is never a 1h close, so the 08:00 close is the one before New York.
8. Time limit: 100 candles.
- How trades ended: 591 at the session open, 520 at the stop, 26 at the target.

B · Asia Flip Zone Fail · BOTH (High WR / Small Loss)
1. Chart: 1h. Only the 1h candles that OPEN 18:00, 19:00 … 01:00 New York (Asia).
2. Setup: a live flip zone (PES+ or PEL+).
3. Trigger: an Asia 1h candle CLOSES ABOVE a PES+ zone → BUY. Or it CLOSES BELOW a PEL+ zone → SELL.
4. Entry: at that close. One trade at a time, one per candle.
5. Stop: 50 pts (MNQ / NQ). ES / MES: 20 pts (not tested).
6. Target: 75 pts (1:1.5).
7. Pro Plus stall exit (the MMM PRO PLUS EXIT label), checked from the next candle:
   - SuperTrend 14 × 2 on the 1h chart.
   - Long: each time the SuperTrend line steps UP or flips up, that candle's body bottom is the stall line and its high is the push level.
   - A later close above the push level clears it.
   - A close below the stall line first → EXIT at that close.
   - A SuperTrend flip down → EXIT at that close.
   - Short: the mirror (body top, low).
8. Time limit: 100 candles.
- How trades ended: 60 at the target, 54 at the stall exit, 33 at the stop.

Results (1 MNQ, one trade at a time, 40.8 months, 1 pt cost)

|  | A · Max Profit | B · High WR / Small Loss |
|---|---|---|
| Trades (per month) | {fa.Trades} ({fa['Trades/Month']:.1f}) | {fb.Trades} ({fb['Trades/Month']:.1f}) |
| WR | {fa.WR*100:.0f}% | {fb.WR*100:.0f}% |
| Avg win / avg loss | {m(fa['AvgWin$'])} / {m(fa['AvgLoss$'])} | {m(fb['AvgWin$'])} / {m(fb['AvgLoss$'])} |
| avg RR | {fa.AvgRR:+.2f} | {fb.AvgRR:+.2f} |
| PF | {fa.PF:.2f} | {fb.PF:.2f} |
| t-score | {fa['t-score']:.2f} | {fb['t-score']:.2f} |
| Net profit | {m(fa['NetProfit$'])} | {m(fb['NetProfit$'])} |
| $ / month | {m(fa['$/Month'])} | {m(fb['$/Month'])} |
| Max wins / losses in a row | {fa.MaxConsWins} / {fa.MaxConsLoss} | {fb.MaxConsWins} / {fb.MaxConsLoss} |
| Max drawdown | {m(-fa['MaxDD$'])} | {m(-fb['MaxDD$'])} |
| Months up | {fa.MonthsUp*100:.0f}% | {fb.MonthsUp*100:.0f}% |
| 2026 (trades · $) | {fa['2026 trades']} · {m(fa['2026 $'])} | {fb['2026 trades']} · {m(fb['2026 $'])} |

Note: FVA Break 4.1 has FVA.M1 (flip zone fail long, 1:4) and FVA.M2 (Asia, zone stop, no early exit). Neither is A or B exactly: to trade A and B from the chart, the indicator needs an update.
"""
open('/home/claude/fva/MMM_FVA_Best_2_Edges.md', 'w').write(doc)
print(len(doc))
