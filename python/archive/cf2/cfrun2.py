"""Run the extra Chart Fanatics strategies through the same grid (every entry x stop x target x exit, random twins, two periods).
python cfrun2.py <name> ...   -> trades_<name>.parquet"""
import sys, time, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/mmmlab'); sys.path.insert(0, '/home/claude/cf'); sys.path.insert(0, '/home/claude/cf2')
from mmmlab import data as D, grade
import cfstrat as CS, cfstrat2 as C2
K = CS.NQSTOP


def halves(d):
    sd = D.sday(d.index); days = np.sort(sd.unique()); cut = days[len(days) // 2]
    return np.where(sd < cut, 'P1', 'P2')


def grade_it(d, S, m, G, flips=None):
    if not len(S): return None
    S = S.astype({'i': int, 's': int, 'endb': int, 'w0': int, 'w1': int}).drop_duplicates(['i', 's']).reset_index(drop=True)
    S = S[S.endb > S.i]
    if not len(S): return None
    out = []
    parts = [(S, G)] if not flips else [(S[S.s == s], dict(G, exits=G['exits'] + [('flip', flips[s])])) for s in (1, -1)]
    for SS, GG in parts:
        if not len(SS): continue
        cols = ['i', 's', 'wk', 'tp', 'lim', 'tag'] + (['tp2'] if 'tp2' in SS.columns else [])
        out.append(grade.trades(d, SS[cols], m, end=SS.endb.values, window=(SS.w0.values, SS.w1.values), **GG))
    T = pd.concat(out, ignore_index=True)
    if flips is not None: T.loc[T.exit == 'flip', 'exit'] = 'EMA stack breaks'
    return T


def jobs(name):
    """yield (strat, m, tf, src, d, S, grid, flips)"""
    if name == 'TG':
        for m in ('NQ', 'ES', 'GC'):
            for d in D.series(m, 30):
                src = d.src.iloc[0]; S, fl = C2.tg_capital(d, m, src)
                yield 'TG Capital', m, 30, src, d, S, dict(entries=['market', ('limit', 'lim')], stops=[('col', 'wk'), 'fixed'], targets=[2, 3, 5, 10, 20, None], exits=['stop/target']), fl
    if name == 'Tori':
        for m in ('NQ', 'ES', 'GC'):
            for tf in (60, 240):
                for d in D.series(m, tf):
                    yield 'Tori Trades', m, tf, d.src.iloc[0], d, C2.tori(d, m), dict(entries=['market'], stops=[('col', 'wk'), 'fixed', ('atr', 2.0)], targets=[2, 3, 5, None], exits=['stop/target']), None
    if name == 'Jade':
        for m in ('NQ', 'ES'):
            for tf in (1, 5):
                for d in D.series(m, tf):
                    src = d.src.iloc[0]; DL = CS.extra_levels(src, m)
                    yield 'Jade Cap', m, tf, src, d, C2.jadecap(d, m, src, DL), dict(entries=['market', ('limit', 'lim')], stops=[('col', 'wk'), 'fixed'], targets=[('col', 'tp'), 2, 3], exits=['stop/target']), None
    if name == 'Kane':
        for tf in (1, 3, 5):
            dn = D.bars('MNQ', tf); de = D.bars('MES', tf)
            S, J = C2.kane(dn, de); J = J.copy(); J['per'] = halves(J); J['src'] = 'MNQ'
            yield 'Trader Kane', 'NQ', tf, 'MNQ+MES', J, S, dict(entries=['market', ('limit', 'lim')], stops=[('col', 'wk'), 'fixed', ('pts', 25.0)], targets=[('col', 'tp'), 1, 2, 4], exits=['stop/target', ('half', 1)]), None
    if name == 'Tanja':
        for m in ('NQ', 'ES'):
            for tf in (1, 5):
                for d in D.series(m, tf):
                    sd = D.sday(d.index); nfp = set(x for x in pd.DatetimeIndex(sd.unique()) if x.weekday() == 4 and x.day <= 7)
                    yield 'Tanja Trades', m, tf, d.src.iloc[0], d, C2.tanja(d, m, nfp), dict(entries=[('limit', 'lim'), 'market'], stops=[('col', 'wk'), 'fixed'], targets=[('col', 'tp'), 2, 3], exits=['stop/target']), None
    if name in EXTRA:
        yield from EXTRA[name]()


EXTRA = {}
if __name__ == '__main__':
    import cfstrat3, cfstrat4   # register more jobs into EXTRA
    cfstrat3.register(EXTRA); cfstrat4.register(EXTRA)
    for name in sys.argv[1:]:
        allT = []
        for strat, m, tf, src, d, S, G, fl in jobs(name):
            t0 = time.time(); T = grade_it(d, S, m, G, fl)
            if T is None: print(strat, m, tf, src, 'no signals', flush=True); continue
            T['strat'] = strat; T['m'] = m; T['tf'] = tf; T['src'] = src
            allT.append(T); print(f'{strat} {m} {tf}m {src}: {len(S)} signals, {len(T)} trades, {time.time()-t0:.0f}s', flush=True)
        if allT:
            A = pd.concat(allT, ignore_index=True)
            for col in ('entry', 'stop', 'target', 'exit', 'tag', 'strat', 'm', 'src', 'per'): A[col] = A[col].astype(str)
            A.to_parquet(f'trades_{name}.parquet'); print('saved', name, len(A), flush=True)
