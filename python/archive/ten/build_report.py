"""Merge q1..q4 json into results.json and write REPORT.md (both periods side by side: 2022-25 / 2026)"""
import json
A, B = '2022-25', '2026'
Q = {k: json.load(open(f'/home/claude/ten/{k}.json')) for k in ['q1', 'q2', 'q3', 'q4']}
json.dump({'notes': {'cell format in REPORT': '2022-25 / 2026', 'data': '2022-25 = NQ 1m Dec 2022-Dec 2025 (763 good days); 2026 = MNQ 1m Mar-May + Sep-Oct 2026 (61 good days)'},
           'Q1_10am_candles': Q['q1'], 'Q2_UPG_gaps': Q['q2'], 'Q3_pullback_10_14': Q['q3'], 'Q4_BC_runs': Q['q4']},
          open('/home/claude/ten/results.json', 'w'), indent=1)

def f(v):
    if v is None: return '-'
    if isinstance(v, float):
        return f'{v:.0f}' if abs(v) >= 100 else f'{v:.1f}'.rstrip('0').rstrip('.') if v != int(v) else f'{int(v)}'
    return str(v)

def table(rowsA, rowsB, cols, keycol='key', label='', small_key='n'):
    """rowsA/rowsB lists of dicts with same keys. cells 'a / b'."""
    mB = {r[keycol]: r for r in rowsB}
    head = '| ' + (label or 'group') + ' | ' + ' | '.join(c[1] for c in cols) + ' |'
    sep = '|' + '---|' * (len(cols) + 1)
    lines = [head, sep]
    for ra in rowsA:
        rb = mB.get(ra[keycol], {})
        if ra.get(small_key, 1) == 0 and rb.get(small_key, 0) == 0: continue
        k = ra[keycol] + (' *' if rb and rb.get(small_key) is not None and rb.get(small_key) < 30 else '')
        lines.append('| ' + k + ' | ' + ' | '.join(f'{f(ra.get(c[0]))} / {f(rb.get(c[0]))}' for c in cols) + ' |')
    return '\n'.join(lines)

L = []
P = L.append
P('# 10:00 NY Study: MMCB candles, opening gaps, 10-14 pullback, BC runs')
P('')
P('**How to read every table:** each cell shows **2022-25 / 2026**. Example `62 / 55` = 62% in 2022-25 and 55% in 2026.')
P('')
P('- **2022-25** = NQ 1-minute data, Dec 2022 to Dec 2025. **763 days.**')
P('- **2026** = MNQ 1-minute data, Mar-May and Sep-Oct 2026. **61 days only.** This is a SMALL SAMPLE.')
P('- A `*` after a row name = fewer than 30 cases in 2026. Treat that 2026 number as a guess, not a fact.')
P('- Weekdays only. Days with any missing 1m bar from 09:30 to 09:59 were skipped.')
P('- All times are New York. "pts" = NQ points. n = how many cases.')
P('- Checks done before running: the 4H bar labelled 06:00 = the 1m bars 06:00 to 09:59 (same open, high, low, close). The candle classifier was tested on 16 hand-made candles (one per type) and on real candles.')
P('')
P('**Words used:**')
P('- **Lean** = the side the MMCB type points to (bull or bear). BuAFs- leans bear. BeAFs- leans bull.')
P('- **BC** = body close. Bull BC = close above the previous candle high. Bear BC = close below the previous low. **NBC** = no body close.')
P('- **Family** = BC+ (strong BC), BC- (weak BC), C2 (took both sides then closed beyond one), AFs (took one side, closed back inside), CI (inside candle), S&D (took both sides, closed inside).')
P('- **Took HI first** = the next candle trades above this candle high before it trades below this candle low.')
P('')

# ---------------- Q1
P('## 1. Candles that close at 10:00 NY')
P('')
P('Candles: 4H 06:00-10:00, 1h 09:00-10:00, 15m 09:45-10:00, 5m 09:55-10:00. "Next candle" = the candle of the same timeframe that opens at 10:00. "16:00" = the 16:00 close compared to the 10:00 close.')
P('')
P('**Most important:**')
P('- **BC+ candles (strong close near the top or bottom) work.** The next candle takes the lean side high/low FIRST about 86-92% of the time, on every timeframe, in both periods. Think of it like a ball already at the door: the close sits right next to that extreme, so it gets hit first.')
P('- **BC- candles (weak close) are close to a coin flip** for which side gets taken first (lean side first only about 42-61%). A body close alone is not enough; the close position matters.')
P('- **The 10:00 lean does NOT tell you the 16:00 close.** On bear-lean days in 2022-25, NY still closed UP 52-57% of the time (the market went up a lot in those years). In 2026 it is about 50/50. Do not hold all day just because of the 10:00 candle.')
P('- **4H 06-10 candle -> 10-14 candle:** the 10-14 candle takes the lean-side extreme first 75% (bull lean) / 71% (bear lean) in 2022-25, and 76% / 68% in 2026. But it only CLOSES beyond that extreme 45% / 34% of the time (2022-25). So: the high/low gets taken, but often the candle does not hold past it.')
P('')
c1 = [('n', 'n'), ('share%', 'share %'), ('1st high%', 'took HI first %'), ('1st low%', 'took LO first %'), ('1st none%', 'took neither %'),
      ('took LEAN ext%', 'took lean side at all %'), ('next same lean%', 'next candle same lean %'),
      ('16:00 UP%', '16:00 UP %'), ('16:00 med pts', '16:00 median pts (10:00 close to 16:00 close)')]
c1f = [('n', 'n')] + [('next ' + x + '%', 'next = ' + x + ' %') for x in ['BC+', 'BC-', 'C2', 'AFs', 'CI', 'S&D']]
names = {'4h': '4H 06:00-10:00', '1h': '1h 09:00-10:00', '15m': '15m 09:45-10:00', '5m': '5m 09:55-10:00'}
for tf in ['4h', '1h', '15m', '5m']:
    a = Q['q1'][A][tf]; b = Q['q1'][B][tf]
    P(f'### 1.{["4h","1h","15m","5m"].index(tf)+1} {names[tf]}')
    P('')
    P('**By type (share + who gets taken first + 16:00 close):**')
    P('')
    P(table(a['by_type'] + a['by_lean'] + [a['all']], b['by_type'] + b['by_lean'] + [b['all']], c1, label='type'))
    P('')
    P('**By family and lean side (16:00 measured in the lean direction: + = moved the lean way):**')
    P('')
    P(table(a['by_family'], b['by_family'], [('n', 'n'), ('LEAN ext 1st%', 'took lean side FIRST %'), ('took LEAN ext%', 'took lean side at all %'),
                                               ('next same lean%', 'next candle same lean %'), ('16:00 WITH lean%', '16:00 closed lean way %'),
                                               ('16:00 med pts WITH lean', '16:00 median pts lean way')], label='family'))
    P('')
    P('**Next candle family (what type the 10:00 candle turns into next):**')
    P('')
    P(table(a['by_type'] + a['by_lean'], b['by_type'] + b['by_lean'], c1f, label='this type'))
    P('')
P('### 1.5 4H 06-10 candle -> what the 10:00-14:00 4H candle does')
P('')
P(table(Q['q1'][A]['4h_next_10_14'], Q['q1'][B]['4h_next_10_14'],
        [('n', 'n'), ('1st high%', 'took 06-10 HI first %'), ('1st low%', 'took 06-10 LO first %'), ('none%', 'took neither %'),
         ('took LEAN ext%', 'took lean side at all %'), ('close ABOVE high%', '10-14 closes ABOVE 06-10 high %'),
         ('close BELOW low%', '10-14 closes BELOW 06-10 low %'), ('close INSIDE%', 'closes inside %')], label='06-10 type'))
P('')

# ---------------- Q2
q2a, q2b = Q['q2'][A], Q['q2'][B]
P('## 2. UPG gaps made 09:30-10:00 (5m and 1m)')
P('')
P('Bull UPG = c2 is a bull BC (close above c1 high) and c3 low is above c1 high. Gap zone = c1 high to c3 low. Bear = mirror. We count gaps whose c3 candle opens 09:30 or later and closes by 10:00 (5m: c3 = 09:30 to 09:55 bar; 1m: 09:30 to 09:59 bar). Gaps can overlap (each 3-candle set counts once). We watch until 16:00.')
P('')
P('- **Touch** = price trades back into the zone. **Full fill** = price trades through the far edge (c1 high for a bull gap).')
P('- **React** = after the touch, a 5m candle closes back outside the gap on the gap side BEFORE any 5m close beyond the far edge. **Fail** = a 5m close beyond the far edge comes first.')
P('')
P('**Most important:**')
P('- **Gaps almost always get touched, and fast.** 5m gaps: 83% / 73% touched, median 5 / 3.5 minutes after the gap is made. 1m gaps: 92% / 92% touched, median 1 minute. A gap here is like a sponge: price comes back to soak it up.')
P('- **Most of them get fully filled too:** 5m 74% / 67%, 1m 88% / 87%. If a 5m gap is touched, 90% / 91% get fully filled at some point before 16:00. So "react" is often only a bounce, not a final hold.')
P('- **React beats fail: 63% / 68% (5m).** The gap side wins more when the gap points the SAME way as the 4H 06-10 lean: react 68% / 79%. Against the 4H lean: react only 47% / 29%. WARNING: the 4H candle is still open until 10:00, so this filter is only fully known at 10:00 (it peeks a little ahead for gaps made before 10:00).')
P('- **The first 5m close outside the gap tells you a lot:** a FAIL close is nearly always a real body close (5m gaps: BC+ family 68% / 76%, BC family total 87% / 81%). A REACT close is most often an AFs candle (47% / 51%), like BuAFs+ for a bull gap (sweep the low, close back up). So: strong BC through the far edge = the gap is dead. AFs back out of the gap = the gap held. (This rule is for 5m gaps. For tiny 1m gaps the fail candle is often just an AFs, 35% / 38%.)')
P('- **After a FULL fill it is close to a coin flip.** In 60 minutes, 5m gaps: price goes 30 pts the fill way 65% / 82% and 30 pts back the other way 60% / 77% (2026 moves more). Which 30 comes first: about 50/50 (5m 50% / 57% continue first, 1m 46% / 53%). Price gets back past the near edge of the gap within 60 min 82% / 88%. So a filled gap is NOT a clean breakout signal.')
P('')
P('### 2.1 Gap counts, touch, fill, react/fail')
P('')
P(table(q2a['summary'], q2b['summary'], [('n gaps', 'n gaps'), ('gaps/day', 'gaps per day'), ('med size pts', 'median gap size pts'),
                                          ('touched%', 'touched %'), ('med min to touch', 'median min to touch'), ('p75 min to touch', '75th pct min to touch'),
                                          ('touched <=5 min%', 'touched within 5 min %'), ('touched <=30 min%', 'touched within 30 min %'),
                                          ('full fill%', 'full fill %'), ('fill if touched%', 'full fill if touched %'),
                                          ('n touched', 'n touched'), ('REACT%', 'REACT % (of touched)'), ('FAIL%', 'FAIL %'), ('neither%', 'neither %')], label='gap set', small_key='n gaps'))
P('')
P('### 2.2 Gap with or against the 4H 06-10 lean')
P('')
P(table(q2a['by_4h_lean'], q2b['by_4h_lean'], [('n gaps', 'n gaps'), ('touched%', 'touched %'), ('full fill%', 'full fill %'), ('n touched', 'n touched'),
                                               ('REACT%', 'REACT %'), ('FAIL%', 'FAIL %')], label='gap vs 4H lean', small_key='n gaps'))
P('')
P('### 2.3 After a FULL fill (next 60 minutes, measured from the far edge)')
P('')
P('"Same way" = the way price filled the gap (down for a bull gap). "Reverse" = back the gap way. "Back past gap" = price trades back beyond the near edge of the gap.')
P('')
P(table(q2a['after_full_fill'], q2b['after_full_fill'], [('n fills', 'n fills'), ('cont 30 pts in 60m%', 'went 30 pts same way %'), ('cont 60 pts in 60m%', 'went 60 pts same way %'),
                                                         ('rev 30 pts in 60m%', 'went 30 pts reverse %'), ('cont30 FIRST (vs rev30)%', '30 same way FIRST (vs 30 reverse) %'),
                                                         ('rev30 FIRST%', '30 reverse FIRST %'), ('back past gap in 60m%', 'back past gap in 60 min %'),
                                                         ('back past gap by 16:00%', 'back past gap by 16:00 %'),
                                                         ('med pts same way (60m)', 'median pts same way (MFE)'), ('p75 pts same way', '75th pct same way'),
                                                         ('med pts reverse (60m)', 'median pts reverse (MAE)'), ('p75 pts reverse', '75th pct reverse')], label='gap set', small_key='n fills'))
P('')
P('### 2.4 The FIRST 5m candle that closes outside the gap after the touch')
P('')
P('Top 5 MMCB types (count, %). "close WITH gap dir" is 100% for react and 0% for fail by definition. "candle lean = close side" = the MMCB lean of that candle points the same way it closed.')
P('')
P('| set | n | top 5 types 2022-25 | top 5 types 2026 | families 2022-25 | close WITH 4H 06-10 lean % | candle lean = close side % |')
P('|---|---|---|---|---|---|---|')
for k in q2a['first_5m_close_outside']:
    ra = q2a['first_5m_close_outside'][k]; rb = q2b['first_5m_close_outside'][k]
    t5 = lambda r: ', '.join(f'{t} {p}%' for t, c, p in r['top5 types'])
    fm = ', '.join(f'{t} {p}%' for t, c, p in ra['families'])
    P(f'| {k} gaps{" *" if rb["n"] < 30 else ""} | {ra["n"]} / {rb["n"]} | {t5(ra)} | {t5(rb)} | {fm} | {f(ra["close WITH 4H lean%"])} / {f(rb["close WITH 4H lean%"])} | {f(ra["candle lean = close side%"])} / {f(rb["candle lean = close side%"])} |')
P('')
P('Families for 2026:')
P('')
for k in q2b['first_5m_close_outside']:
    rb = q2b['first_5m_close_outside'][k]
    P(f'- {k} (n={rb["n"]}): ' + ', '.join(f'{t} {p}%' for t, c, p in rb['families']))
P('')

# ---------------- Q3
P('## 3. Pullback inside the 10:00-14:00 4H candle')
P('')
P('(a) "Adverse" = the biggest move AGAINST the 06-10 4H lean, measured from the 10:00 open, anywhere from 10:00 to 13:59. (b) For the 10-14 candle itself: if it closes up, how far it went below its open (and the mirror for down candles).')
P('')
P('**Most important:**')
P('- **The 06-10 lean is a coin flip for the 10-14 close:** 51% / 49% close the lean way. The 06-10 candle alone is not a direction signal for 10-14.')
P('- **When the lean IS right, the pullback is small and EARLY:** median 34 / 65 pts against you (about 25% of the 06-10 range), 75th pct 58 / 97 pts. The worst point comes before 10:30 in 61% / 53% of these days. If price is still going against you after 10:30-11:00, the lean is probably wrong (on wrong days the worst point comes late, median 175 minutes after 10:00).')
P('- **Stop size check (your 50 pt NQ stop):** even on days the lean is RIGHT, price goes 50+ pts against the 10:00 open 31% / 57% of the time. A 50 pt stop right at the 10:00 open is too tight for 2026 volatility. Use the % of the 06-10 range (about 25% typical, 40-44% at the 75th pct) instead of fixed points, or wait for the early pullback.')
P('- **10-14 candle wicks:** an UP 10-14 candle first drops about 29 / 45 pts below its open (median), about 24% of its own range. A DOWN candle first rises about 31 / 47 pts. The opposite wick is made FIRST about 88% / 84-90% of the time.')
P('')
P('### 3.1 (a) Move against the 06-10 lean after 10:00')
P('')
P(table(Q['q3'][A]['a_adverse_vs_0610_lean'], Q['q3'][B]['a_adverse_vs_0610_lean'],
        [('n', 'n'), ('med adverse pts', 'median pts against'), ('p75 adverse pts', '75th pct pts'), ('p90 adverse pts', '90th pct pts'),
         ('med adverse % of 06-10 range', 'median % of 06-10 range'), ('p75 adverse %', '75th pct %'), ('adverse >=50 pts%', '50+ pts against %'),
         ('med 06-10 range pts', 'median 06-10 range pts'), ('med favour pts', 'median pts in favour'), ('10-14 closes WITH lean%', '10-14 closes lean way %')], label='group'))
P('')
P('**When does the worst point happen? (minutes after 10:00)**')
P('')
P(table(Q['q3'][A]['a_adverse_vs_0610_lean'], Q['q3'][B]['a_adverse_vs_0610_lean'],
        [('n', 'n'), ('med min to worst pt', 'median minutes'), ('worst by 10:30%', 'by 10:30 %'), ('worst 10:30-11%', '10:30-11 %'),
         ('worst 11-12%', '11-12 %'), ('worst 12-13%', '12-13 %'), ('worst 13-14%', '13-14 %')], label='group'))
P('')
P('### 3.2 (b) The 10-14 candle: how far it goes the wrong way first')
P('')
P('"pts against open first" = for an UP candle, the lowest point below the open BEFORE the candle high is made (mirror for DOWN). "wick" = open to the low (any time).')
P('')
P(table(Q['q3'][A]['b_1014_candle'], Q['q3'][B]['b_1014_candle'],
        [('n', 'n'), ('share%', 'share %'), ('med pts against open first', 'median pts against first'), ('p75 pts against first', '75th pct'),
         ('med wick vs open pts (any time)', 'median wick pts'), ('p75 wick pts', '75th pct wick'), ('med wick % of 10-14 range', 'median wick % of range'),
         ('p75 wick %', '75th pct wick %'), ('opposite extreme made FIRST%', 'opposite extreme made first %'), ('med 10-14 range pts', 'median 10-14 range pts')], label='group'))
P('')

# ---------------- Q4
P('## 4. BC runs around 09:30-10:00')
P('')
P('A run starts at the first BC. Every next BC on the SAME side adds 1. NBCs in between do not stop the run. Only an OPPOSITE BC ends it. "pts to run extreme" = from the first BC close to the best high (bull) or low (bear) before the opposite BC. "pts to last BC close" = from first BC close to the close of the last same-side BC. The walk can go past 16:00 if no opposite BC shows up.')
P('')
P('**Most important:**')
P('- **A run is short: median 2 BCs, average about 2.5-2.8.** About 37% of runs are just ONE BC, then the other side body-closes. This is true on 5m, 15m and 1h, both periods.')
P('- **Each new BC has about a 60% chance to get another one on the same side** (2nd BC ~60%, 2nd->3rd ~59%, 3rd->4th ~58%). It does not get safer or riskier as the run gets longer. Like flipping a coin that lands your way 6 times in 10.')
P('- **09:30-11:30 runs do NOT have more BCs than other hours** (5m: 2.54 vs 2.44 avg). But they travel MORE points: 5m median 27 / 41 pts vs 10 / 18 pts at other hours; 15m 42 / 74 vs 18 / 34. Same count, bigger candles.')
P('- **Bull runs last a bit longer than bear runs** (2022-25 5m 2.77 vs 2.74 from 09:30; 15m 3.00 vs 2.50; 1h 3.00 vs 2.40). The 10:00 candle family changes little for runs that start after 10:00 (5m avg 2.4-2.9 for every family). One useful line: on 1h, a 10:00 BC+ candle -> next run WITH its lean averages 3.0 BCs and median 88 pts (2022-25), the best family row.')
P('- WARNING on "first BC after 09:30" split by 10:00 candle: that run often INCLUDES the 10:00 candle, so the "same lean" row peeks ahead. Use the "after 10:00" tables for trading rules.')
P('')
c4 = [('n', 'n'), ('avg BC count', 'avg BCs'), ('med BC count', 'median BCs'), ('1 BC%', '1 BC %'), ('2 BC%', '2 %'), ('3 BC%', '3 %'), ('4 BC%', '4 %'), ('5+ BC%', '5+ %'),
      ('med pts to run extreme', 'median pts to extreme'), ('avg pts to run extreme', 'avg pts to extreme'), ('med pts to last BC close', 'median pts to last BC close'),
      ('avg NBCs in run', 'avg NBCs in run'), ('med run minutes', 'median run minutes')]
c4s = [('n', 'n'), ('got 2nd BC%', 'got 2nd BC %'), ('2nd->3rd%', '2nd -> 3rd %'), ('3rd->4th%', '3rd -> 4th %'), ('4th->5th%', '4th -> 5th %')]
sec = 1
for tf in ['5m', '15m', '1h']:
    a = Q['q4'][A][tf]; b = Q['q4'][B][tf]
    for k in ['first BC after 09:30', 'first BC after 10:00']:
        P(f'### 4.{sec} {tf} - run from the {k}'); sec += 1
        P('')
        P(f'Run ended before 16:00: {f(a[k + " - ends before 16:00%"])}% / {f(b[k + " - ends before 16:00%"])}%')
        P('')
        P(table(a[k], b[k], c4, label='group'))
        P('')
        P('Chance of the next same-side BC:')
        P('')
        P(table(a[k][:5], b[k][:5], c4s, label='group'))
        P('')
    P(f'### 4.{sec} {tf} - ALL runs by the hour they START (whole data, every run)'); sec += 1
    P('')
    P(table(a['all runs by start hour'], b['all runs by start hour'], c4, label='start time'))
    P('')
    P(table(a['all runs by start hour'], b['all runs by start hour'], c4s, label='start time'))
    P('')

P('## Files')
P('')
P('- `results.json` = every table (more columns than this report).')
P('- `common.py` (loader, classifier), `verify.py` (time and classifier checks), `q1.py` `q2.py` `q3.py` `q4.py` (one per question), `build_report.py` (this report).')
P('- `q1_*.csv`, `q2_*_gaps.csv`, `q3_*.csv`, `q4_*_firstBC.csv` = one row per case, if you want to check any day by hand.')
open('/home/claude/ten/REPORT.md', 'w').write('\n'.join(L) + '\n')
print('ok', len(L))
