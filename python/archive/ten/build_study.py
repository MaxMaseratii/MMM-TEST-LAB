# -*- coding: utf-8 -*-
"""Build '9:30 AM to 11:30 AM Testing Studies': site page + standalone artifact + markdown, from one content list."""
import json, html, re
D=json.load(open('/home/claude/mmmpro-journal/backtests/ny-open/data.json'))
def g(x): return '–' if x is None else ('%g'%round(x,1))
def ab(a,b): return f'{g(a)} / {g(b)}'
def fam(tf,per,k):
    L=D['open'][per][tf]; m=[x for x in L if x['key']==k]; return m[0] if m else {}
def c10(tf,per,k): return [x for x in D['c10'][per][tf] if x['key']==k][0]
S=[]  # sections: dict(id,num,title,sub,intro,cards,table,bullets,note)
W=D['win']
S.append(dict(id='data',num='0',title='The data and the rules',sub='Read this first',bullets=[
 '<b>2022–25</b> = NQ 1-minute data, Dec 2022 to Dec 2025, <b>763 trading days</b>. This is where the numbers come from.',
 '<b>2026</b> = MNQ 1-minute data, Mar–May and Sep–Oct 2026, <b>61 days</b>. A fresh check. Small sample: treat 2026 as a guess when n is under 30.',
 'Every result is written <b>2022–25 / 2026</b>. Example: 83 / 85% = 83% in 2022–25 and 85% in 2026.',
 'All times are New York. Weekdays only. Days with a missing 1m bar between 09:30 and 09:59 were skipped.',
 'The window ends at <b>11:30</b>, the moment Max stops trading.',
 'Candles are read with <b>MMM Candle Bias</b>: each candle compared with the one before it. TGT (target) = the lean-side extreme. Protected = the other end.',
 'Parts 1 to 8 count what price does. They are <b>not</b> tested strategies. Part 9 is a real trade test with a 1 point cost.']))
S.append(dict(id='window',num='1',title='When the morning high and low are made',sub='09:30 to 11:30, by 15-minute slot',
 table=dict(h=['Slot','High made here %','Low made here %'],rows=[[t,ab(W['old']['hw'][i],W['fresh']['hw'][i]),ab(W['old']['lw'][i],W['fresh']['lw'][i])] for i,t in enumerate(['09:30–09:45','09:45–10:00','10:00–10:15','10:15–10:30','10:30–10:45','10:45–11:00','11:00–11:15','11:15–11:30'])]),
 kpis=[('Median 09:30–11:30 range',ab(W['old']['range']['med'],W['fresh']['range']['med'])+' pts'),('High or low in by 10:00',ab(W['old']['by10'],W['fresh']['by10'])+'%'),('11:30 closes above 09:30',ab(W['old']['up'],W['fresh']['up'])+'%'),('High made before the low',ab(W['old']['hf'],W['fresh']['hf'])+'%')],
 bullets=['<b>The first 15 minutes make the morning extremes.</b> About 30–33% of highs and lows, 3 to 4 times a middle slot.',
  '<b>By 10:00, one side of the morning is usually done</b> (83 / 85%). Both extremes after 10:00 is rare (17 / 15%).',
  '<b>11:15–11:30 is the second slot for the high</b> (20 / 21%): strong mornings often push into 11:30.',
  '<b>Up or down is a coin flip</b> (51 / 53% up). The open does not tell you the side by itself.']))
rows=[]
for tf in ('5m','15m'):
    for k,lab in [('BC+','BC+'),('BC-','BC−'),('C2','C2'),('S&D','S&amp;D'),('AFs','AFs')]:
        a=fam(tf,'old',k); b=fam(tf,'fresh',k)
        rows.append([f'{tf} · {lab}',ab(a.get('n'),b.get('n')),ab(a.get('share'),b.get('share')),ab(a.get('next_tgt_first'),b.get('next_tgt_first')),ab(a.get('tgt_before_prot'),b.get('tgt_before_prot')),ab(a.get('close_lean'),b.get('close_lean'))])
S.append(dict(id='open',num='2',title='The 09:30 opening candle',sub='The first 5m or 15m candle, until 11:30',
 table=dict(h=['Candle','n','Share %','Next candle TGT first %','TGT before protected %','11:30 closes its way %'],rows=rows),
 bullets=['<b>C2 is the most common opening candle</b> (about 40%): the pre-open candle is small, so the open takes both of its sides.',
  '<b>BC+ is the cleanest:</b> the next candle takes its target first 82–87%, and the target comes before the protected end 87–93%.',
  '<b>No opening candle tells you the 11:30 close</b> (about 50% in 2022–25). Use it for the first push only.']))
o,n=D['or']['old'],D['or']['fresh']
S.append(dict(id='or',num='3',title='The 30-minute opening range',sub='The 09:30–10:00 high and low',
 kpis=[('Median range',ab(o['rng_med'],n['rng_med'])+' pts'),('Closed out by 11:30',ab(o['broke'],n['broke'])+'%'),('First close out up / down',f"{g(o['first_up'])} up · {g(o['first_dn'])} down / {g(n['first_up'])} · {g(n['first_dn'])}"),('Run past the edge, median',ab(o['ext_med'],n['ext_med'])+' pts'),('Closed out of the other side too',ab(o['other_side'],n['other_side'])+'%'),('11:30 still past that edge',ab(o['end_with'],n['end_with'])+'%')],
 bullets=['<b>Price almost always leaves the range before 11:30</b> (94 / 92%), and the side is about 50/50.',
  '<b>The first close out usually holds:</b> only 14 / 11% of days close out of the other side too, and 57 / 63% end 11:30 past the first edge.',
  'Think of the range as a door: wait for the first 1m close through it, then expect about 51 / 71 pts more.']))
rows=[]
for tf,lab in (('4h','4H 06:00–10:00'),('1h','1h 09:00–10:00'),('15m','15m 09:45–10:00'),('5m','5m 09:55–10:00')):
    r=[lab]
    for k in ('BC+ bull','BC+ bear','BC- bull','BC- bear','C2 bull','C2 bear'):
        a=c10(tf,'old',k); b=c10(tf,'fresh',k); r.append(ab(a['first'],b['first'])+(' *' if b['n']<10 else ''))
    rows.append(r)
S.append(dict(id='c10',num='4',title='The candle that closes at 10:00',sub='How often the next candle takes the lean-side extreme FIRST (%)',
 table=dict(h=['Candle','BC+ bull','BC+ bear','BC− bull','BC− bear','C2 bull','C2 bear'],rows=rows),
 note='* = fewer than 10 cases in 2026.',
 bullets=['<b>BC+ works on every timeframe:</b> 86–92% in 2022–25. The close sits next to the target, like a ball already at the door.',
  '<b>BC− is a coin flip</b> (42–61%). The close position matters more than the body close.',
  '<b>The 10:00 lean does not tell you the 16:00 close</b> (about 50–60%). Trade the morning, not the day.']))
G=D['gaps']
rows=[[x['key'],ab(x['n'],y['n']),ab(x['t'],y['t']),ab(x['mt'],y['mt']),ab(x['ff'],y['ff']),ab(x['re'],y['re'])] for x,y in zip(G['old']['sum'],G['fresh']['sum']) if 'all' in x['key']]
rows+=[[x['key'].replace('06-10','06–10'),ab(x['n'],y['n']),ab(x['t'],y['t']),'',ab(x['ff'],y['ff']),ab(x['re'],y['re'])] for x,y in zip(G['old']['lean'],G['fresh']['lean'])]
S.append(dict(id='gaps',num='5',title='UPG gaps made 09:30–10:00',sub='3-candle gaps: touch, fill, react or fail',
 table=dict(h=['Gaps','n gaps','Touched %','Median minutes to touch','Full fill %','React %'],rows=rows),
 bullets=['<b>Opening gaps get touched fast:</b> 5m 83 / 73%, median 5 / 4 minutes. A gap is a sponge: price comes back to soak it up.',
  '<b>Trade the gaps that point with the 4H 06–10 candle:</b> react 68 / 79%. Against it only 47 / 29%.',
  '<b>Most gaps get fully filled</b> later (5m 74 / 67%). A react is often a bounce, not the end.']))
P=D['opp']
rows=[]
for tf in ('4h','1h','15m','5m'):
    for k,lab in (('BC+/C2','strong (BC+ / C2)'),('other','weak')):
        a=P[f'{tf}|old|{k}'];b=P[f'{tf}|fresh|{k}']
        rows.append([f'{tf.upper() if tf=="4h" else tf} · {lab}',ab(a['n'],b['n']),ab(a['has'],b['has']),ab(a['gap_first'],b['gap_first']),ab(a['tgt_with'],b['tgt_with'])])
S.append(dict(id='opp',num='6',title='An open gap on the other side of the 10:00 target',sub='Does price visit the gap behind it first? 10:00 to 11:30',
 table=dict(h=['10:00 candle','n','Open gap there %','Gap BEFORE the target %','Target by 11:30 with the gap %'],rows=rows),
 bullets=['<b>A gap is usually there</b> (56–78% of days) and it does not stop the target.',
  '<b>Strong candles ignore it:</b> the gap comes first only 5% (5m) to 22% (1h).',
  '<b>Weak candles go there first</b> 15% (5m), 32% (15m), 45% (1h), 52% (4H). On 1h and 4H, wait at the gap on those days.']))
R=D['runs']; rows=[]
for tf in ('1m','5m','15m'):
    for m,lab in (('opp BC','opposite BC'),('close past BC low','close past BC low')):
        a=R[f'{tf}|old|{m}|all'];b=R[f'{tf}|fresh|{m}|all']
        rows.append([f'{tf} · {lab}',ab(a['same_med'],b['same_med']),ab(a['nbc_avg'],b['nbc_avg']),ab(a['mfe_med'],b['mfe_med']),ab(a['end_avg'],b['end_avg']),ab(a['alive'],b['alive']),ab(a['mins'],b['mins'])])
RE=D['reach']
reach=[[f'{tf}']+[ab(RE[f'{tf}|old|close past BC low'][i],RE[f'{tf}|fresh|close past BC low'][i]) for i in range(5)] for tf in ('1m','5m','15m')]
S.append(dict(id='runs',num='7',title='From the first BC after 10:00 until the opposite candle or 11:30',sub='Body closes our way, NBCs, points, minutes',
 table=dict(h=['Chart · opposite rule','Same-side BCs (median)','NBCs (average)','MFE median pts','Points at the end (average)','Still alive at 11:30 %','Minutes (median)'],rows=rows),
 table2=dict(h=['Chart (close past BC low)','10 pts %','20 pts %','30 pts %','50 pts %','80 pts %'],rows=reach),
 note='Same-side BCs count the first BC. Opposite BC = the first body close the other way. Close past BC low = a close below the low of the last bull BC (bear: above the high of the last bear BC). The second table = how often the run gave X points our way before it ended.',
 bullets=['<b>Runs are short:</b> median 2 same-side BCs on every chart, with about 3 NBCs (5m) or 2 (15m) in between.',
  '<b>The points are there, the exit is late:</b> MFE median 30–36 pts on 5m, 36 pts on 15m, but at the opposite candle the average is about 0.',
  '<b>Take points before the other side closes:</b> on 5m, 20 pts came 68 / 80% of the time, 30 pts 56 / 67%.',
  '<b>"Close past BC low" holds the longest.</b> The 4H lean does not change the run.']))
H=D['runhours']
S.append(dict(id='hours',num='8',title='5m BC runs by the hour they start',sub='Every run in the data',
 table=dict(h=['Run starts in','n runs','BCs (average)','Only 1 BC %','Median pts to the run extreme'],rows=[[x['key'],ab(x['n'],y['n']),ab(x['avg'],y['avg']),ab(x['one'],y['one']),ab(x['pts'],y['pts'])] for x,y in zip(H['old'],H['fresh'])]),
 bullets=['<b>Same count, bigger steps:</b> 09:30–11:30 runs have the same number of BCs as other hours, but travel more points (27 / 41 pts median).']))
Q=D['q7']; rows=[]
for tf in ('5m','15m'):
    for k,lab in (('all','all'),('with 4H lean','with the 4H lean'),('first BC is BC+','first BC is a BC+')):
        a=Q[f'{tf}|old|{k}'];b=Q[f'{tf}|fresh|{k}']
        rows.append([f'{tf} · {lab}',ab(a['n'],b['n']),ab(a['WR'],b['WR']),f"{a['avgRR']:+.2f} / {b['avgRR']:+.2f}",ab(a['PF'],b['PF']),ab(a['t'],b['t'])])
S.append(dict(id='check',num='9',title='The trade test: 50 pt stop at 1:2',sub='Entry at the first BC after 10:00, target 100, out at 11:30, 1 pt cost',
 table=dict(h=['Chart · group','n','WR = win rate %','avg RR','PF = profit factor','t-score'],rows=rows),
 note='avg RR = average result in stops (1 = one 50 pt stop). PF = money won ÷ money lost. t-score of 2 or more = probably not luck.',
 bullets=['<b>No edge.</b> avg RR −0.14 to +0.09 and every t-score under 2. The first BC after 10:00 is where you start counting, not an entry.']))
S.append(dict(id='best',num='10',title='Best read per timeframe',best=[
 ('4H',['A BC+ at 10:00: target first 87–90% (75–78% in 2026).','Weak 4H candle: the gap behind it comes first 52%. Wait there.','Pullback when the lean is right: median 34 / 65 pts, mostly before 10:30.']),
 ('1h',['BC+: target first 86–91%.','Weak 1h candle: gap or target is a coin flip.']),
 ('15m',['The best balance. BC+: target first 89–92%.','Runs after 10:00: about half still alive at 11:30.','20 pts reached 70 / 87%, 30 pts 59 / 73%.']),
 ('5m',['The fastest. BC+: target first 86–89%.','Opening gaps react 68 / 79% with the 4H lean.','Runs end in 25–35 minutes. 20 pts reached 68 / 80%.'])]))
S.append(dict(id='plan',num='11',title='How to use it from 09:30 to 11:30',sub='A reading order built from these counts, not a tested strategy',steps=[
 ('Before 09:30','Note the 4H 06:00–10:00 candle forming and any open UPG gaps from the night. The 4H side is the filter for the opening gaps.'),
 ('09:30–10:00','Expect the morning high or low to be made here (about 1 day in 3 in the first 15 minutes). Read the 09:30 5m / 15m candle: a BC+ shows the first push. Mark the 09:30–10:00 range.'),
 ('09:30–10:00 gaps','A 5m gap that points WITH the 4H candle reacts 68 / 79% of the time. Against it, it fails more often than it holds.'),
 ('10:00','Read the candles that close at 10:00. BC+ → its target is likely next. BC− → no side. Weak 1h or 4H candle → price often visits the open gap behind it first.'),
 ('10:00–11:30','Count the run: about 2 BCs and 2–3 NBCs, then the other side closes. Take points (20–30 on 5m / 15m) before the opposite candle. Use "close past the BC low" as the line that ends the run.'),
 ('11:30','Stop. Most mornings already made their range, and the 10:00 lean says nothing about 16:00.')]))
S.append(dict(id='no',num='12',title='What does NOT work',bullets=[
 'The 10:00 lean to call the 16:00 close (about 50–60%).',
 'A BC− candle for direction (coin flip).',
 'Holding until the opposite candle: the run gives the points back (average about 0 at the exit).',
 'The first BC after 10:00 as an entry with a 50 pt stop at 1:2 (no edge, t-score under 2).',
 'Guessing the side of the opening range before the first close out of it (about 50/50).']))
S.append(dict(id='words',num='13',title='Words used',defs=[
 ('BC','Body close: the candle closes past the previous candle’s high (bull) or low (bear). Urgency.'),
 ('NBC','No body close: the candle closes inside the previous candle. Negotiation.'),
 ('BC+ / BC−','A BC that closes in its strong quarter (+) or not (−).'),
 ('C2','The candle takes the other side first, then closes through: an engulf.'),
 ('AFs / CI / S&amp;D','Sweep and close back inside / inside candle / takes both sides and closes inside.'),
 ('TGT / protected','TGT = the lean-side extreme of the candle. Protected = the other end.'),
 ('UPG gap','A 3-candle gap: candle 3 never comes back to candle 1’s high (bull).'),
 ('MFE','The most points in our favour before the end.'),
 ('Opening range','The high and low of 09:30–10:00.')]))
json.dump(S,open('/home/claude/ten/study_sections.json','w'),ensure_ascii=False)
print(len(S))
