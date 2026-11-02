"""Run the PRO PLUS points test on every market x timeframe x run. Output: trades.parquet, counts.parquet."""
import sys, time, numpy as np, pandas as pd
import ppdata, engine

TFS = [1, 2, 3, 5, 10, 15, 30, 60]
RUNS = {  # name: kwargs
    'base': dict(),                                   # all hours, EXIT label or flip, fixed 50-pt-equivalent stop
    'win': dict(win_on=True, day_on=True),            # 5 windows + daily rules (3 trades, stop after 2 losses)
    'flip': dict(use_exit=False),                     # exit on SuperTrend flip only
    'fst': dict(stop_mode='flipst'),                  # stop = flip ST line, skipped if farther than the fixed stop
}


def htf_dir(src, htf, idx):
    """bias = direction of the last CLOSED htf candle before the htf candle holding each chart candle (Pine: hD[1], lookahead on)."""
    d = ppdata.bars_one(src, htf)
    a = engine.rma_atr(d.high.values, d.low.values, d.close.values)
    _, dr = engine.supertrend(d.open.values, d.high.values, d.low.values, d.close.values, a, pine_custom=False)
    dirv = np.where(dr < 0, 1, -1)
    cur = idx.floor(f'{htf}min')
    k = np.searchsorted(d.index.values, cur.values, 'left') - 1   # last htf candle that started before the current one
    out = np.where(k >= 0, dirv[np.clip(k, 0, None)], 0)
    return out


def main(markets):
    allT = []; cnt = []
    for m in markets:
        sp = ppdata.SPEC[m]
        for tf in TFS:
            for d in ppdata.series(m, tf):
                t0 = time.time()
                S = engine.signals(d)
                src = d.src.iloc[0]
                htf = 15 if tf <= 5 else 60 if tf <= 30 else None
                hd = htf_dir(src, htf, d.index) if htf else np.zeros(len(d), int)
                per = d.per.values
                for rn, kw in RUNS.items():
                    if rn == 'win' and tf > 30: continue
                    T, mi, sk = engine.trades(S, d.index, sp['stop'], sp['cost'], sp['tick'], **kw)
                    if len(T):
                        i = T.isig.values; sd = T.side.values
                        T['per'] = per[i]
                        T['t'] = d.index.values[i]
                        j = T.itag.values   # decision candle: the EXIT candle for the 50% limit (order placed there), else the signal candle
                        cl = S['c'][j]; vw = S['vw'][j]; st = S['st'][j]; vs = S['vws'][j]
                        T['vside'] = np.where((cl - vw) * sd > 0, 'with', 'against')
                        T['vcol'] = np.where(vs == sd, 'colored with', np.where(vs == 0, 'black', 'colored against'))
                        T['stack'] = ((cl - vw) * sd > 0) & ((vw - st) * sd > 0)
                        T['htf'] = np.where(hd[j] == 0, 'none', np.where(hd[j] == sd, 'with', 'against'))
                        T['m'] = m; T['tf'] = tf; T['run'] = rn
                        T['rr'] = T.pl / sp['stop']
                        T['wait'] = T.isig.values - j
                        allT.append(T.drop(columns=['isig', 'ifill', 'iexit', 'itag']))
                    for p in ('P1', 'P2'):
                        pass
                    cnt.append(dict(m=m, tf=tf, run=rn, src=src, **{f'missed{k}': int(mi[k]) for k in range(engine.NS)},
                                    **{f'skip{k}': int(sk[k]) for k in range(engine.NS)}, bars=len(d),
                                    d0=str(d.index[0]), d1=str(d.index[-1]),
                                    days=int(pd.Series((d.index + pd.Timedelta(hours=6)).normalize()).nunique())))
                print(m, tf, src, len(d), f'{time.time() - t0:.1f}s', flush=True)
    A = pd.concat(allT, ignore_index=True)
    A['setup'] = A.setup.astype(np.int8); A['side'] = A.side.astype(np.int8); A['win'] = A.win.astype(np.int8)
    tag = '_'.join(markets)
    A.to_parquet(f'trades_{tag}.parquet'); pd.DataFrame(cnt).to_parquet(f'counts_{tag}.parquet')
    print('done', len(A))


if __name__ == '__main__':
    main(sys.argv[1:])
