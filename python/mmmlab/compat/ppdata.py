"""Drop-in replacement for the old pp/ppdata.py (bars_one / series / SPEC), reading the mmmlab data pack."""
from mmmlab import data as _D
import pandas as pd
END = pd.Timestamp('2026-10-28 23:59'); MK = _D.MK; SPEC = _D.SPEC


def bars_one(src, tfm):
    d = _D.bars(src, tfm) if src != 'NQ' else _D.bars(src, tfm)
    return d[d.index <= END].copy()


def series(m, tfm):
    return [d[d.index <= END] for d in _D.series(m, tfm)]
