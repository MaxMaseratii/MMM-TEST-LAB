import pickle, sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/lez')
from data import rs

PERIODS = {'old': '2022-25', 'fresh': '2026'}
TFMIN = {'5m': 5, '15m': 15, '1h': 60, '4h': 240}

_R = None
def raw():
    global _R
    if _R is None:
        _R = pickle.load(open('/home/claude/lez/raw.pkl', 'rb'))
    return _R

def good_days(d1):
    """weekday calendar dates with all 30 1m bars 09:30..09:59 present"""
    t = d1.index
    m = (t.time >= pd.Timestamp('09:30').time()) & (t.time <= pd.Timestamp('09:59').time())
    s = pd.Series(1, index=t[m]).groupby(t[m].normalize()).size()
    days = s[s == 30].index
    return [x for x in days if x.weekday() < 5]

def ctype(o, h, l, c, pH, pL):
    """MMCB type exactly like the Pine code"""
    rng = h - l
    cpos = 0.5 if rng == 0 else (c - l) / rng
    if l < pL and c > pH: return 'BuC2+' if cpos >= 0.75 else 'BuC2-'
    if h > pH and c < pL: return 'BeC2+' if cpos <= 0.25 else 'BeC2-'
    if c > pH: return 'BuBC+' if cpos >= 0.75 else 'BuBC-'
    if c < pL: return 'BeBC+' if cpos <= 0.25 else 'BeBC-'
    if h > pH and l < pL: return 'S&D.BuAF' if cpos >= 0.5 else 'S&D.BeAF'
    if l < pL: return 'BuAFs+' if cpos >= 0.5 else 'BuAFs-'
    if h > pH: return 'BeAFs+' if cpos <= 0.5 else 'BeAFs-'
    return 'CI.BuAF' if cpos >= 0.5 else 'CI.BeAF'

TYPES = ['BuC2+', 'BuC2-', 'BeC2+', 'BeC2-', 'BuBC+', 'BuBC-', 'BeBC+', 'BeBC-',
         'S&D.BuAF', 'S&D.BeAF', 'BuAFs+', 'BuAFs-', 'BeAFs+', 'BeAFs-', 'CI.BuAF', 'CI.BeAF']

def lean(t):
    if t == 'BuAFs-': return 'bear'
    if t == 'BeAFs-': return 'bull'
    if t.startswith('Bu') or t.startswith('CI.Bu') or t.startswith('S&D.Bu'): return 'bull'
    return 'bear'

def family(t):
    if 'C2' in t: return 'C2'
    if 'BC+' in t: return 'BC+'
    if 'BC-' in t: return 'BC-'
    if 'AFs' in t: return 'AFs'
    if t.startswith('CI'): return 'CI'
    return 'S&D'

FAMS = ['BC+', 'BC-', 'C2', 'AFs', 'CI', 'S&D']

def bcside(h, l, c, pH, pL):
    if c > pH: return 1
    if c < pL: return -1
    return 0

def bars(key, tf):
    """resampled bars with prev high/low and type columns, cached"""
    d = rs(raw()[key], tf)
    d['pH'] = d.high.shift(1); d['pL'] = d.low.shift(1); d['plab'] = pd.Series(d.index, index=d.index).shift(1)
    d = d.dropna(subset=['pH'])
    d['type'] = [ctype(o, h, l, c, a, b) for o, h, l, c, a, b in zip(d.open, d.high, d.low, d.close, d.pH, d.pL)]
    d['bc'] = np.where(d.close > d.pH, 1, np.where(d.close < d.pL, -1, 0))
    return d

def pct(x, n):
    return None if n == 0 else round(100.0 * x / n, 1)

def med(a):
    a = [x for x in a if x is not None and not (isinstance(x, float) and np.isnan(x))]
    return None if not a else round(float(np.median(a)), 2)

def q(a, p):
    a = [x for x in a if x is not None and not (isinstance(x, float) and np.isnan(x))]
    return None if not a else round(float(np.percentile(a, p)), 2)

def mean(a):
    a = [x for x in a if x is not None and not (isinstance(x, float) and np.isnan(x))]
    return None if not a else round(float(np.mean(a)), 2)
