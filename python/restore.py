"""RESTORE: bring back every old test exactly as it was, so the archived scripts run again.

python restore.py                 -> restores into /home/claude (the folder every old script points at)
python restore.py --root /path    -> restores somewhere else and rewrites the old /home/claude/ paths to that folder
python restore.py --force         -> overwrite files that already exist

What it does:
 1. copies archive/<folder> back to <root>/<folder> (allm, pp, bf, xb, fva, lez, ten, rt, ...)
 2. unpacks data/raw_csv.tar.xz -> <root>/rt/lib/data (NQ / MNQ / MES 1m CSVs, MNQ footprint) and <root>/data5 (5m / 15m / 1h / 1d)
 3. rebuilds the cached data files the old scripts load: lez/raw.pkl, xb/raw2.pkl
 4. checks the rebuilt NQ / MNQ 1m bars match the data pack"""
import os, sys, shutil, tarfile, pickle, glob
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OLDROOT = '/home/claude'


def ld(folder):
    fs = sorted(glob.glob(os.path.join(folder, '*.csv')))
    if not fs: return None
    d = pd.concat([pd.read_csv(f) for f in fs]); d.index = pd.to_datetime(d.pop('time'))
    d = d[~d.index.duplicated(keep='last')].sort_index()
    return d[['open', 'high', 'low', 'close', 'volume']].astype(float)


def main():
    a = sys.argv[1:]
    root = a[a.index('--root') + 1] if '--root' in a else OLDROOT
    force = '--force' in a
    root = os.path.abspath(root); os.makedirs(root, exist_ok=True)
    # 1. code
    n = 0
    for src in glob.glob(os.path.join(HERE, 'archive', '**', '*'), recursive=True):
        if os.path.isdir(src) or src.endswith('INDEX.md'): continue
        rel = os.path.relpath(src, os.path.join(HERE, 'archive')); dst = os.path.join(root, rel)
        if os.path.exists(dst) and not force: continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if root != OLDROOT and src.endswith(('.py', '.sh')):
            open(dst, 'w').write(open(src).read().replace(OLDROOT + '/', root + '/'))
        else: shutil.copy2(src, dst)
        n += 1
    print('code files restored:', n)
    # 2. data
    with tarfile.open(os.path.join(HERE, 'data', 'raw_csv.tar.xz')) as t:
        t.extractall(root, filter='data')
    print('raw data unpacked into', os.path.join(root, 'rt/lib/data'), 'and', os.path.join(root, 'data5'))
    # 3. caches the old scripts load
    old = ld(os.path.join(root, 'rt/lib/data/NQ/1m')); old = old[old.index < '2026-01-01']
    fresh1 = ld(os.path.join(root, 'rt/lib/data/MNQ/1m'))
    os.makedirs(os.path.join(root, 'lez'), exist_ok=True); os.makedirs(os.path.join(root, 'xb'), exist_ok=True)
    pickle.dump({'old': old, 'fresh': fresh1}, open(os.path.join(root, 'lez/raw.pkl'), 'wb'))
    sday = lambda ix: (ix + pd.Timedelta(hours=6)).normalize()
    m5 = ld(os.path.join(root, 'data5/MNQ/5m')); m15 = ld(os.path.join(root, 'data5/MNQ/15m'))
    d1 = set(sday(fresh1.index)); d5 = set(sday(m5.index))
    p5 = m5[~sday(m5.index).isin(d1)]; p15 = m15[~sday(m15.index).isin(d1 | d5)]
    f_all = pd.concat([fresh1, p5, p15]).sort_index(); f_all = f_all[~f_all.index.duplicated(keep='first')]
    f_5 = pd.concat([fresh1, p5]).sort_index(); f_5 = f_5[~f_5.index.duplicated(keep='first')]
    pickle.dump({'old': old, 'fresh': f_all, 'fresh5': f_5}, open(os.path.join(root, 'xb/raw2.pkl'), 'wb'))
    print('rebuilt lez/raw.pkl and xb/raw2.pkl')
    # 4. check against the data pack
    pk = pd.read_parquet(os.path.join(HERE, 'data/fine/NQ.parquet'))
    ok = len(pk) == len(old) and np.allclose(pk.close.values, old.close.values)
    pm = pd.read_parquet(os.path.join(HERE, 'data/fine/MNQ.parquet')); pm1 = pm[pm.res == 1]
    ok2 = len(pm1) == len(fresh1) and np.allclose(pm1.close.values, fresh1.close.values)
    print('NQ 1m matches data pack:', ok, '| MNQ 1m matches:', ok2)
    print('Done. Old scripts now run from', root, '(e.g. cd', os.path.join(root, 'bf'), '&& python3 lvtest.py)')


if __name__ == '__main__':
    main()
