"""How big can payouts get with NO edge? 1,000 make-believe traders, each copies coin-flip trades (1 a day, 1:2, after costs
avg RR -0.05) onto 20 Apex-like accounts for 2 years ($25 eval + $79 activation, $2,000 payout cap, 6 payouts per account, rebuy when blown).
Also: how many no-edge traders turn a live $130k into $1.4M in one month by betting big?"""
import sys, numpy as np, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, '/home/claude/mmmlab')
from mmmlab import propsim as PS
days = pd.bdate_range('2024-01-02', periods=500)
p = (1 - 0.05) / 3           # 2p - (1-p) = -0.05  -> no edge, small cost
def one(seed):
    rng = np.random.default_rng(seed)
    r = np.where(rng.random(len(days)) < p, 2.0, -1.0)
    T = pd.DataFrame({'te': days, 'r': r})
    a = PS.slots(T, risk_usd=500, n=20, eval_cost=25, activation=79, cap=2000, max_pays=6, stagger=0)
    return a['paid'], a['spent'], a['best_month'], a['evals'], a['payouts']
if __name__ == '__main__':
    with Pool(8) as P: R = np.array(P.map(one, range(1000)))
    paid, spent, best, ev, npay = R.T; net = paid - spent
    q = lambda x, k: np.percentile(x, k)
    print('payouts paid: median %.0f  top 10%% %.0f  top 1%% %.0f  max %.0f' % (q(paid, 50), q(paid, 90), q(paid, 99), paid.max()))
    print('net after evals: median %.0f  top 10%% %.0f  top 1%% %.0f  max %.0f   share net>0 %.2f' % (q(net, 50), q(net, 90), q(net, 99), net.max(), (net > 0).mean()))
    print('best month: median %.0f top 1%% %.0f max %.0f' % (q(best, 50), q(best, 99), best.max()))
    print('evals bought median %.0f max %.0f ; payouts median %.0f' % (q(ev, 50), ev.max(), q(npay, 50)))
    np.save('luck_apex.npy', R)
    # live account: $130k, ~20 trading days, 2 trades a day, risk a fixed % of the balance at 1:2, no edge
    rng = np.random.default_rng(1); N = 1_000_000
    for risk in (0.05, 0.10, 0.15, 0.20):
        b = np.full(N, 130000.0)
        for t in range(40):
            w = rng.random(N) < p
            b *= np.where(w, 1 + 2 * risk, 1 - risk)
        print(f'risk {risk:.0%} of balance per trade: reach $1.4M+ = {(b >= 1.4e6).mean()*100:.3f}% of traders ({(b >= 1.4e6).sum()} of 1,000,000); lose half+ = {(b <= 65000).mean()*100:.0f}%')
