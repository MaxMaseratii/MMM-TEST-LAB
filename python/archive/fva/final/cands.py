import sys; sys.path.insert(0, '/home/claude/fva/final')
from fva_final import *
L1 = load_all('1h'); L4 = load_all('4h')
C = [('M1 flip fail long dATR 1:4 XN2W', L1, dict(etypes={'Fail+C'}, side='long', stop='datr', rk=4, ex='XN2W')),
     ('M1b flip fail long box 1:6 XSF', L1, dict(etypes={'Fail+C'}, side='long', stop='box', rk=6, ex='XSF')),
     ('M2 Asia flip fail both box 1:1.5 X0', L1, dict(etypes={'Fail+C'}, sess={'Asia 18-02'}, stop='box', rk=1.5, ex='X0')),
     ('M2b Asia flip fail both fix50 1:1.5 XN2W', L1, dict(etypes={'Fail+C'}, sess={'Asia 18-02'}, stop='fix', rk=1.5, ex='XN2W')),
     ('M2c Asia flip fail both fix50 1:1.5 XSA', L1, dict(etypes={'Fail+C'}, sess={'Asia 18-02'}, stop='fix', rk=1.5, ex='XSA')),
     ('B1 box fail long NY dATR 1:6 XN2W', L1, dict(etypes={'FailC'}, side='long', sess={'NY 08-13:30'}, stop='datr', rk=6, ex='XN2W')),
     ('B2 box fail long all ATR1 1:6 XH', L1, dict(etypes={'FailC'}, side='long', stop='atr1', rk=6, ex='XH')),
     ('B3 4h box fail long ATR1.5 1:6 X0', L4, dict(etypes={'FailC'}, side='long', stop='atr15', rk=6, ex='X0'))]
rows = []
for nm, L, kw in C:
    df, mo_o, mo_n = run(L, **kw)
    s = stats(df, mo_o + mo_n); so = stats(df[df.period == 'old'], mo_o); sn = stats(df[df.period == 'new'], mo_n)
    s['name'] = nm; s['t 2022-25'] = so['t-score']; s['2026 trades'] = sn['Trades']; s['2026 avgRR'] = sn.get('AvgRR'); s['2026 $'] = sn.get('NetProfit$'); s['$/mo @DD1000'] = s['$/Month'] / s['MaxDD$'] * 1000
    rows.append(s)
import pandas as pd
pd.set_option('display.width', 300); pd.set_option('display.max_columns', 40)
print(pd.DataFrame(rows).set_index('name').round(2).T.to_string())
