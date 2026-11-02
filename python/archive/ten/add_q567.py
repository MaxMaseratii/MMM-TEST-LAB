import json,re
S5=json.load(open('q5sum.json')); S6=json.load(open('q6sum.json')); S7=json.load(open('q7.json'))
def c(a,b): 
    f=lambda x:'-' if x is None or (isinstance(x,float) and x!=x) else (('%g'%x))
    return f'{f(a)} / {f(b)}'
L=[]
L.append('## 5. Open UPG gaps on the OTHER side of the target (10:00 to 11:30)\n')
L.append('Question: when the 10:00 candle leans one way, is there still an open (never touched) UPG gap on the other side, and does price go to that gap before the target?\n')
L.append('- **Gap** = a 3-candle UPG gap (5m, or the same timeframe as the candle) made since 18:00 and not touched before 10:00, fully on the other side of the 10:00 close (below price for a bull lean, above for a bear lean). The closest one counts.')
L.append('- **Target (TGT)** = the 10:00 candle lean-side extreme. Everything is checked on 1m bars from 10:00 to 11:30.')
L.append('- Almost all of these gaps point the SAME way as the lean (a bull gap below price on a bull-lean day): an open gap on the wrong side is rare.\n')
L.append('**What we found:**')
L.append('- **Yes, there is usually one.** An open gap sits on the other side 56-78% (2022-25) of days. It is about 36-46 pts away in 2022-25 and about 83 pts in 2026 (bigger moves).')
L.append('- **It does NOT stop the target.** The target gets hit by 11:30 just as often with the gap as without it.')
L.append('- **Strong candles ignore it.** After a BC+ or C2 candle, price goes to the gap BEFORE the target only 5% (5m), 12% (15m), 22% (1h), 19% (4h) of the time in 2022-25.')
L.append('- **Weak candles go to the gap first much more often.** After BC-, AFs, CI or S&D: gap first 15% (5m), 32% (15m), 45% (1h), 52% (4h). On 1h and 4h, a weak 10:00 candle is about a coin flip between the gap and the target. The gap is a good place to wait for those days.')
L.append('- **After price reaches the gap first, the target still comes by 11:30 only 31-58% of the time.** Do not count on both.\n')
L.append('| TF | type | n | gap there % | TGT by 11:30 with gap % | TGT by 11:30 no gap % | gap BEFORE TGT % | TGT after the gap % | gap distance pts |')
L.append('|---|---|---|---|---|---|---|---|---|')
for tf in ('5m','15m','1h','4h'):
    for nm in ('ALL','BC+/C2','other'):
        a=S5[f'{tf}|old|{nm}']; b=S5[f'{tf}|fresh|{nm}']
        L.append(f"| {tf} | {nm} | {int(a['n'])} / {int(b['n'])} | {c(a['has'],b['has'])} | {c(a['tgt_with'],b['tgt_with'])} | {c(a['tgt_without'],b['tgt_without'])} | {c(a['gap_first'],b['gap_first'])} | {c(a['tgt_after_gap'],b['tgt_after_gap'])} | {c(a['dist'],b['dist'])} |")
L.append('\n"other" = BC-, AFs, CI and S&D. 2026 rows have few cases (gap-first counts of 1-15): treat them as a guess.\n')
L.append('## 6. From the first BC after 10:00 until the opposite candle or 11:30\n')
L.append('Start = the first body close (bull or bear) of that timeframe at or after 10:00. We follow it until an **opposite candle** or 11:30 (your stop time). Three ways to call the opposite candle:')
L.append('- **opp BC** = the first body close the other way.')
L.append('- **close past BC open** = a close below the open of the LAST bull BC (bear run: above the open of the last bear BC).')
L.append('- **close past BC low** = a close below the low of the LAST bull BC (bear run: above its high).\n')
L.append('Counts: **same BCs** = body closes our way, the first one included. **NBCs** = no-body-close candles before the end. **MFE** = the most points in our favour from the start close. **End pts** = points at the opposite candle close (or 11:30). **Alive** = no opposite candle before 11:30.\n')
L.append('**What we found:**')
L.append('- **The run is short on every timeframe: median 2 same-side BCs** (the first one counts). 1m runs end in about 5-6 minutes, 5m in 25-35 minutes, 15m in about 60-75 minutes.')
L.append('- **NBCs: about 3 on 5m and 1m, about 2 on 15m** before the opposite candle. A run is BC, NBC, NBC, BC, NBC… then the other side closes.')
L.append('- **Points our way (MFE): 5m median 30-36 pts (75th pct 61-74), 15m median 36 pts (75th pct 67-70) in 2022-25. In 2026: 5m 36-46, 15m 56 pts.** 1m only 13-15 pts.')
L.append('- **But waiting for the opposite candle gives it all back.** End pts median is NEGATIVE (5m about -8 to -10, 15m -2 to -5 in 2022-25) and the average is about 0. The move is there; the exit on the opposite candle is too late. Take points, not the full run.')
L.append('- **Which opposite rule?** "Close past BC LOW" holds longest (5m: 35 min, 11% still alive at 11:30; 15m: 62% alive) and gives the most MFE. "Close past BC open" and "opp BC" end about the same time.')
L.append('- **The 4H lean does not help the run.** With or against the 4H 06-10 lean, the numbers are almost the same.')
L.append('- **How often the run gives X points (5m, close past BC low, 2022-25 / 2026):** 10 pts 81 / 85%, 20 pts 68 / 80%, 30 pts 56 / 67%, 50 pts 38 / 48%, 80 pts 22 / 36%. 15m: 20 pts 70 / 87%, 30 pts 59 / 73%, 50 pts 36 / 57%.\n')
for tf in ('1m','5m','15m'):
    L.append(f'### 6.{["1m","5m","15m"].index(tf)+1} {tf}\n')
    L.append('| opposite rule | group | n | same BCs median / avg | NBCs avg | MFE median pts | MFE 75th pct | end pts avg | end pts > 0 % | alive at 11:30 % | minutes median |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|')
    for mode in ('opp BC','close past BC open','close past BC low'):
        for g in ('all','with 4H lean','against 4H lean','with 4H BC+/C2'):
            a=S6[f'{tf}|old|{mode}|{g}']; b=S6[f'{tf}|fresh|{mode}|{g}']
            star=' *' if b['n']<30 else ''
            L.append(f"| {mode} | {g}{star} | {int(a['n'])} / {int(b['n'])} | {a['same_med']:g}, {a['same_avg']:g} / {b['same_med']:g}, {b['same_avg']:g} | {c(a['nbc_avg'],b['nbc_avg'])} | {c(a['mfe_med'],b['mfe_med'])} | {c(a['mfe75'],b['mfe75'])} | {c(a['end_avg'],b['end_avg'])} | {c(a['end_win'],b['end_win'])} | {c(a['alive'],b['alive'])} | {c(a['mins'],b['mins'])} |")
    L.append('')
L.append('## 7. Fixed 50 pt stop at 1:2 on that first BC (your check)\n')
L.append('Entry at the close of the first 5m / 15m BC at or after 10:00, in its direction. Stop 50 pts, target 100 pts, out at 11:30 if neither. 1 pt cost.\n')
L.append('| TF | group | n | WR = win rate % | avg RR | PF = profit factor | t-score |')
L.append('|---|---|---|---|---|---|---|')
for tf in ('5m','15m'):
    for g in ('all','with 4H lean','against 4H lean','first BC is BC+','with 4H BC+/C2'):
        a=S7.get(f'{tf}|old|{g}'); b=S7.get(f'{tf}|fresh|{g}')
        if not a or not b: continue
        L.append(f"| {tf} | {g} | {a['n']} / {b['n']} | {c(a['WR'],b['WR'])} | {c(a['avgRR'],b['avgRR'])} | {c(a['PF'],b['PF'])} | {c(a['t'],b['t'])} |")
L.append('\n- **No edge.** Best 2022-25 row: 5m first BC is BC+ at +0.09 avg RR, t 1.55 (under 2 = could be luck), and it is negative in 2026. The first BC after 10:00 alone is not a trade. Use it as the start of the count, not as an entry.\n')
body='\n'.join(L)+'\n'
# summary
SUM='''## Best per timeframe (summary of all 7 parts)

**One line:** at 10:00, trust a **BC+ / C2** candle for the next candle's target, ignore a weak candle's direction, expect short runs (2 BCs) and take points before the opposite candle, latest 11:30.

**4H (06:00-10:00 candle)**
- BC+ / C2: next 4H candle takes the target first about 87-90% (2022-25), 75-78% (2026).
- Weak 4H candle (BC-, AFs, CI, S&D): price goes to the open gap on the other side BEFORE the target 52% of the time. Wait at that gap.
- Does not tell you the 16:00 close. Pullback when right: median 34 / 65 pts, mostly before 10:30.

**1h (09:00-10:00 candle)**
- BC+ / C2: target first about 86-91% (2022-25), 91-100% (2026, small n).
- Weak 1h candle: gap on the other side first 45%. Coin flip between gap and target.

**15m (09:45-10:00 candle)** — the best balance
- BC+ / C2: target first about 89-92% / 78-94%.
- Strong candle: the gap on the other side comes first only 12%.
- Run after 10:00: median 2 same-side BCs, about 2 NBCs, MFE median 36 pts (2026: 56). About half the runs are still alive at 11:30.
- Take 20-30 pts: reached 70 / 87% (20 pts) and 59 / 73% (30 pts) before the opposite candle.

**5m (09:55-10:00 candle)** — the fastest
- BC+ / C2: target first about 86-89% / 71-93%. The gap on the other side first only 5%.
- 5m UPG gaps made 09:30-10:00: touched 83 / 73%, react 63 / 68% (68 / 79% with the 4H lean).
- Run after 10:00: median 2 BCs, about 3 NBCs, MFE median 30-36 pts (2026: 36-46), ends in 25-35 minutes. Take 20 pts: reached 68 / 80%.

**What does NOT work:** BC- candles for direction (coin flip), the 10:00 lean for the 16:00 close, holding until the opposite candle (gives the points back), and the first BC after 10:00 as an entry with a 50 pt stop at 1:2 (no edge).

**Important:** sections 5-7 describe what price does, they are not tested strategies. MFE and "X pts reached" have no random baseline, and 2026 has only 61 days.

'''
R=open('REPORT.md').read()
R=re.sub(r'\n## 5\. Open UPG.*?(?=\n## Files)','\n',R,flags=re.S)
R=R.replace('\n## Files', '\n'+body+'## Files',1)
R=re.sub(r'## Best per timeframe.*?(?=## 1\. Candles)','',R,flags=re.S)
R=R.replace('## 1. Candles that close at 10:00 NY', SUM+'## 1. Candles that close at 10:00 NY',1)
R=R.replace('`q1.py` `q2.py` `q3.py` `q4.py` (one per question)','`q1.py` `q2.py` `q3.py` `q4.py` (one per question), `q56.py` + `q5sum.py` + `q6sum.py` (parts 5-6), `q7.py` (part 7)')
R=R.replace('# 10:00 NY Study: MMCB candles, opening gaps, 10-14 pullback, BC runs','# 10:00 NY Study: MMCB candles, opening gaps, 10-14 pullback, BC runs, other-side gaps, runs to 11:30')
open('REPORT.md','w').write(R); print(len(R))
