import pandas as pd, numpy as np, json
X = pd.read_parquet('xbrange.parquet')
# one name per zone for both sides (sell side names, buy side mirrored)
NM = {'XBB bottom (balanced top)': 'Zone edge (XBB bottom / XBS top)', 'XBS top (balanced bottom)': 'Zone edge (XBB bottom / XBS top)',
      'XBB middle': 'Zone middle (XBB / XBS middle)', 'XBS middle': 'Zone middle (XBB / XBS middle)',
      'XB high (far edge)': 'XB edge (XB high / XB low)', 'XB low (far edge)': 'XB edge (XB high / XB low)',
      'Balanced middle (reference)': 'Balanced middle (reference)'}
X['ent'] = X.entry.map(NM)
TG = ['balanced middle', 'balanced far side', 'far zone middle', 'XB far edge']
TGN = {'balanced middle': 'Balanced middle', 'balanced far side': 'Other side of Balanced', 'far zone middle': 'Middle of the other zone', 'XB far edge': 'Other XB edge'}
rows = []
for (per, tf, ent), g in X.groupby(['period', 'tf', 'ent']):
    sd = np.where(g.side == 'SELL', -1, 1)
    for j, tn in enumerate(TG):
        m = g[f'tg{j}'].notna().values
        if m.sum() < 5: continue
        gg = g[m]; s = sd[m]
        hit = (gg[f'hit{j}'] >= 0).values
        dist = (gg[f'tg{j}'] - gg.ep).abs().values
        mae = gg[f'mae{j}'].values; H = gg.height.values
        hs1 = hit & ~((gg.hs >= 0) & (gg.hs <= gg[f'hit{j}'])).values
        s50 = hit & ~((gg.s50 >= 0) & (gg.s50 <= gg[f'hit{j}'])).values
        risk = (gg.edge - gg.ep).abs().values + 0.5
        vio = s * (gg.vclose.values - gg.ep.values)
        res = {'Target or violation close': np.where(hit, dist, vio) - 1, 'Stop 2 ticks past the XB edge': np.where(hs1, dist, -risk) - 1, 'Stop 50 pts': np.where(s50, dist, -50.0) - 1}
        r = dict(period=per, tf=tf, entry=ent, target=TGN[tn], n=int(len(gg)), hit=hit.mean(), viol=1 - hit.mean(), hit_hs=hs1.mean(), hit_s50=s50.mean(),
                 dist=np.median(dist), risk=np.median(risk), height=np.median(H),
                 dd_med=np.median(mae[hit]) if hit.any() else np.nan, dd_p75=np.quantile(mae[hit], .75) if hit.any() else np.nan,
                 dd_p90=np.quantile(mae[hit], .9) if hit.any() else np.nan, dd_pct=np.median(mae[hit] / H[hit]) if hit.any() else np.nan,
                 vio_loss=np.median(-vio[~hit]) if (~hit).any() else np.nan)
        for k, p in res.items():
            w = p[p > 0].sum(); lo = -p[p < 0].sum()
            r[k + '|wr'] = (p > 0).mean(); r[k + '|avg'] = p.mean(); r[k + '|pf'] = w / lo if lo > 0 else np.nan
            r[k + '|t'] = p.mean() / p.std(ddof=1) * np.sqrt(len(p)) if p.std() > 0 else np.nan
        rows.append(r)
O = pd.DataFrame(rows); O.to_parquet('range_comb.parquet')
pd.set_option('display.width', 260)
for tf in ['15m', '1h', '4h', 'D']:
    q = O[O.tf == tf].pivot_table(index=['entry', 'target'], columns='period', values=['n', 'hit', 'dist', 'dd_med', 'dd_p90', 'vio_loss', 'Target or violation close|avg', 'Target or violation close|t']).round(2)
    print('\n###', tf); print(q.to_string())
