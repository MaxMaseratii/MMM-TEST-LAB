"""Does the higher-timeframe Xpander Block improve the EDGE PRO strategies when used as a FILTER? (Oct 30 2026)
Every EDGE PRO signal (NQ 2022-25 = P1, MNQ 2026 = P2) is graded with two rules:
  BOOK = the strategy's own entry / stop / target (new Oct 30 rules for C.M4, XCS.M1 longs, X.M3)
  S50  = market at the signal close, fixed 50 pt stop, 1:2
Then each trade is tagged with the HTF XB state known at the signal close (closed HTF candles only, no repaint):
  where the entry sits in the live HTF XB, the XB direction, the last HTF XB break, and live HTF FVAs."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/xb')
from xbzone2 import blocks
from sig_edge import zone
from mdata import bars, TFM
import grade1

RULE_BOOK = {  # strat: (entry e, stop st, target t index, exit x)
    'C.M4': (1, 1, 5, 2), 'X.M3': (1, 0, 2, 0),
}
TIDX = {1.0: 0, 1.5: 1, 2.0: 2, 3.0: 3, 4.0: 4, 6.0: 5, 10.0: 6}

def htf_state(m, htf):
    """per HTF bar (after its close): live XB H, L, bt, bb, dir · last XB break dir and kind · live FVAs list."""
    d = bars(m, htf); o, h, l, c = d.open.values, d.high.values, d.low.values, d.close.values; n = len(c)
    Z = zone(o, h, l, c)
    BL = blocks(o, h, l, c, True)
    live = np.zeros(n, bool); XH = np.full(n, np.nan); XL = XH.copy(); BT = XH.copy(); BB = XH.copy(); XD = np.zeros(n, int)
    for B in BL:
        for (i, H, L, bt, bb) in B['hist']:
            if B['end'] < 0 or i < B['end']:
                live[i] = True; XH[i] = H; XL[i] = L; BT[i] = bt; BB[i] = bb; XD[i] = B['dir']
    lastBrk = np.zeros(n, int); lastKind = np.array([''] * n, dtype=object)
    fvas = [[] for _ in range(n)]     # (side, top, bot) live after bar i
    ends = sorted([(B['end'], B) for B in BL if B['end'] > 0], key=lambda x: x[0])
    cur = []; ptr = 0; lb = 0; lk = ''
    for i in range(n):
        while ptr < len(ends) and ends[ptr][0] == i:
            B = ends[ptr][1]; s = B['brk']; fn = B['fn']
            if s == -1: top, bot = B['H'], min(o[fn], c[fn])
            else: top, bot = max(o[fn], c[fn]), B['L']
            if top > bot: cur.append([s, top, bot])
            lb = s
            if Z['ev'][i] != 0 and Z['evd'][i] == s: lk = 'flip' if Z['ev'][i] == 1 else 'cont'
            else: lk = 'internal'
            ptr += 1
        cur = [f for f in cur if not ((f[0] == -1 and c[i] > f[1]) or (f[0] == 1 and c[i] < f[2]))]
        fvas[i] = [tuple(f) for f in cur[-12:]]
        lastBrk[i] = lb; lastKind[i] = lk
    close_t = (d.index + pd.Timedelta(minutes=TFM[htf])).values.astype('datetime64[ns]').astype(np.int64)
    return dict(close_t=close_t, live=live, XH=XH, XL=XL, BT=BT, BB=BB, XD=XD, lastBrk=lastBrk, lastKind=lastKind, fvas=fvas)

def tag(T, st, side_col='side', px_col='ep'):
    """T: trades with signal close time 'tc' (ns) and entry price. Returns tag columns."""
    k = np.searchsorted(st['close_t'], T.tc.values, 'right') - 1
    out = {'loc': [], 'xbdir': [], 'lastbrk': [], 'lastkind': [], 'infva': []}
    for kk, s, p in zip(k, T[side_col].values, T[px_col].values):
        if kk < 0:
            for key in out: out[key].append('n/a')
            continue
        if st['live'][kk]:
            H, L, bt, bb = st['XH'][kk], st['XL'][kk], st['BT'][kk], st['BB'][kk]
            if p > H or p < L: loc = 'outside XB (above high)' if p > H else 'outside XB (below low)'
            elif bb <= p <= bt: loc = 'inside Balanced'
            elif p > bt: loc = 'in XBB (premium)'
            else: loc = 'in XBS (discount)'
            # trade-relative: right zone = long in XBS / short in XBB
            if loc == 'in XBS (discount)': loc = 'right zone' if s == 1 else 'wrong zone'
            elif loc == 'in XBB (premium)': loc = 'right zone' if s == -1 else 'wrong zone'
            elif loc.startswith('outside'):
                loc = 'outside, break side' if ((s == 1 and p > H) or (s == -1 and p < L)) else 'outside, against'
            out['xbdir'].append('XB with trade' if st['XD'][kk] == s else 'XB against trade')
        else:
            loc = 'no live XB'; out['xbdir'].append('no live XB')
        out['loc'].append(loc)
        lb = st['lastBrk'][kk]
        out['lastbrk'].append('last break with trade' if lb == s else ('last break against' if lb == -s else 'none'))
        out['lastkind'].append(f"last break {st['lastKind'][kk]} {'with' if lb == s else 'against'}" if lb != 0 else 'none')
        inf = any(f[0] == s and f[2] <= p <= f[1] for f in st['fvas'][kk])
        out['infva'].append('inside live FVA of trade side' if inf else 'not inside')
    return pd.DataFrame(out, index=T.index)

def trades_for(m, strat, S, rule):
    tf = S.tf.iloc[0]
    if rule == 'S50': e, st_, t, x = 1, 1, 2, 0
    elif strat in RULE_BOOK: e, st_, t, x = RULE_BOOK[strat]
    elif strat == 'XCS.M1':
        out = []
        for sd, r in ((1, (6, 1, 2, 0)), (-1, (0, 0, 2, 0))):
            g = S[S.side == sd]
            if len(g): out.append(grade1.trades(m, tf, g, *r))
        T = pd.concat(out) if out else pd.DataFrame()
        T['tf'] = tf; return T
    else:
        rr = S.nrr.iloc[0]
        if rr not in TIDX: return pd.DataFrame()
        e, st_, t, x = 0, 0, TIDX[rr], 0
    T = grade1.trades(m, tf, S, e, st_, t, x); T['tf'] = tf
    return T

if __name__ == '__main__':
    HTFS = ['1h', '4h', 'D']
    allT = []
    for m in ('NQ', 'MNQ'):
        states = {h: htf_state(m, h) for h in HTFS}
        Sg = pd.read_parquet(f'sig_edge_{m}.parquet')
        for strat, S in Sg.groupby('strat'):
            if S.tf.iloc[0] == '1m': continue
            S = S.reset_index(drop=True)
            for rule in ('BOOK', 'S50'):
                T = trades_for(m, strat, S, rule)
                if not len(T): continue
                T = T.reset_index(drop=True)
                T['tc'] = (pd.to_datetime(T.t) + pd.to_timedelta(T.tf.map(TFM), unit='min')).values.astype('datetime64[ns]').astype(np.int64)
                T['strat'] = strat; T['rule'] = rule; T['m'] = m
                for h in HTFS:
                    tg = tag(T, states[h])
                    for col in tg.columns: T[f'{h}|{col}'] = tg[col].values
                allT.append(T)
            print(m, strat, flush=True)
    A = pd.concat(allT, ignore_index=True)
    A.to_parquet('xb_filter_trades.parquet')
    print(len(A))
