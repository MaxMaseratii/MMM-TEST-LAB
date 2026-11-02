import pandas as pd, numpy as np, glob, sys
G = '/home/claude/fva/grid'
KEY = ['tf', 'type', 'side', 'session', 'entry', 'stop', 'target', 'exit']


def met(df):
    n = df.n.astype(float)
    avg = df.s / n
    sd = np.sqrt(np.maximum((df.s2 - n * avg * avg) / np.maximum(n - 1, 1), 0))
    df = df.assign(avgR=avg, WR=df.w / n, PF=np.where(df.gl > 0, df.gw / df.gl.replace(0, np.nan), np.nan),
                   t=np.where(sd > 0, avg / sd * np.sqrt(n), np.nan))
    return df


def load():
    old = pd.concat([pd.read_parquet(f) for f in glob.glob(f'{G}/old_*.parquet')])
    new = pd.concat([pd.read_parquet(f) for f in glob.glob(f'{G}/new_*.parquet')])
    old = met(old); new = met(new)
    m = old.merge(new, on=KEY, suffixes=('_o', '_n'), how='left')
    return m


if __name__ == '__main__':
    m = load()
    m.to_parquet(f'{G}/merged.parquet')
    ok_o = (m.n_o >= 100) & (m.avgR_o > 0) & (m.t_o >= 2)
    ok_n = (m.n_n >= 30) & (m.avgR_n > 0) & (m.t_n >= 2)
    m['PASS'] = ok_o & ok_n
    m['WATCH'] = ok_o & (m.n_n >= 30) & (m.avgR_n > 0) & (m.t_n >= 1) & ~m.PASS
    elig = (m.n_o >= 100) & (m.n_n >= 30)
    pr = m[elig].groupby(['tf', 'type']).agg(cells=('PASS', 'size'), passed=('PASS', 'sum'), watch=('WATCH', 'sum'))
    pr['pass %'] = (pr.passed / pr.cells * 100).round(2)
    pd.set_option('display.width', 250); pd.set_option('display.max_rows', 400); pd.set_option('display.max_columns', 30)
    print(pr)
    cols = KEY + ['n_o', 'WR_o', 'avgR_o', 't_o', 'PF_o', 'n_n', 'WR_n', 'avgR_n', 't_n']
    p = m[m.PASS & (m.type != 'RANDOM')].copy()
    p['score'] = np.minimum(p.t_o, p.t_n * 1.5)
    print(p.sort_values('score', ascending=False)[cols].head(80).round(3).to_string(index=False))
