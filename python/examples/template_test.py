"""TEMPLATE: test any new idea in about 20 lines.
Example idea: trade every Body Flip (CDS / CDL) in the flip direction.
Change the SIGNALS part only. The rest (stops, targets, exits, random twins, two periods, PASS rule) stays the same.
Run:  python examples/template_test.py"""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mmmlab import data, grade, candles, money, flip

MARKET, TF = 'NQ', 5
rows = []
for d in data.series(MARKET, TF):                      # NQ 2022-25 (P1) and MNQ 2026 (P2), run apart
    # ---- SIGNALS: one row per signal: i = bar index of the signal close, s = +1 long / -1 short, + any tags ----
    S = flip.signals(d)
    ev = (S['eK'] == 1)                                 # event 1 = flip
    sig = pd.DataFrame({'i': S['eI'][ev], 's': S['eS'][ev], 'po4': S['eWk'][ev]})
    flipbar = np.zeros(len(d), bool); flipbar[S['eI'][ev]] = True
    # ---- FOUNDATION: what happens after the signal (BCs, points) ----
    print(d.src.iloc[0], candles.foundation(d.open.values, d.high.values, d.low.values, d.close.values, sig.i.values, sig.s.values))
    # ---- TRADES: every entry x stop x target x exit ----
    T = grade.trades(d, sig, MARKET,
                     entries=['market'],
                     stops=['fixed', ('col', 'po4'), ('atr', 1.0)],     # fixed = NQ 50 / ES 20 (Max's 1:2 rule is always in)
                     targets=[1, 2, 3, None],
                     exits=['stop/target', ('flip', flipbar)])          # flip = out at the next flip's close
    rows.append(T)
T = pd.concat(rows, ignore_index=True)
G = grade.table(T, ['entry', 'stop', 'target', 'exit'])
G = grade.passes(G)                                     # PASS = t >= 2 in BOTH periods, with the random luck level beside it
pd.set_option('display.width', 250)
print(G.round(2).sort_values('t2', ascending=False).head(20).to_string())
# ---- DOLLARS: one account, $200 risk, one trade at a time, stop after 2 losses a day ----
best = T[(T.stop == 'fixed') & (T.target == '2') & (T.exit == 'stop/target')]
for p in ('P1', 'P2'):
    A = money.account(best[best.per == p], risk_usd=200, max_losses=2)
    pr = money.prop(A)
    print(p, money.monthly(A), 'prop pass', pr.count('pass'), 'of', len(pr))
