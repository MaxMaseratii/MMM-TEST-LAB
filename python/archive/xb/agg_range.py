import pandas as pd, numpy as np, json
X = pd.read_parquet('xbrange.parquet')
TG = ['balanced middle', 'balanced far side', 'far zone middle', 'XB far edge']
rows = []; trades = []
for (per, tf, side, ent), g in X.groupby(['period', 'tf', 'side', 'entry']):
    for j, tn in enumerate(TG):
        gg = g[g[f'tg{j}'].notna()]
        if len(gg) == 0: continue
        hit = gg[f'hit{j}'] >= 0
        dist = (gg[f'tg{j}'] - gg.ep).abs()
        maeT = gg[f'mae{j}']
        maeH = maeT[hit]
        # stops
        hs_first = hit & ~((gg.hs >= 0) & (gg.hs <= gg[f'hit{j}']))
        s50_first = hit & ~((gg.s50 >= 0) & (gg.s50 <= gg[f'hit{j}']))
        risk_edge = (gg.edge - gg.ep).abs() + 0.5
        sd = np.where(gg.side == 'SELL', -1, 1)
        vio_pts = sd * (gg.vclose - gg.ep)
        pa = np.where(hit, dist, vio_pts) - 1.0                         # exit: target or violation close
        pb = np.where(hs_first, dist, -risk_edge) - 1.0                  # hard stop past the XB edge
        pc = np.where(s50_first, dist, -50.0) - 1.0                      # 50 pt stop
        rows.append(dict(period=per, tf=tf, side=side, entry=ent, target=tn, n=len(gg), hit=hit.mean(),
                         dist=dist.median(), height=gg.height.median(),
                         mae_hit_med=maeH.median() if len(maeH) else np.nan, mae_hit_p75=maeH.quantile(.75) if len(maeH) else np.nan,
                         mae_hit_p90=maeH.quantile(.9) if len(maeH) else np.nan,
                         mae_hit_pct=(maeH / gg.height[hit]).median() if len(maeH) else np.nan,
                         mae_all_med=maeT.median(), hit_hs=hs_first.mean(), hit_s50=s50_first.mean(),
                         risk_edge=risk_edge.median()))
        for name, p in (('target or violation close', pa), ('stop 2 ticks past XB edge', pb), ('50 pt stop', pc)):
            p = np.asarray(p, float); w = p[p > 0].sum(); lo = -p[p < 0].sum()
            trades.append(dict(period=per, tf=tf, side=side, entry=ent, target=tn, exit=name, n=len(p), wr=(p > 0).mean(),
                               avg=p.mean(), pf=w / lo if lo > 0 else np.nan, t=p.mean() / p.std(ddof=1) * np.sqrt(len(p)) if len(p) > 2 and p.std() > 0 else np.nan))
O = pd.DataFrame(rows); T = pd.DataFrame(trades)
O.to_parquet('range_odds.parquet'); T.to_parquet('range_trades.parquet')
pd.set_option('display.width', 250)
for tf in ['15m', '1h', '4h', 'D']:
    print('\n#####', tf)
    q = O[(O.tf == tf)].pivot_table(index=['side', 'entry', 'target'], columns='period', values=['n', 'hit', 'mae_hit_med', 'mae_hit_p90', 'hit_hs', 'hit_s50', 'dist', 'risk_edge']).round(2)
    print(q[[('n','old'),('n','fresh'),('hit','old'),('hit','fresh'),('hit_hs','old'),('hit_hs','fresh'),('hit_s50','old'),('hit_s50','fresh'),('dist','old'),('risk_edge','old'),('mae_hit_med','old'),('mae_hit_med','fresh'),('mae_hit_p90','old')]].to_string())
