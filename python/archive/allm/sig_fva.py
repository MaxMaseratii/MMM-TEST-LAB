"""Signal generator for the 22 MMM PRO FVA strategies (FVA.M1 - FVA.M22).
Port of the Pine v6 indicator claude/MMM_EDGE_PRO_FVA.pine (f_cfg, f_eng, HTF levels, chart turn box, setup state machine).
signals(m) -> one row per setup that places an order / takes an entry (first entry of each setup only).
Not applied (by design): MINR, max open trades, one trade at a time, LVS 400-level memory cap.
Time window: applied at the decision time (next open = close of candle i; a 17:00 close counts as 18:00).
"""
import math, sys, time as _time
import numpy as np, pandas as pd
from numba import njit
sys.path.insert(0, '/home/claude/allm')
from mdata import bars, fine, SPEC

NAN = float('nan')
TFM = {'1m': 1, '5m': 5, '15m': 15, '1h': 60}
LTF2TF = {1: '1m', 5: '5m', 15: '15m', 60: '1h'}

# ── f_cfg (verbatim) ──
_CFG = [
    "5,0,1,1,-1,-1,0,0,2.0,1,0,0,0,0,0,0,1",
    "5,0,3,0,720,960,0,1,3.0,2,0,0,0,0,0,0,1",
    "5,0,2,0,570,720,0,0,2.0,2,0,0,0,0,0,0,1",
    "5,0,4,0,-1,-1,0,1,3.0,2,1,0,0,0,0,0,1",
    "5,0,5,0,-1,-1,1,0,3.0,2,0,0,0,0,0,0,1",
    "1,0,6,0,570,720,0,2,0.0,1,0,0,0,0,0,0,1",
    "1,0,7,1,120,480,0,2,2.0,1,0,0,0,0,0,0,1",
    "5,0,3,1,-1,-1,0,0,2.0,1,0,0,0,0,0,0,1",
    "5,1,8,1,-1,-1,1,0,5.0,3,0,1,0,0,0,0,1",
    "5,2,0,0,-1,-1,0,0,10.0,0,1,0,0,0,0,0,1",
    "15,2,0,0,-1,-1,0,1,10.0,1,0,0,0,0,0,0,1",
    "60,3,0,0,-1,-1,0,0,5.0,2,1,0,0,0,0,0,1",
    "15,1,3,1,1080,120,0,0,2.0,0,0,1,0,0,0,0,1",
    "5,1,1,1,-1,-1,0,4,10.0,0,0,0,1,1,0,0,0",
    "15,1,3,0,120,480,0,1,3.0,2,0,1,1,1,0,0,1",
    "5,1,1,1,-1,-1,0,0,0.0,3,0,0,0,1,3,0,1",
    "15,1,3,1,-1,-1,0,0,3.0,0,0,1,0,0,0,0,1",
    "15,1,2,1,-1,-1,0,2,10.0,0,0,1,2,0,0,0,1",
    "5,1,9,0,-1,-1,0,0,2.0,0,0,0,0,0,0,1,1",
    "15,1,3,1,-1,-1,0,0,5.0,0,0,0,0,2,0,0,1",
    "5,1,2,0,-1,-1,0,1,3.0,0,0,0,0,3,1,0,0",
    "1,1,6,0,-1,-1,0,1,3.0,4,0,2,0,4,0,0,0",
]
_KEYS = ['LTF', 'TYP', 'LVL', 'HELD', 'WA', 'WB', 'H1F', 'STK', 'RRT', 'TRL', 'SIDE', 'TCH', 'AREA', 'PRE', 'REN', 'NBCQ', 'BXX']


def cfg(k):
    v = [float(x) for x in _CFG[k].split(',')]
    c = dict(zip(_KEYS, v))
    for kk in _KEYS:
        if kk != 'RRT':
            c[kk] = int(c[kk])
    c['HELD'] = bool(c['HELD']); c['H1F'] = bool(c['H1F']); c['NBCQ'] = bool(c['NBCQ']); c['BXX'] = bool(c['BXX'])
    return c


BOOK_P1 = [1293, 1256, 866, 352, 1779, 521, 185, 5112, 208, 947, 570, 188, 288, 307, 192, 362, 882, 494, 567, 868, 748, 504]


# ═══════════════════ MMM PRO FVA BOX ENGINE (f_eng) ═══════════════════
class Bx:
    __slots__ = ('id', 'pol', 'kind', 'tier', 'top', 'bot', 'tL', 'mk', 'wife', 'brk', 'leg', 'il')

    def __init__(s, id, pol, kind, tier, top, bot, tL, mk):
        s.id = id; s.pol = pol; s.kind = kind; s.tier = tier; s.top = top; s.bot = bot; s.tL = tL; s.mk = mk
        s.wife = -1; s.brk = ''; s.leg = 0; s.il = ''


def _ext(b):
    return b.bot if b.pol == 1 else b.top


def _nz(x, y):
    return y if x != x else x


class Eng:
    def __init__(s, tick):
        s.A = []; s.by = {}; s.N = 0
        s.zT = []; s.zB = []; s.zD = []; s.zK = []; s.zI = []
        s.HT = tick / 2; s.tick = tick
        s.side = 0; s.tier = 0; s.idT = -1; s.idP = -1; s.idR = -1; s.pend = 0; s.pendW = -1; s.legN = 0; s.bi = -1
        s.pH = NAN; s.pL = NAN; s.lastBc = 0
        s.fnTop = NAN; s.fnBot = NAN; s.fnT = None
        s.seqLo = NAN; s.seqHi = NAN; s.nHi = NAN; s.nLo = NAN
        s.pbX = NAN; s.pbXO = NAN; s.pbXC = NAN; s.pbXT = None
        s.lcT = [NAN, NAN]; s.lcB = [NAN, NAN]; s.lcL = [None, None]

    # helpers
    def get(s, id):
        return s.by.get(id) if id is not None and id >= 0 else None

    def new(s, pol, kind, tr, top, bot, tL, mk):
        id = s.N; s.N += 1
        b = Bx(id, pol, kind, tr, top, bot, tL, mk)
        s.A.append(b); s.by[id] = b
        return id

    def _rm(s, b):
        s.A.remove(b); del s.by[b.id]

    def kill(s, id0):
        id = id0; g = 0
        while id >= 0 and g < 6:
            b = s.by.get(id)
            if b is None:
                break
            s._rm(b)
            id = b.wife
            g += 1

    def findR(s, pol, px):
        r = -1
        for b in s.A:
            if b.kind == 2 and b.pol == pol and abs(_ext(b) - px) < s.HT:
                r = b.id
        return r

    def bsync(s, pol, px, lead):
        HT = s.HT; idT = s.idT
        G = [b for b in s.A if b.kind <= 3 and b.pol == pol and abs(_ext(b) - px) < HT]
        if len(G) < 2:
            return
        e = G[0]; hasRole = False; byLead = False
        for b in G:
            if b.id == lead:
                e = b; byLead = True
        for b in G:
            if not byLead and (b.tL > e.tL or (b.tL == e.tL and b.id > e.id)):
                e = b
            if b.kind >= 1:
                hasRole = True
        oldL = e.tL
        for b in G:
            oldL = min(oldL, b.tL)
        for b in G:
            if pol == 1:
                b.top = e.top
            else:
                b.bot = e.bot
            b.tL = oldL
        kl = []; lastInt = -1
        n = len(G)
        for i in range(n):
            a = G[i]
            if a.kind == 0:
                if hasRole:
                    kl.append(a.id)
                elif lastInt >= 0:
                    kl.append(min(lastInt, a.id)); lastInt = max(lastInt, a.id)
                else:
                    lastInt = a.id
            if a.kind == 3 and i < n - 1:
                for j in range(i + 1, n):
                    b = G[j]
                    if b.kind == 3 and a.tier == b.tier:
                        kl.append(b.id if a.id == idT else a.id if b.id == idT else min(a.id, b.id))
        for id in kl:
            s.kill(id)

    def step(s, o, h, l, c, t):
        ev = 0; evTop = NAN; evBot = NAN
        if o != o or h != h or l != l or c != c:
            return s.side, ev, evTop, evBot
        s.bi += 1; bi = s.bi; HT = s.HT
        isBu = s.pH == s.pH and c > s.pH
        isBe = s.pL == s.pL and c < s.pL
        isN = s.pH == s.pH and not isBu and not isBe
        # 0. wick moves
        mvH = False; mvL = False
        for b in s.A:
            if b.kind >= 4:
                continue
            if b.pol == -1 and h > b.top + HT and c <= b.top:
                b.top = h; mvH = True
            elif b.pol == 1 and l < b.bot - HT and c >= b.bot:
                b.bot = l; mvL = True
        if mvH:
            s.bsync(-1, h, -1)
        if mvL:
            s.bsync(1, l, -1)
        # pullback extreme since the P#
        if s.side != 0 and (s.idP >= 0 or s.pend == 1):
            if s.pbX != s.pbX or (h > s.pbX if s.side == -1 else l < s.pbX):
                s.pbX = h if s.side == -1 else l
                s.pbXO = o; s.pbXC = c; s.pbXT = t
        # 1. turn box
        newId = -1; tzTop = NAN; tzBot = NAN; tzL = None
        if isBu and s.lastBc == -1:
            lo = min(_nz(s.seqLo, l), l)
            tp = o if s.fnTop != s.fnTop else s.fnTop
            tl = t if s.fnT is None else s.fnT
            if tp <= lo:
                tp = max(o, c); tl = t
            newId = s.new(1, 0, s.tier, tp, lo, tl, bi)
            tzTop = tp; tzBot = lo; tzL = tl
        elif isBe and s.lastBc == 1:
            hi = max(_nz(s.seqHi, h), h)
            bt = o if s.fnBot != s.fnBot else s.fnBot
            tl = t if s.fnT is None else s.fnT
            if bt >= hi:
                bt = min(o, c); tl = t
            newId = s.new(-1, 0, s.tier, hi, bt, tl, bi)
            tzTop = hi; tzBot = bt; tzL = tl
        # 2. its role
        if newId >= 0:
            side = s.side
            nb = s.get(newId)
            cand = newId
            resum = nb.pol == side and side != 0 and ((s.pend == 0 and s.idP >= 0) or s.pend == 1)
            if resum and s.pbX == s.pbX and (s.pbX > nb.top + HT if side == -1 else s.pbX < nb.bot - HT):
                rid = s.findR(side, s.pbX)
                if rid < 0:
                    eb = min(s.pbXO, s.pbXC); et = max(s.pbXO, s.pbXC)
                    if side == -1:
                        rid = s.new(-1, 0, s.tier, s.pbX, eb if eb < s.pbX - HT else s.pbX - s.tick, s.pbXT, bi)
                    else:
                        rid = s.new(1, 0, s.tier, et if et > s.pbX + HT else s.pbX + s.tick, s.pbX, s.pbXT, bi)
                nb.il = 'r'
                cand = rid
            cb = s.get(cand)
            oR0 = s.get(s.idR)
            if oR0 is None:
                moreR = True
            elif cb.id == oR0.id:
                moreR = False
            else:
                moreR = cb.top > oR0.top + HT if side == -1 else cb.bot < oR0.bot - HT
            if s.pend == 1 and resum:
                cb.kind = 3; cb.tier = s.tier; cb.leg = s.legN; cb.wife = s.pendW
                s.idT = cb.id; s.pend = 0; s.pendW = -1; s.pbX = NAN
            elif s.pend == 2 and nb.pol == side:
                nb.kind = 3; nb.tier = s.tier; nb.leg = s.legN; nb.wife = s.pendW
                s.idT = newId; s.pend = 0; s.pendW = -1
            elif side == 0:
                s.side = nb.pol; s.tier = 1; s.legN += 1
                nb.kind = 3; nb.tier = 1; nb.leg = s.legN
                s.idT = newId
            elif s.pend == 0 and nb.pol == -side:
                if s.idP < 0:
                    nb.kind = 1; nb.tier = s.tier
                    s.idP = newId
                    s.pbX = h if side == -1 else l
                    s.pbXO = o; s.pbXC = c; s.pbXT = t
                else:
                    nb.il = 'p'
            elif resum and cb.kind == 0:
                if moreR:
                    if oR0 is not None:
                        oR0.kind = 0; oR0.il = 'r'
                    cb.kind = 2; cb.tier = s.tier
                    s.idR = cb.id
                else:
                    cb.il = 'r'; nb.il = 'r'
            else:
                nb.il = 'p' if nb.pol == -side else 'r'
            cbId = cb.id
            for cid in (newId, cbId):
                q = s.get(cid)
                if q is not None:
                    s.bsync(q.pol, _ext(q), q.id if q.mk == bi else -1)
        # 3. official breaks
        official = False
        curT = s.get(s.idT)
        if s.side != 0 and curT is not None:
            side = s.side
            revBrk = c > curT.top if side == -1 else c < curT.bot
            if revBrk:
                ns = -side
                s.kill(curT.wife)
                curT.wife = -1; curT.kind = 4
                curT.brk = 'CDL' if ns == 1 else 'CDS'
                ev = 1 if ns == 1 else 2
                evTop = curT.top; evBot = curT.bot
                if s.pend == 1:
                    s.kill(s.pendW)
                s.pend = 0; s.pendW = -1
                oR = s.get(s.idR)
                if oR is not None:
                    oR.kind = 0; oR.il = 'r'
                s.legN += 1
                bP = s.get(s.idP)
                if bP is not None:
                    bP.kind = 3; bP.tier = 1; bP.leg = s.legN; bP.wife = curT.id
                    s.idT = bP.id
                else:
                    s.idT = -1; s.pend = 2; s.pendW = curT.id
                s.pbX = NAN; s.side = ns; s.tier = 1; s.idP = -1; s.idR = -1
                official = True
            elif s.pend == 0:
                curP = s.get(s.idP)
                if curP is not None:
                    contBrk = c < curP.bot if side == -1 else c > curP.top
                    if contBrk:
                        curP.kind = 4
                        curP.brk = 'LD' if side == 1 else 'SD'
                        ev = 3 if side == 1 else 4
                        evTop = curP.top; evBot = curP.bot
                        s.tier += 1
                        bR = s.get(s.idR)
                        if bR is not None:
                            bR.kind = 3; bR.tier = s.tier; bR.leg = s.legN; bR.wife = curP.id
                            s.idT = bR.id
                        else:
                            s.pend = 1; s.pendW = curP.id
                        if s.pend == 0:
                            s.pbX = NAN
                        s.idP = -1; s.idR = -1
                        official = True
        if official:
            nT0 = s.get(s.idT)
            if nT0 is not None:
                s.bsync(nT0.pol, _ext(nT0), -1)
        # 4. a range ended: clear its internal boxes
        if official:
            for id in [b.id for b in s.A if b.kind == 0]:
                s.kill(id)
        # 5. closes through
        kl = []
        for b in s.A:
            if b.kind >= 4 or b.mk == bi:
                continue
            viol = c < b.bot if b.pol == 1 else c > b.top
            if viol:
                if b.kind == 3:
                    if b.id != s.idT:
                        kl.append(b.id)
                elif b.kind == 2 or b.kind == 0:
                    if b.id == s.idR:
                        s.idR = -1
                    kl.append(b.id)
        for id in kl:
            s.kill(id)
        if official or len(kl) > 0:
            orphan = []
            for w in s.A:
                if w.kind == 4 and w.id != s.pendW:
                    hasH = False
                    for hb in s.A:
                        if hb.kind == 3 and hb.wife == w.id:
                            hasH = True; break
                    if not hasH:
                        orphan.append(w.id)
            for id in orphan:
                b = s.by.get(id)
                if b is not None:
                    s._rm(b)
        # internal boxes: per side keep the most extreme and the newest
        for pol in (-1, 1):
            newest = -1; extId = -1; ex = NAN
            for b in s.A:
                if b.kind == 0 and b.pol == pol:
                    newest = max(newest, b.id)
                    e2 = _ext(b)
                    if ex != ex or (e2 > ex if pol == -1 else e2 < ex):
                        ex = e2; extId = b.id
            kP = [b.id for b in s.A if b.kind == 0 and b.pol == pol and b.id != newest and b.id != extId]
            for id in kP:
                s.kill(id)
        # memory guard
        g = 0
        while len(s.A) > 120 and g < 20:
            g += 1
            cT = s.get(s.idT)
            keepW = -1 if cT is None else cT.wife
            j = 0
            while j < len(s.A):
                bid = s.A[j].id
                if bid != s.idT and bid != s.idP and bid != s.idR and bid != keepW and bid != s.pendW:
                    break
                j += 1
            if j < len(s.A):
                s.kill(s.A[j].id)
        # LEZ: live ones
        zT, zB, zD, zK, zI = s.zT, s.zB, s.zD, s.zK, s.zI
        for i in range(len(zT) - 1, -1, -1):
            d = zD[i]
            if (c < zB[i]) if d == 1 else (c > zT[i]):
                del zT[i]; del zB[i]; del zD[i]; del zK[i]; del zI[i]
            elif d == 1 and l < zB[i]:
                zB[i] = l
            elif d == -1 and h > zT[i]:
                zT[i] = h
        for k in (0, 1):
            if s.lcT[k] == s.lcT[k]:
                if (c < s.lcB[k]) if k == 0 else (c > s.lcT[k]):
                    s.lcT[k] = NAN; s.lcB[k] = NAN; s.lcL[k] = None
                elif k == 0 and l < s.lcB[k]:
                    s.lcB[k] = l
                elif k == 1 and h > s.lcT[k]:
                    s.lcT[k] = h
        if ev > 0:
            d = 1 if ev in (1, 3) else -1
            k = 0 if d == 1 else 1
            ty = ev - 1
            if s.lcT[k] == s.lcT[k]:
                zT.append(s.lcT[k]); zB.append(s.lcB[k]); zD.append(d); zK.append(ty)
                zid = s.N; s.N += 1
                zI.append(zid)
                s.lcT[k] = NAN; s.lcB[k] = NAN; s.lcL[k] = None
                n = 0
                for i in range(len(zK) - 1, -1, -1):
                    if zK[i] == ty:
                        n += 1
                        if n > 1:
                            del zT[i]; del zB[i]; del zD[i]; del zK[i]; del zI[i]
        if tzTop == tzTop:
            k = 0 if isBu else 1
            s.lcT[k] = tzTop; s.lcB[k] = tzBot; s.lcL[k] = tzL
        elif isBu and s.lastBc == 1 and s.fnT is not None and s.nLo == s.nLo:
            lo2 = min(s.nLo, l)
            if s.fnTop > lo2:
                s.lcT[0] = s.fnTop; s.lcB[0] = lo2; s.lcL[0] = s.fnT
        elif isBe and s.lastBc == -1 and s.fnT is not None and s.nHi == s.nHi:
            hi2 = max(s.nHi, h)
            if s.fnBot < hi2:
                s.lcT[1] = hi2; s.lcB[1] = s.fnBot; s.lcL[1] = s.fnT
        # 8. candle sequence
        if isBu or isBe:
            s.lastBc = 1 if isBu else -1
            s.fnTop = NAN; s.fnBot = NAN; s.fnT = None
            s.seqLo = l; s.seqHi = h; s.nHi = NAN; s.nLo = NAN
        elif isN:
            s.nHi = max(_nz(s.nHi, h), h)
            s.nLo = min(_nz(s.nLo, l), l)
            if s.fnT is None:
                s.fnTop = max(o, c); s.fnBot = min(o, c); s.fnT = t
            s.seqLo = min(_nz(s.seqLo, l), l)
            s.seqHi = max(_nz(s.seqHi, h), h)
        s.pH = h; s.pL = l
        return s.side, ev, evTop, evBot


_EC = {}


def run_engine(m, tf, snap=True):
    """MMM PRO FVA engine on every candle of bars(m, tf). Returns dict: side, ev, evT, evB arrays and per-candle snapshots
    boxes = list of tuples (id, kind, d, top, bot, name_kind) and lez = list of (zid, d, top, bot)."""
    key = (m, tf, snap)
    if key in _EC:
        return _EC[key]
    if not snap and (m, tf, True) in _EC:
        return _EC[(m, tf, True)]
    b = bars(m, tf)
    O = b.open.values; H = b.high.values; L = b.low.values; C = b.close.values
    T = b.index.values.astype('datetime64[ns]').astype(np.int64)
    E = Eng(SPEC[m]['tick'])
    n = len(b)
    side = np.zeros(n, np.int8); ev = np.zeros(n, np.int8); evT = np.full(n, NAN); evB = np.full(n, NAN)
    boxes = [None] * n if snap else None
    lez = [None] * n if snap else None
    for i in range(n):
        sd, e, et, eb = E.step(O[i], H[i], L[i], C[i], int(T[i]))
        side[i] = sd; ev[i] = e; evT[i] = et; evB[i] = eb
        if snap:
            boxes[i] = [(x.id, x.kind, (1 if x.brk in ('CDL', 'LD') else -1) if x.kind == 4 else x.pol, x.top, x.bot,
                         x.brk if x.kind == 4 else ('internal', 'P#', 'R#', 'T#')[x.kind]) for x in E.A]
            lez[i] = list(zip(E.zI, E.zD, E.zT, E.zB))
    r = dict(side=side, ev=ev, evT=evT, evB=evB, boxes=boxes, lez=lez, tend=b.tend.values.astype('datetime64[ns]').astype(np.int64))
    _EC[key] = r
    return r


# ═══════════════════ CHART: candle types and the turn box ═══════════════════
@njit(cache=True)
def _turn(T, O, H, L, C):
    n = len(C)
    tbD = np.zeros(n, np.int8); tbT = np.full(n, np.nan); tbB = np.full(n, np.nan); tbN = np.zeros(n, np.bool_)
    tLast = 0; tFnT = np.nan; tFnB = np.nan; tFnTm = -1; tSqL = np.nan; tSqH = np.nan
    for k in range(n):
        if k == 0:
            continue
        bu = C[k] > H[k - 1]; be = C[k] < L[k - 1]; nbc = not bu and not be
        if bu and tLast == -1:
            lo = min(L[k] if np.isnan(tSqL) else tSqL, L[k])
            tp = O[k] if np.isnan(tFnT) else tFnT
            tbN[k] = not np.isnan(tFnT)
            if tp <= lo:
                tp = max(O[k], C[k])
            tbD[k] = 1; tbT[k] = tp; tbB[k] = lo
        elif be and tLast == 1:
            hi = max(H[k] if np.isnan(tSqH) else tSqH, H[k])
            bt = O[k] if np.isnan(tFnB) else tFnB
            tbN[k] = not np.isnan(tFnB)
            if bt >= hi:
                bt = min(O[k], C[k])
            tbD[k] = -1; tbT[k] = hi; tbB[k] = bt
        if bu or be:
            tLast = 1 if bu else -1
            tFnT = np.nan; tFnB = np.nan; tFnTm = -1
            tSqL = L[k]; tSqH = H[k]
        elif nbc:
            if tFnTm < 0:
                tFnT = max(O[k], C[k]); tFnB = min(O[k], C[k]); tFnTm = T[k]
            tSqL = min(L[k] if np.isnan(tSqL) else tSqL, L[k])
            tSqH = max(H[k] if np.isnan(tSqH) else tSqH, H[k])
    return tbD, tbT, tbB, tbN


# first touch → armed → reversal box hit, per level instance
@njit(cache=True)
def _levels(a, kill, d, top, bot, held, dlo, L, H, C, tbD, tbT, tbB, bmL, bmH, BS):
    n = len(a)
    hit = np.full(n, -1, np.int64)
    tch = np.full(n, -1, np.int64)
    for q in range(n):
        k = a[q]; e = kill[q]; dq = d[q]; tp = top[q]; bt = bot[q]
        found = -1
        while k < e:
            if k % BS == 0 and k + BS <= e:
                bk = k // BS
                if (dq == 1 and bmL[bk] > tp) or (dq == -1 and bmH[bk] < bt):
                    k += BS
                    continue
            if (dq == 1 and L[k] <= tp) or (dq == -1 and H[k] >= bt):
                found = k
                break
            k += 1
        if found < 0:
            continue
        k = found
        tch[q] = k
        if k == 0:
            continue
        side_ok = C[k - 1] > tp if dq == 1 else C[k - 1] < bt
        held_ok = (not held) or (C[k] >= bt if dq == 1 else C[k] <= tp)
        if not (side_ok and held_ok):
            continue
        dl = k + dlo
        for kk in range(k + 1, e):
            thr = C[kk] < bt if dq == 1 else C[kk] > tp
            if kk > dl or (held and thr):
                break
            if tbD[kk] == dq and ((tbB[kk] <= tp) if dq == 1 else (tbT[kk] >= bt)):
                hit[q] = kk
                break
    return hit, tch


def _md(ns):
    """minute of day (NY) from int64 ns array"""
    return ((ns // 60_000_000_000) % 1440).astype(np.int64)


def _win(md, WA, WB):
    if WA < 0:
        return np.ones(len(md), bool)
    return (md >= WA) | (md < WB) if WA > WB else (md >= WA) & (md < WB)


class Chart:
    def __init__(s, m, tf):
        b = bars(m, tf)
        s.b = b; s.tf = tf
        s.T = b.index.values.astype('datetime64[ns]').astype(np.int64)
        s.O = b.open.values.astype(float); s.H = b.high.values.astype(float); s.L = b.low.values.astype(float); s.C = b.close.values.astype(float)
        n = len(b); s.n = n
        s.bu = np.zeros(n, bool); s.be = np.zeros(n, bool)
        s.bu[1:] = s.C[1:] > s.H[:-1]; s.be[1:] = s.C[1:] < s.L[:-1]
        s.nbc = np.zeros(n, bool); s.nbc[1:] = ~s.bu[1:] & ~s.be[1:]
        s.tbD, s.tbT, s.tbB, s.tbN = _turn(s.T, s.O, s.H, s.L, s.C)
        BS = 256; s.BS = BS
        nb = (n + BS - 1) // BS
        pad = nb * BS - n
        s.bmL = np.concatenate([s.L, np.full(pad, np.inf)]).reshape(nb, BS).min(1)
        s.bmH = np.concatenate([s.H, np.full(pad, -np.inf)]).reshape(nb, BS).max(1)
        # next-open time (time_close; a 17:00 close → 18:00)
        tc = s.T + TFM[tf] * 60_000_000_000
        tc = np.where(_md(tc) == 1020, tc + 3_600_000_000_000, tc)
        s.tNx = tc


_CH = {}


def chart(m, tf):
    if (m, tf) not in _CH:
        _CH[(m, tf)] = Chart(m, tf)
    return _CH[(m, tf)]


# ═══════════════════ LEVEL INSTANCES ═══════════════════
# each instance: (create chart bar, kill chart bar, d, top, bot, name, seq)
def _kb(ch, tend):
    return np.searchsorted(ch.T, tend, 'left')


def lv_upg(m, ch, tf, nm, SIDE, out, seq0):
    b = bars(m, tf)
    H = b.high.values; L = b.low.values; C = b.close.values
    kb = _kb(ch, b.tend.values.astype('datetime64[ns]').astype(np.int64))
    n = len(b)
    seq = seq0
    for i in range(2, n):
        # c1 = candle i, c2 = i-1, c3 = i-2
        h1, l1, c2, h3, l3 = H[i], L[i], C[i - 1], H[i - 2], L[i - 2]
        d = 0
        if c2 > h3 and l1 > h3:
            d, top, bot = 1, l1, h3
        elif c2 < l3 and h1 < l3:
            d, top, bot = -1, l3, h1
        if d == 0 or not (SIDE == 0 or d == SIDE):
            continue
        a = kb[i]
        if a >= ch.n:
            continue
        rest = C[i + 1:]
        x = np.flatnonzero(rest < bot) if d == 1 else np.flatnonzero(rest > top)
        k = kb[i + 1 + x[0]] if len(x) else ch.n
        # order key: chart bar, then HTF source order, then candle
        out.append((a, k, d, top, bot, 'UPG ' + nm, (a, seq0, i)))
    return out


def lv_boxes(m, ch, tf, src, mode, SIDE, out, srcord):
    """box levels (mode 0 internal · 1 every box · 2 break boxes) and/or LEZ (mode 3)."""
    E = run_engine(m, tf)
    kb = _kb(ch, E['tend'])
    tick = SPEC[m]['tick']
    live = {}
    lastk = -1
    n = len(kb)
    for i in range(n):
        k = kb[i]
        if k >= ch.n:
            break
        if mode == 3:
            items = [(zid, 7, d, top, bot, tf + (' Bu LEZ' if d == 1 else ' Be LEZ')) for (zid, d, top, bot) in E['lez'][i]]
        else:
            items = [(id, kind, d, top, bot, tf + ' ' + nm) for (id, kind, d, top, bot, nm) in E['boxes'][i]
                     if (mode == 1 or (mode == 0 and kind == 0) or (mode == 2 and kind == 4))]
        cur = {}
        for j, (id, kind, d, top, bot, nm) in enumerate(items):
            key = (id, kind, int(round(top / tick)), int(round(bot / tick)))
            cur[key] = (d, top, bot, nm, j)
        for key in list(live.keys()):
            if key not in cur:
                a, d, top, bot, nm, sq = live.pop(key)
                out.append((a, k, d, top, bot, nm, sq))
        for key, (d, top, bot, nm, j) in cur.items():
            if key not in live and (SIDE == 0 or d == SIDE):
                live[key] = (k, d, top, bot, nm, (k, srcord, i * 1000 + j))
    for key, (a, d, top, bot, nm, sq) in live.items():
        out.append((a, ch.n, d, top, bot, nm, sq))
    return out


SWA = [1080, 120, 120, 480, 1080, 570, 570, 570, 810]
SWB = [120, 480, 150, 570, 570, 585, 600, 720, 825]
SWN = ["Asia", "London", "London OR", "Pre-open", "Globex", "NY OR15", "NY OR30", "NY AM", "NY PM OR"]


def lv_session(ch, LVL, SIDE, out):
    T = ch.T; H = ch.H; L = ch.L
    md = _md(T)
    dy = ((T + 6 * 3_600_000_000_000) // 86_400_000_000_000)
    ks = range(8, 9) if LVL == 4 else range(0, 9)
    for k in ks:
        a, b = SWA[k], SWB[k]
        inw = (md >= a) | (md < b) if a > b else (md >= a) & (md < b)
        was = False; sh = NAN; sl = NAN; sd = -1
        for i in range(ch.n):
            iw = inw[i]
            if was and (not iw or dy[i] != sd):
                exp = T[i] + 86_400_000_000_000
                kexp = int(np.searchsorted(T, exp, 'left'))
                if SIDE == 0 or SIDE == 1:
                    out.append((i, kexp, 1, sl, sl, SWN[k] + ' low', (i, 50, k * 2)))
                if LVL == 5 and SIDE in (0, -1):
                    out.append((i, kexp, -1, sh, sh, SWN[k] + ' high', (i, 50, k * 2 + 1)))
                was = False; sh = NAN; sl = NAN
            if iw:
                if not was:
                    was = True; sd = dy[i]; sh = H[i]; sl = L[i]
                else:
                    sh = max(sh, H[i]); sl = min(sl, L[i])
    return out


def levels(m, c, ch):
    LVL = c['LVL']; SIDE = c['SIDE']
    out = []
    if LVL in (2, 3):
        lv_upg(m, ch, '15m', 'M15', SIDE, out, 1)
    if LVL in (1, 3):
        lv_upg(m, ch, '1h', 'H1', SIDE, out, 2)
    if LVL == 3:
        lv_upg(m, ch, '4h', 'H4', SIDE, out, 3)
        lv_upg(m, ch, 'D', 'D', SIDE, out, 4)
        lv_upg(m, ch, 'W', 'W', SIDE, out, 5)
    if LVL == 6:
        lv_boxes(m, ch, '15m', 11, 0, SIDE, out, 10)
    if LVL == 8:
        lv_boxes(m, ch, '1h', 12, 1, SIDE, out, 12)
        lv_boxes(m, ch, '1h', 22, 3, SIDE, out, 13)
    if LVL == 9:
        lv_boxes(m, ch, '15m', 11, 2, SIDE, out, 10)
        lv_boxes(m, ch, '1h', 12, 2, SIDE, out, 12)
        lv_boxes(m, ch, '4h', 13, 2, SIDE, out, 14)
    if LVL == 7:
        lv_boxes(m, ch, '15m', 21, 3, SIDE, out, 10)
        lv_boxes(m, ch, '1h', 22, 3, SIDE, out, 12)
        lv_boxes(m, ch, '4h', 23, 3, SIDE, out, 14)
    if LVL in (4, 5):
        lv_session(ch, LVL, SIDE, out)
    names_rename = {'15m': 'M15', '1h': 'H1', '4h': 'H4'}
    res = []
    for (a, k, d, top, bot, nm, sq) in out:
        if k <= a:
            continue
        p = nm.split(' ', 1)
        if p[0] in names_rename:
            nm = names_rename[p[0]] + ' ' + p[1]
        res.append((a, k, d, top, bot, nm, sq))
    return res


# ═══════════════════ STOPS ═══════════════════
def f_stop(c, m, d, e, top, bot):
    SC = SPEC[m]['s50'] / 50.0; TICK = SPEC[m]['tick']
    STK = c['STK']
    if STK == 1:
        r = 50 * SC
    elif STK == 2:
        r = 20 * SC
    else:
        edge = bot - TICK if d == 1 else top + TICK
        r = abs(e - edge)
        if STK == 0:
            r = min(max(r, 20 * SC), 50 * SC)
        elif STK == 4:
            r = max(r, 10 * SC)
    return e - d * r


# ═══════════════════ SETUPS ═══════════════════
def _h1side(m, ch):
    E = run_engine(m, '1h')
    kb = _kb(ch, E['tend'])
    # side after the last H1 candle processed at or before each chart bar
    idx = np.searchsorted(kb, np.arange(ch.n), 'right') - 1
    s = np.where(idx >= 0, E['side'][np.maximum(idx, 0)], 0)
    return s


def strat_signals(m, k, stats=None, nowin=False):
    c = cfg(k); code = 'FVA.M%d' % (k + 1)
    if nowin:
        c['WA'] = -1
    tf = LTF2TF[c['LTF']]
    ch = chart(m, tf)
    TYP = c['TYP']; n = ch.n
    rows = []
    rrt = c['RRT'] if c['RRT'] > 0 else NAN
    win = _win(_md(ch.tNx), c['WA'], c['WB'])

    def emit(i, d, top, bot, ltop, lbot, ntype, npx, lvn):
        rows.append((code, tf, int(i), ch.b.index[i], int(d), top, bot, ltop, lbot, ntype, float(npx),
                     float(f_stop(c, m, d, npx, top, bot)), rrt, 60, lvn))

    if TYP in (0, 1):
        LV = levels(m, c, ch)
        if stats is not None:
            stats['levels'] = len(LV)
        if not LV:
            return rows
        a = np.array([x[0] for x in LV], np.int64); kl = np.array([x[1] for x in LV], np.int64)
        d = np.array([x[2] for x in LV], np.int64)
        top = np.array([x[3] for x in LV], float); bot = np.array([x[4] for x in LV], float)
        dlo = max(1, int(60 / c['LTF']))
        hit, tch = _levels(a, kl, d, top, bot, c['HELD'], dlo, ch.L, ch.H, ch.C, ch.tbD, ch.tbT, ch.tbB, ch.bmL, ch.bmH, ch.BS)
        if stats is not None:
            # most levels alive and untouched at once (the Pine keeps at most 400 in memory)
            end = np.where(tch >= 0, tch, kl)
            ev = np.concatenate([np.stack([a, np.ones(len(a), np.int64)], 1), np.stack([end, -np.ones(len(a), np.int64)], 1)])
            ev = ev[np.lexsort((ev[:, 1], ev[:, 0]))]
            stats['max_live'] = int(np.cumsum(ev[:, 1]).max())
        h1s = _h1side(m, ch) if c['H1F'] else None
        # one setup per bar and side: the newest level wins
        best = {}
        for q in np.flatnonzero(hit >= 0):
            key = (int(hit[q]), int(d[q]))
            if key not in best or LV[q][6] > LV[best[key]][6]:
                best[key] = q
        for (j, dd), q in sorted(best.items()):
            if c['NBCQ'] and not ch.tbN[j]:
                continue
            if c['H1F'] and h1s[j] != dd:
                continue
            zt, zb = ch.tbT[j], ch.tbB[j]
            lt, lb, lvn = LV[q][3], LV[q][4], LV[q][5]
            if TYP == 0:
                if win[j]:
                    emit(j, dd, zt, zb, lt, lb, 'lmt', zt if dd == 1 else zb, lvn)
            else:
                r = _retest(c, ch, j, dd, zt, zb)
                if r is not None:
                    i, ntype, px = r
                    if win[i]:
                        emit(i, dd, zt, zb, lt, lb, ntype, px, lvn)
    else:
        E = run_engine(m, tf, snap=False)
        ev = E['ev']; evT = E['evT']; evB = E['evB']
        for j in np.flatnonzero((ev == 3) | (ev == 4)):
            dd = 1 if ev[j] == 3 else -1
            if not (c['SIDE'] == 0 or dd == c['SIDE']):
                continue
            zt, zb = evT[j], evB[j]
            lvn = 'LD' if dd == 1 else 'SD'
            if TYP == 3:
                if win[j]:
                    emit(j, dd, zt, zb, NAN, NAN, 'mkt', ch.C[j], lvn)
            else:
                cnt = 0
                for kk in range(j + 1, n):
                    if (ch.C[kk] <= zt) if dd == 1 else (ch.C[kk] >= zb):
                        break
                    cnt += 1
                    if cnt >= 3:
                        if win[kk]:
                            emit(kk, dd, zt, zb, NAN, NAN, 'mkt', ch.C[kk], lvn)
                        break
    return rows


def _retest(c, ch, j, d, top, bot):
    PRE = c['PRE']; TCH = c['TCH']; AREA = c['AREA']
    C = ch.C; H = ch.H; L = ch.L; bu = ch.bu; be = ch.be; nbc = ch.nbc
    st = 0; n2 = nn = no = 0; tk = -1; cin = False
    for k in range(j + 1, ch.n):
        if st == 0:
            brk = C[k] < bot if d == 1 else C[k] > top
            if brk or k >= j + 100:
                return None
            tNow = L[k] <= top if d == 1 else H[k] >= bot
            if tNow:
                if PRE == 2:
                    ok = k == j + 1
                elif PRE == 1:
                    ok = n2 >= 1
                elif PRE == 3:
                    ok = nn >= 1 and no == 0
                elif PRE == 4:
                    ok = n2 >= 1 and nn >= 1 and no >= 1
                else:
                    ok = True
                if not ok:
                    return None
                st = 1; tk = k; cin = False
            else:
                if (bu[k] if d == 1 else be[k]):
                    n2 += 1
                elif nbc[k]:
                    nn += 1
                else:
                    no += 1
        if st == 1:
            brk = C[k] < bot if d == 1 else C[k] > top
            if brk or k >= tk + 60:
                return None
            if bot <= C[k] <= top:
                cin = True
            out = (C[k] > top and bu[k]) if d == 1 else (C[k] < bot and be[k])
            if out:
                if (TCH == 1 and cin) or (TCH == 2 and not cin):
                    return None
                if AREA == 0:
                    return k, 'mkt', C[k]
                lp = (H[k] + L[k]) / 2 if AREA == 1 else (H[k - 1] if d == 1 else L[k - 1])
                return k, 'lmt', lp
    return None


COLS = ['strat', 'tf', 'i', 't', 'side', 'ztop', 'zbot', 'ltop', 'lbot', 'ntype', 'npx', 'nsl', 'nrr', 'nwait', 'level']


def signals(m: str, strats=None, verbose=False) -> pd.DataFrame:
    rows = []
    for k in (strats if strats is not None else range(22)):
        t0 = _time.time()
        st = {}
        r = strat_signals(m, k, st)
        rows += r
        if verbose:
            print('  %s FVA.M%d %s: %d setups (%.1fs) %s' % (m, k + 1, LTF2TF[cfg(k)['LTF']], len(r), _time.time() - t0, st), flush=True)
    df = pd.DataFrame(rows, columns=COLS)
    df['i'] = df['i'].astype(np.int64); df['side'] = df['side'].astype(np.int64); df['nwait'] = df['nwait'].astype(np.int64)
    return df


# ═══════════════════ validation helper: native limit fills on the finest data ═══════════════════
def limit_fills(m, df):
    """for 'lmt' rows: first fine-bar touch of npx within nwait chart bars after the close of candle i.
    returns (filled bool array, fill time array)"""
    f = fine(m)
    FT = f.index.values.astype('datetime64[ns]').astype(np.int64)
    FL = f.low.values; FH = f.high.values
    filled = np.zeros(len(df), bool); ftime = np.full(len(df), np.int64(-1))
    for r, row in enumerate(df.itertuples(index=False)):
        if row.ntype != 'lmt':
            continue
        tfm = TFM[row.tf] * 60_000_000_000
        t0 = pd.Timestamp(row.t).value + tfm
        t1 = t0 + (row.nwait + 1) * tfm
        a = np.searchsorted(FT, t0, 'left'); b = np.searchsorted(FT, t1, 'left')
        x = np.flatnonzero(FL[a:b] <= row.npx) if row.side == 1 else np.flatnonzero(FH[a:b] >= row.npx)
        if len(x):
            filled[r] = True; ftime[r] = FT[a + x[0]]
    return filled, ftime


if __name__ == '__main__':
    ms = sys.argv[1:] or ['NQ', 'MNQ', 'MES', 'MGC', 'MCL']
    for m in ms:
        t0 = _time.time()
        df = signals(m, verbose=True)
        df.to_parquet('/home/claude/allm/sig_fva_%s.parquet' % m)
        print(m, len(df), 'rows', '%.0fs' % (_time.time() - t0), flush=True)
