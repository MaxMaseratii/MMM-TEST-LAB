"""Collect every result table into sheets.json for the HTML research sheet."""
import pandas as pd, numpy as np, json, glob
OUT = '/home/claude/rt/out'
S = []

def add(name, df, note, pct=(), r2=(), keep=None):
    df = df.copy().replace([np.inf, -np.inf], np.nan)
    for c in df.columns:
        if df[c].dtype.kind == 'f':
            df[c] = df[c].round(3)
    S.append(dict(name=name, note=note, cols=list(df.columns), pct=list(pct), rows=df.replace({np.nan: None, np.inf: None, -np.inf: None}).astype(object).where(df.notna(), None).values.tolist()))

PER = {'old': 'NQ 2022-25', 'fresh': 'MNQ Jul-Oct 26', 'fresh10': 'MNQ Jan-Oct 26'}

# ── themes (median over every stop x target x exit) + the fixed 50 / 1:2 cells
th = pd.read_parquet(f'{OUT}/THEMES.parquet')
m = pd.read_parquet(f'{OUT}/ALL_merged.parquet')
T = ['tf', 'family', 'signal', 'side', 'session', 'entry']
f50 = m[(m.stop == 'S0 fixed 50') & (m.target == '1:2')]
x0 = f50[f50.exit == 'X0 none'][T + ['trades_o', 'WR_o', 'PF_o', 'avgR_o', 't_o', 'trades_f', 'WR_f', 'PF_f', 'avgR_f', 't_f']]
x0.columns = T + ['50pt 1:2 n old', 'WR old', 'PF old', 'avg RR old', 't old', 'n new', 'WR new', 'PF new', 'avg RR new', 't new']
be = f50.sort_values('avgR_o', ascending=False).groupby(T).head(1)[T + ['exit', 'avgR_o', 'WR_o', 'avgR_f', 'WR_f']]
be.columns = T + ['best exit (old) at 50pt 1:2', 'its avg RR old', 'its WR old', 'its avg RR new', 'its WR new']
th2 = th.merge(x0, on=T, how='left').merge(be, on=T, how='left')
th2 = th2.rename(columns={'cells': 'combos', 'n_o': 'median n old', 'n_f': 'median n new', 'med_o': 'median avg RR old', 'med_f': 'median avg RR new',
                          'pos_o': 'combos positive old', 'pos_f': 'combos positive new', 'minmed': 'worse of the two'})
pc = ['combos positive old', 'combos positive new', 'WR old', 'WR new', 'its WR old', 'its WR new']
for fam, nm, note in [('MMCB', 'MMCB entries', 'Every MMCB candle type x entry. "median avg RR" = the middle result over every stop x target x exit (5 x 6 x 11 = 330 combos). Then the fixed 50 pt stop at 1:2 with no early exit, and the best exit for that 50 pt 1:2 trade. old = NQ 2022-25 (1m replay) · new = MNQ Jul-Oct 2026 for 5m/10m/15m, Jan-Oct 2026 for 1h/4H/D.'),
                      ('GMC', 'GMC entries', 'GMC = 3 candles with a gap (bull: c2 closes above c1 high, c3 low stays above c1 high). Split by what candle 3 is. XU = the gap candle (c2) open.'),
                      ('Zone', 'Zone x entries', 'MMM x box breaks (CONTRACTION G1 and EXPANDER G1): flips T1 and continuations T2 / T3+. S1 stop = the new protected level (new T#).')]:
    q = th2[th2.family.str.startswith(fam)].sort_values('worse of the two', ascending=False)
    add(nm, q, note, pc)

# ── POC vs ladder (footprint period)
c = pd.read_parquet(f'{OUT}/ALL_sess.parquet')
fx = c[(c.period == 'fresh') & (c.family == 'MMCB') & c.tf.isin(['5m', '10m', '15m']) & (c.trades >= 20)]
rows = []
for ss in ['All sessions', 'Asia+NY AM']:
    y = fx[fx.session == ss]
    g = y.groupby(['tf', 'signal', 'entry']).avgR.median().unstack('entry').reset_index()
    g.insert(2, 'session', ss); rows.append(g)
poc = pd.concat(rows)
order = ['tf', 'signal', 'session', 'C', 'P 87.5', 'MP 75', 'BAL 50', 'MD 25', 'D 12.5', 'XD 0', 'O open', 'POC', 'VA near edge', 'VA far edge']
add('POC vs ladder', poc[order], 'Footprint period only (MNQ Jul 8 - Oct 16 2026). Median avg RR over every stop x target x exit for each entry. POC / VA come from your footprint export. Max-delta price is not in the export, so it could not be tested.')

# ── pullback map
pm = []
for p in ['old', 'fresh']:
    d = pd.read_parquet(f'{OUT}/P_pullback_{p}.parquet'); pm.append(d)
pm = pd.concat(pm)
pm['period'] = pm.period.map(PER)
cols = [c for c in pm.columns]
add('Pullback map', pm, 'Does the next candle take the target (bull: the high) before the protected end (bull: the low)? For the ones that DO: how deep was the pullback first, and which level was filled first (1 tick through). "fill %" = the level filled inside the window. "target after fill %" = after the fill, the target still came before the protected end. Old = 1m replay. New = 5m replay for 10m/15m/1h+ (coarser: the pullback inside the first 5m bar is not seen), 1m for 5m.',
    [c for c in pm.columns if '%' in c and 'depth' not in c] + ['target_taken', 'protected_broken_first', 'takers_no_pullback_below_close'] + [c for c in pm.columns if c.startswith('takers:')])

# ── magnifier
ms = pd.read_parquet(f'{OUT}/MAG_summary.parquet'); ms['period'] = ms.period.map(PER)
add('Magnifier', ms, 'HTF candle closes. In the next HTF candle price pulls back to a level of that candle; on the LTF we wait for a trigger and enter at its close. Target = the HTF candle extreme (TGT) or 2R / 3R. "pct_target_ge_2R" = share of trades where the HTF target was at least 2R away at entry. All MMCB types pooled.',
    ['pct_target_ge_2R', 'WR_at_HTF_target', 'WR_at_2R', 'WR_at_3R', 'WR_if_ge2_at_target'])
md = pd.read_parquet(f'{OUT}/MAG_detail.parquet')
K = ['htf', 'ltf', 'window', 'type', 'level', 'trigger', 'stop']
o = md[md.period == 'old']; f = md[md.period == 'fresh10']
mm = o.merge(f, on=K, suffixes=(' old', ' new'), how='left')
mm = mm[mm['trades old'] >= 30]
mm['worse avg RR at target'] = np.minimum(mm['avgR_at_HTF_target old'], mm['avgR_at_HTF_target new'])
mm = mm.sort_values('worse avg RR at target', ascending=False)
add('Magnifier by candle', mm, 'Same test split by HTF candle type and pullback level. old = NQ 2022-25 · new = MNQ Jan - Oct 2026 (15m LTF only).',
    [c for c in mm.columns if c.startswith('WR') or c.startswith('pct')])
fu = pd.read_parquet(f'{OUT}/MAG_funnel.parquet'); fu['period'] = fu.period.map(PER)
add('Magnifier funnel', fu, 'What happened to every HTF signal: price never reached the level, the target came first, the protected end broke first, no LTF trigger, or traded.',
    ['no touch', 'target first (missed)', 'protected broke first', 'no trigger', 'traded', 'stop too small'])

# ── exits
mx = m[(m.trades_o >= 50) & (m.trades_f >= 20)]
ex = mx.groupby(['tf', 'exit']).agg(**{'median avg RR old': ('avgR_o', 'median'), 'median avg RR new': ('avgR_f', 'median'),
                                       'median WR old': ('WR_o', 'median'), 'median WR new': ('WR_f', 'median'), 'combos': ('avgR_o', 'size')}).reset_index()
K2 = ['tf', 'family', 'signal', 'side', 'session', 'entry', 'stop', 'target']
b = mx[mx.exit == 'X0 none'][K2 + ['avgR_o', 'avgR_f', 'WR_o', 'WR_f']].rename(columns={'avgR_o': 'b_o', 'avgR_f': 'b_f', 'WR_o': 'w_o', 'WR_f': 'w_f'})
j = mx.merge(b, on=K2)
j['d_o'] = j.avgR_o - j.b_o; j['d_f'] = j.avgR_f - j.b_f; j['dw_o'] = j.WR_o - j.w_o; j['dw_f'] = j.WR_f - j.w_f
dd = j.groupby(['tf', 'exit']).agg(**{'avg RR change vs no early exit, old': ('d_o', 'median'), 'avg RR change new': ('d_f', 'median'),
                                      'WR change old': ('dw_o', 'median'), 'WR change new': ('dw_f', 'median'),
                                      'beats no-exit old': ('d_o', lambda x: (x > 0).mean()), 'beats no-exit new': ('d_f', lambda x: (x > 0).mean())}).reset_index()
ex = ex.merge(dd, on=['tf', 'exit'])
add('Exits', ex, 'Every early exit next to "X0 none" (stop and target only), on the same trades. Median over every signal x entry x stop x target. XN = N NBCs in a row after the fill. XN2A = 2 NBCs and one closes in the half against you. XN2W = 2 NBCs that all close in your half. XN2R = 2 NBCs with a rejection wick against you. XSA / XSB = MMM PRO PLUS stall EXIT (any close / body close only) or a SuperTrend 14 x 2 flip. XSF = flip only.',
    ['median WR old', 'median WR new', 'WR change old', 'WR change new', 'beats no-exit old', 'beats no-exit new'])
dt = j.groupby(['family', 'target', 'exit']).agg(**{'avg RR change old': ('d_o', 'median'), 'avg RR change new': ('d_f', 'median'),
                                                   'WR change old': ('dw_o', 'median'), 'WR change new': ('dw_f', 'median')}).reset_index()
add('Exits by target', dt, 'Same comparison split by engine and target. A close-based exit cuts the trade before far targets, so it costs more the further the target.', ['WR change old', 'WR change new'])

# ── balance composition
bl = pd.read_parquet(f'{OUT}/B_balance.parquet'); bl['period'] = bl.period.map(PER)
bb = bl.groupby(['period', 'N', 'composition']).agg(events=('cont', 'size'), **{'next BC with the run %': ('cont', 'mean'),
                                                                               'move to next BC (ATR)': ('move_atr', 'mean')}).reset_index()
bt = bl.groupby(['period', 'tf', 'N']).agg(events=('cont', 'size'), **{'next BC with the run %': ('cont', 'mean'), 'move to next BC (ATR)': ('move_atr', 'mean')}).reset_index()
bt.insert(2, 'composition', 'ALL')
add('Balance (NBC) types', pd.concat([bb.assign(tf='all'), bt]), 'Every time N NBCs in a row print after a body close run. Which BC comes next: with the run (continuation) or against it? "move to next BC" = points from the close of the Nth NBC to the close of the next BC, with the run = +, in ATR. Split by what the balance candles are.',
    ['next BC with the run %'])

# ── absorption
ab = pd.read_parquet(f'{OUT}/ABS_boxes.parquet')
ab['location of the last close'] = pd.cut(ab.last_pos, [-.01, 1 / 3, 2 / 3, 1.01], labels=['bottom third', 'middle third', 'top third']).astype(str)
feats = {'net delta of the box > 0': ab.net_delta > 0, 'last candle delta > 0': ab.last_delta > 0,
         'stacked buy imbalances > sell': ab.stack_buy > ab.stack_sell, 'delta at the top edge > 0 (buyers hit the top)': (ab.n_top > 0) & (ab.delta_top > 0),
         'delta at the bottom edge < 0 (sellers hit the bottom)': (ab.n_bot > 0) & (ab.delta_bot < 0),
         'big volume small move in the TOP half, buyers (delta > 0)': (ab.abs_top_buyers > 0) & (ab.abs_bot == 0),
         'big volume small move in the TOP half, sellers (delta < 0)': (ab.abs_top_sellers > 0) & (ab.abs_bot == 0),
         'big volume small move in the BOTTOM half, sellers (delta < 0)': (ab.abs_bot_sellers > 0) & (ab.abs_top == 0),
         'big volume small move in the BOTTOM half, buyers (delta > 0)': (ab.abs_bot_buyers > 0) & (ab.abs_top == 0),
         'expander candle bullish': ab.exp_dir > 0, 'POC of the box candles in the top half': ab.poc_side > 0}
rows = []
for box in ['CONTRACTION', 'EXPANDER']:
    for fn, fm in feats.items():
        for loc in ['ALL', 'bottom third', 'middle third', 'top third']:
            for tf in ['5m', '10m', '15m', 'all']:
                sel = (ab.box == box) & (True if tf == 'all' else ab.tf == tf) & (True if loc == 'ALL' else ab['location of the last close'] == loc)
                a = ab[sel & fm]; r = ab[sel & ~fm]
                if len(a) < 20: continue
                rows.append(dict(box=box, feature=fn, location=loc, tf=tf, boxes=len(a), **{'break UP %': a.up.mean(), 'break UP % without it': r.up.mean(),
                            'difference': a.up.mean() - r.up.mean(), 'z': (a.up.mean() - r.up.mean()) / np.sqrt(.25 / len(a) + .25 / max(len(r), 1)),
                            'break keeps going %': a.follow_through.mean()}))
add('Absorption', pd.DataFrame(rows), 'MNQ footprint Jul 8 - Oct 16 2026. Every finished MMM x box (G1 grow). Does a footprint clue inside the box say which edge breaks? "location" = where the last candle before the break closed inside the box. Read the rows inside one location: that removes the "price was already near that edge" effect. "big volume small move" = volume per point > 1.5 x its 200-candle median and volume above median.',
    ['break UP %', 'break UP % without it', 'difference', 'break keeps going %'])


# ── live box control (what an indicator sees at each close inside a live box)
lv = pd.read_parquet(f'{OUT}/LIVE_box.parquet')
lv['location now'] = pd.cut(lv.pos, [-.01, 1 / 3, 2 / 3, 1.01], labels=['bottom third', 'middle third', 'top third']).astype(str)
lv['box age'] = pd.cut(lv.k, [0, 1, 3, 6, 1000], labels=['1st inside candle', '2-3', '4-6', '7+']).astype(str)
rows = []
for (p, tf, loc, age), g in lv.groupby(['period', 'tf', 'location now', 'box age']):
    rows.append(dict(period=p, tf=tf, location=loc, age=age, closes=len(g), **{'breaks UP %': g.up.mean(), 'breaks DOWN %': 1 - g.up.mean(), 'avg position': g.pos.mean()}))
for (p, loc), g in lv.groupby(['period', 'location now']):
    rows.append(dict(period=p, tf='all', location=loc, age='all', closes=len(g), **{'breaks UP %': g.up.mean(), 'breaks DOWN %': 1 - g.up.mean(), 'avg position': g.pos.mean()}))
lf = lv[lv.cumdelta.notna()].copy()
lf['delta'] = np.where(lf.cumdelta > 0, 'box delta +', 'box delta -') + ' / ' + np.where(lf.lastdelta > 0, 'last +', 'last -')
for (loc, dd_), g in lf.groupby(['location now', 'delta']):
    rows.append(dict(period='MNQ Jul-Oct 26 (footprint)', tf='5m/10m/15m', location=loc, age=dd_, closes=len(g), **{'breaks UP %': g.up.mean(), 'breaks DOWN %': 1 - g.up.mean(), 'avg position': g.pos.mean()}))
add('Live box control', pd.DataFrame(rows), 'At EVERY candle that closes inside a live MMM x box (what an indicator sees in real time): which edge breaks first? A coin with no memory would follow the "avg position" (a close at 94% of the box would break up 94% of the time). Real boxes hold their edges much more than that: that gap is the balance. "age" = how many candles have closed inside so far. Delta rows: footprint period only.', ['breaks UP %', 'breaks DOWN %', 'avg position'])

# ── BC flow
fl = pd.read_parquet(f'{OUT}/F_bcflow.parquet'); fl['period'] = fl.period.map(PER)
fl = fl[['period', 'tf', 'candle', 'side', 'candles', 'avg_same_bcs_before_opposite_bc', 'avg_same_bcs_before_first_nbc', 'pct_no_follow_through', 'avg_best_pts', 'median_best_pts', 'avg_pts_at_opposite_bc']]
add('BC flow', fl, 'After each candle type: how many more BCs on its side print before the first opposite BC, and before the first NBC. "best pts" = the most points in its direction before the opposite BC (from its close). "pts at opposite BC" = where price stands when the opposite BC closes.', ['pct_no_follow_through'])

# ── cells that held in both periods
sv = m[(m.trades_o >= 100) & (m.avgR_o > 0) & (m.t_o >= 2.5) & (m.trades_f >= 30) & (m.avgR_f > 0)].copy()
sv['worse avg RR'] = np.minimum(sv.avgR_o, sv.avgR_f)
sv = sv.sort_values('worse avg RR', ascending=False)
sv = sv[['tf', 'family', 'signal', 'side', 'session', 'entry', 'stop', 'target', 'exit', 'trades_o', 'WR_o', 'PF_o', 'avgR_o', 't_o', 'trades_f', 'WR_f', 'PF_f', 'avgR_f', 't_f', 'worse avg RR']]
sv.columns = ['tf', 'family', 'signal', 'side', 'session', 'entry', 'stop', 'target', 'exit', 'n old', 'WR old', 'PF old', 'avg RR old', 't old', 'n new', 'WR new', 'PF new', 'avg RR new', 't new', 'worse avg RR']
add('Held both periods', sv, f'Single combos with old n >= 100, old t >= 2.5, avg RR > 0 in BOTH periods and new n >= 30. {len(sv):,} of {len(m):,} combos. Pure luck would give about 0.3% of combos = about {int(len(m) * .003):,}. So read this list as themes that repeat, not as single winners.', ['WR old', 'WR new'])

# ── baseline
b = c[(c.family == 'MMCB') & (c.entry == 'C')]
num = ['trades', '_w', '_s', '_s2', '_gw', '_gl']
bb = b.groupby(['period', 'tf', 'side', 'session', 'stop', 'target', 'exit'])[num].sum().reset_index()
bb['avgR'] = bb._s / bb.trades; bb['WR'] = bb._w / bb.trades
base = bb.groupby(['period', 'tf', 'side', 'session']).agg(**{'median avg RR (every candle at its close)': ('avgR', 'median'), 'median WR': ('WR', 'median')}).reset_index()
base['period'] = base.period.map(PER)
add('Random baseline', base, 'Every candle traded at its close in its lean direction (all MMCB types pooled) = what "no edge" looks like. A setup must beat this, not 0: longs rode a rising NQ in both periods.', ['median WR'])

json.dump(S, open(f'{OUT}/sheets.json', 'w'), separators=(',', ':'))
print([(s['name'], len(s['rows'])) for s in S])
