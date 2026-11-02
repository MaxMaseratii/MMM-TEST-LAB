"""Run every coded strategy: every entry x stop x target x exit, both periods, random twins. Output cf_trades.parquet."""
import sys, time, numpy as np, pandas as pd
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', '..')); sys.path.insert(0, '/home/claude/cf')
from mmmlab import data as D, grade
import cfstrat as CS
K = CS.NQSTOP


def grid(name, m):
    k = K[m]
    if name == 'JJ Simon': return dict(entries=['market'], stops=['fixed', ('pts', 25 * k), ('pts', 37.5 * k), ('col', 'wk')], targets=[1, 1.52, 2, 3, 4, ('col', 'tp')], exits=['stop/target', ('time', 660)])
    if name == 'Candace Lau': return dict(entries=['market', ('limit', 'lim')], stops=['fixed', ('col', 'wk'), ('pts', 20 * k), ('pts', 30 * k)], targets=[2, 3, 4, ('col', 'tp')], exits=['stop/target'])
    if name == 'Dhesi': return dict(entries=['market'], stops=['fixed', ('col', 'wk'), ('pts', 40 * k)], targets=[1.5, 2, 3, ('col', 'tp'), None], exits=['stop/target', ('half', 1.5), ('half', 2)])
    if name == 'Okala': return dict(entries=['market', ('limit', 'lim')], stops=[('pts', 10 * k), ('pts', 20 * k), ('col', 'wk'), 'fixed'], targets=[1.5, 2, 3, None], exits=['stop/target', ('half', 1.5)])
    if name == 'Marci Silfrain': return dict(entries=['market'], stops=[('col', 'wk'), 'fixed', ('atr', 1.0)], targets=[('col', 'tp'), 1, 2, 3], exits=['stop/target'])
    if name == 'Fabio Valentini': return dict(entries=['market'], stops=[('col', 'wk'), 'fixed', ('pts', 20 * k)], targets=[2, 2.5, 3, 4, 5, ('col', 'tp'), None], exits=['stop/target', ('half', 2)])


PLAN = [('JJ Simon', ['NQ', 'ES'], [1]), ('Candace Lau', ['NQ', 'ES'], [1]), ('Dhesi', ['NQ', 'ES'], [1]),
        ('Okala', ['NQ'], [1, 3, 5]), ('Fabio Valentini', ['NQ', 'ES'], [1, 5]), ('Marci Silfrain', ['NQ', 'ES', 'GC'], [5, 15, 60])]
if __name__ == '__main__':
    only = sys.argv[1:]
    allT = []
    for name, mks, tfs in PLAN:
        if only and name.split()[0] not in only: continue
        for m in mks:
            for tf in tfs:
                for d in D.series(m, tf):
                    src = d.src.iloc[0]; t0 = time.time()
                    if name in ('Candace Lau', 'Dhesi', 'Fabio Valentini'):
                        DL = CS.extra_levels(src, m)
                    if name == 'JJ Simon': S = CS.jj_simon(d, m)
                    elif name == 'Candace Lau': S = CS.candace(d, m, DL)
                    elif name == 'Dhesi': S = CS.dhesi(d, m, DL, D.bars(src, 15))
                    elif name == 'Okala': S = CS.okala(d, m)
                    elif name == 'Marci Silfrain': S = CS.marci(d, m)
                    elif name == 'Fabio Valentini': S = CS.fabio(d, m, DL)
                    if not len(S): print(name, m, tf, src, 'no signals'); continue
                    S = S.astype({'i': int, 's': int, 'endb': int, 'w0': int, 'w1': int}).drop_duplicates(['i', 's']).reset_index(drop=True)
                    S = S[S.endb > S.i]
                    G = grid(name, m)
                    T = grade.trades(d, S[['i', 's', 'wk', 'tp', 'lim', 'tag']], m, end=S.endb.values, window=(S.w0.values, S.w1.values), **G)
                    T['strat'] = name; T['m'] = m; T['tf'] = tf; T['src'] = src
                    allT.append(T)
                    print(f'{name} {m} {tf}m {src}: {len(S)} signals, {len(T)} trades, {time.time()-t0:.0f}s', flush=True)
    A = pd.concat(allT, ignore_index=True)
    for col in ('entry', 'stop', 'target', 'exit', 'tag', 'strat', 'm', 'src', 'per'): A[col] = A[col].astype(str)
    A.to_parquet('cf_trades%s.parquet' % ('_' + '_'.join(only) if only else ''))
    print('saved', len(A))
