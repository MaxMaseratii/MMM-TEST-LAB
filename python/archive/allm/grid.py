"""Full grid for any signal table: every entry x every stop x every target x every exit, bull/bear and periods apart.
Entries (16): E0 native · E1 market at the signal close · signal-candle ladder XD..XP (7) · zone ladder XD..XP (7).
  Ladder names are measured from the LOW (Max's names). A limit already passed fills at the signal close.
Stops (6): native · fixed 50-pt equivalent · 1.5x ATR(14) · past the signal candle (2 ticks) · past the zone far side (2 ticks) · past the zone 50%.
Targets (7): 1:1 1:1.5 1:2 1:3 1:4 1:6 1:10.
Exits (4): stop/target only (100 candles) · close through the zone far side (violation) · next session open (02:00, 08:00, 09:30 NY) · first opposite BC close.
Graded on the finest bars: stop wins ties, target only from the bar after a limit fill, cost per trade."""
import sys, numpy as np, pandas as pd
from numba import njit
from mdata import fine, bars, SPEC, period

LAD = [0.0, .125, .25, .5, .75, .875, 1.0]; LADN = ['XD', 'D', 'MD', 'BAL', 'MP', 'P', 'XP']
ENAME = ['native', 'market at signal close'] + [f'candle {n}' for n in LADN] + [f'zone {n}' for n in LADN]
SNAME = ['native stop', 'fixed 50 (scaled)', 'ATR 1.5x', 'past signal candle', 'past zone far side', 'past zone 50%']
TGT = np.array([1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 10.0])
XNAME = ['stop / target only', 'close through the zone (violation)', 'next session open', 'first opposite BC close']
NE, NS, NT, NX = len(ENAME), len(SNAME), len(TGT), len(XNAME)
WAIT, HOLD = 10, 100

def next_open_index(t_ns):
    t = pd.to_datetime(t_ns); m = (t.hour * 60 + t.minute).values; day = t.normalize()
    nxtm = np.full(len(m), 120 + 1440)
    for o in (570, 480, 120):
        nxtm = np.where(m < o, o, nxtm)
    tgt = day.values + (nxtm * 60 * 1_000_000_000).astype('timedelta64[ns]')
    return np.searchsorted(t_ns, tgt.astype(np.int64), 'left')

@njit(cache=True)
def kernel(si, sside, sper, sid, EL, EW, SLF, atr, vio, tc, th, tl, ke, ci, fo, fh, fl, fc, nxt, acc, nbar, s50, cost, minr, tgt):
    nf = len(fh)
    for q in range(len(si)):
        i = si[q]; s = sside[q]; sd = 0 if s == 1 else 1; pr = sper[q]; g = sid[q]
        k0 = ke[i]
        if k0 >= nf: continue
        for e in range(EL.shape[1]):
            lv = EL[q, e]
            if lv != lv: continue
            mk = EW[q, e] == 0 or (s == 1 and lv >= tc[i]) or (s == -1 and lv <= tc[i])
            if mk: lv = tc[i]
            kf = -1
            if mk: kf = k0
            else:
                kexp = ke[min(i + EW[q, e], nbar - 1)] - 1
                for k in range(k0, min(kexp + 1, nf)):
                    if (s == 1 and fl[k] <= lv) or (s == -1 and fh[k] >= lv):
                        kf = k; break
            if kf < 0: continue
            ep = lv; cf = ci[kf]
            kmax = ke[min(cf + HOLD_, nbar - 1)] - 1
            kv = -1; pv = 0.0; ko = -1; po = 0.0
            for j in range(cf, min(cf + HOLD_, nbar)):
                if kv < 0 and vio[q] == vio[q] and ((s == 1 and tc[j] < vio[q]) or (s == -1 and tc[j] > vio[q])):
                    kv = ke[j]; pv = tc[j]
                if ko < 0 and j >= 1 and ((s == 1 and tc[j] < tl[j - 1]) or (s == -1 and tc[j] > th[j - 1])):
                    ko = ke[j]; po = tc[j]
                if kv >= 0 and ko >= 0: break
            ksx = nxt[kf]; psx = fo[ksx] if ksx < nf else fc[nf - 1]
            for st in range(SLF.shape[1]):
                if st == 1: sl = ep - s * s50
                elif st == 2: sl = ep - s * 1.5 * atr[i]
                else: sl = SLF[q, st]
                if sl != sl: continue
                risk = s * (ep - sl)
                if not (risk >= minr): continue
                ks = -1; kt = np.full(7, -1); left = 7; kend = -1; pend = 0.0
                for j in range(kf, nf):
                    if j > kmax:
                        kend = j; pend = fc[j - 1]; break
                    if (s == 1 and fl[j] <= sl) or (s == -1 and fh[j] >= sl):
                        ks = j; break
                    if j > kf or mk:
                        for t in range(7):
                            if kt[t] < 0:
                                tp = ep + s * risk * tgt[t]
                                if (s == 1 and fh[j] >= tp) or (s == -1 and fl[j] <= tp):
                                    kt[t] = j; left -= 1
                    if left == 0 and j >= max(kv, ko, ksx): break
                if ks < 0 and kend < 0:
                    kend = min(kmax + 1, nf - 1); pend = fc[kend - 1]
                cst = cost / risk
                for t in range(7):
                    for x in range(4):
                        best = 1 << 60; r = 0.0
                        if ks >= 0: best = ks; r = -1.0
                        if kt[t] >= 0 and kt[t] < best: best = kt[t]; r = tgt[t]
                        if x == 1 and kv >= 0 and kv <= best: best = kv; r = s * (pv - ep) / risk
                        if x == 2 and ksx < nf and ksx <= best and ksx > kf: best = ksx; r = s * (psx - ep) / risk
                        if x == 3 and ko >= 0 and ko <= best: best = ko; r = s * (po - ep) / risk
                        if best == (1 << 60): r = s * (pend - ep) / risk
                        r -= cst
                        a = acc[g, sd, pr, e, st, t, x]
                        a[0] += 1; a[1] += r; a[2] += r * r
                        if r > 0: a[3] += 1; a[4] += r
                        else: a[5] -= r
HOLD_ = HOLD

def prepare(m, tf, S):
    """S: signals for ONE market and ONE tf with columns i side ztop zbot ntype npx nsl nwait sgid"""
    sp = SPEC[m]; tick = sp['tick']
    d = bars(m, tf); F = fine(m)
    ft = F.index.values.astype('datetime64[ns]').astype(np.int64)
    o, h, l, c = d.open.values, d.high.values, d.low.values, d.close.values
    tr = np.maximum(h - l, np.maximum(np.abs(h - np.r_[c[0], c[:-1]]), np.abs(l - np.r_[c[0], c[:-1]])))
    atr = pd.Series(tr).rolling(14).mean().bfill().values
    ke = np.searchsorted(ft, d.tend.values.astype('datetime64[ns]').astype(np.int64), 'left')
    ks0 = np.searchsorted(ft, d.index.values.astype('datetime64[ns]').astype(np.int64), 'left')
    ci = np.clip(np.searchsorted(ks0, np.arange(len(ft)), 'right') - 1, 0, len(d) - 1)
    nxt = next_open_index(ft)
    i = S.i.values.astype(np.int64); s = S.side.values.astype(np.int64)
    zt = S.ztop.values.astype(float); zb = S.zbot.values.astype(float)
    n = len(S)
    EL = np.full((n, NE), np.nan); EW = np.full((n, NE), WAIT, dtype=np.int64)
    EL[:, 0] = S.npx.values; EW[:, 0] = np.where(S.ntype.values == 'mkt', 0, S.nwait.fillna(WAIT).values.astype(np.int64))
    EL[:, 1] = c[i]; EW[:, 1] = 0
    for k, p in enumerate(LAD):
        EL[:, 2 + k] = l[i] + p * (h[i] - l[i])
        EL[:, 9 + k] = zb + p * (zt - zb)
    SLF = np.full((n, NS), np.nan)
    SLF[:, 0] = S.nsl.values
    SLF[:, 3] = np.where(s == 1, l[i] - 2 * tick, h[i] + 2 * tick)
    SLF[:, 4] = np.where(s == 1, zb - 2 * tick, zt + 2 * tick)
    SLF[:, 5] = (zt + zb) / 2 - s * 2 * tick
    vio = np.where(s == 1, zb, zt)
    if m in ('NQ', 'MNQ'):
        per = np.full(n, 0 if m == 'NQ' else 1, dtype=np.int64)
    else:   # ES / gold / crude: split each chart's own data in two halves by time
        cut = d.index[len(d) // 2]
        per = (d.index[i] >= cut).astype(np.int64)
    return dict(si=i, sside=s, sper=per, sid=S.sgid.values.astype(np.int64), EL=EL, EW=EW, SLF=SLF, atr=atr, vio=vio,
                tc=c, th=h, tl=l, ke=ke, ci=ci, fo=F.open.values, fh=F.high.values, fl=F.low.values, fc=F.close.values, nxt=nxt, nbar=len(d))

def run(m, tf, S, acc):
    sp = SPEC[m]
    P = prepare(m, tf, S)
    kernel(P['si'], P['sside'], P['sper'], P['sid'], P['EL'], P['EW'], P['SLF'], P['atr'], P['vio'], P['tc'], P['th'], P['tl'], P['ke'], P['ci'],
           P['fo'], P['fh'], P['fl'], P['fc'], P['nxt'], acc, P['nbar'], sp['s50'], sp['cost'], sp['s50'] * 0.08, TGT)

def random_signals(m, tf, step=7, seed=7):
    d = bars(m, tf); rng = np.random.default_rng(seed)
    i = np.arange(20, len(d) - 1, step); s = np.where(rng.random(len(i)) < .5, 1, -1)
    c = d.close.values
    return pd.DataFrame(dict(i=i, side=s, ztop=d.high.values[i], zbot=d.low.values[i], ntype='mkt', npx=c[i], nsl=np.nan, nwait=0))
