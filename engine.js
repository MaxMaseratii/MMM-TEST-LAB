/* MMM Test Lab engine (Max Maserati, Nov 2026).
   Runs as a Web Worker in the page, or as a Node module for checks against the Python library (python/mmmlab).
   Same rules as the Python tests: two periods (NQ 2022-25 vs MNQ 2026; ES / gold / crude: first vs second half),
   every entry x stop x target x exit paired, a random twin for every trade, stop wins a same-candle tie, cost per trade,
   PASS = t-score >= 2 in BOTH periods with 30+ trades each. */
(function (G) {
'use strict';
const SPEC = { NQ: { stop: 50, cost: 1, tick: .25, pv: 2 }, ES: { stop: 20, cost: .5, tick: .25, pv: 5 },
  GC: { stop: 12, cost: .2, tick: .1, pv: 10 }, CL: { stop: .5, cost: .02, tick: .01, pv: 100 } };
const MK = { NQ: ['NQ', 'MNQ'], ES: ['MES'], GC: ['MGC'], CL: ['MCL'] };
const BIN = { NQ: 2, ES: .5, GC: .5, CL: .01 };
const SESS = [120, 480, 570, 960, 1020];      // Max's hold rule: 18:00->02:00, 02:00->08:00, 08:30->09:30, 09:30->16:00, ->17:00
const nan = NaN, isn = x => x !== x;

/* ---------- data ---------- */
function decode(ab) {
  const a = new Int32Array(ab.buffer ? ab.buffer.slice(ab.byteOffset, ab.byteOffset + ab.byteLength) : ab);
  const n = a[0], tick = a[1] / 1e6; let p = 2;
  const col = () => { const x = a.subarray(p, p + n); p += n; return x; };
  const dt = col(), dO = col(), dH = col(), dL = col(), dC = col(), V = col(), R = col();
  const t = new Float64Array(n), o = new Float64Array(n), h = new Float64Array(n), l = new Float64Array(n), c = new Float64Array(n), v = new Float64Array(n), res = new Int32Array(n);
  let T = 0, pc = 0;
  for (let i = 0; i < n; i++) {
    T += dt[i]; t[i] = T; const O = pc + dO[i]; o[i] = O * tick; h[i] = (O + dH[i]) * tick; l[i] = (O + dL[i]) * tick;
    const C = O + dC[i]; c[i] = C * tick; pc = C; v[i] = V[i]; res[i] = R[i];
  }
  return { n, t, o, h, l, c, v, res, tick };
}
const sdOf = t => Math.floor((t + 360) / 1440);            // trading day number (18:00 starts the next day)
const mnOf = t => ((t % 1440) + 1440) % 1440;

function bars(F, tf) {
  const T = [], O = [], H = [], L = [], C = [], V = [];
  let k0 = null, j = -1;
  for (let i = 0; i < F.n; i++) {
    if (F.res[i] > tf) continue;
    const k = tf <= 60 ? Math.floor(F.t[i] / tf) * tf : Math.floor((F.t[i] - 1080) / tf) * tf + 1080;
    if (k !== k0) { k0 = k; j++; T.push(k); O.push(F.o[i]); H.push(F.h[i]); L.push(F.l[i]); C.push(F.c[i]); V.push(F.v[i]); }
    else { if (F.h[i] > H[j]) H[j] = F.h[i]; if (F.l[i] < L[j]) L[j] = F.l[i]; C[j] = F.c[i]; V[j] += F.v[i]; }
  }
  const B = { n: T.length, tf, t: Float64Array.from(T), o: Float64Array.from(O), h: Float64Array.from(H), l: Float64Array.from(L), c: Float64Array.from(C), v: Float64Array.from(V) };
  B.mn = new Int32Array(B.n); B.sd = new Int32Array(B.n);
  for (let i = 0; i < B.n; i++) { B.mn[i] = mnOf(B.t[i]); B.sd[i] = sdOf(B.t[i]); }
  B.bc = bcArr(B); B.atr = atrRma(B.h, B.l, B.c, 14);
  return B;
}
function bcArr(B) {
  const b = new Int8Array(B.n);
  for (let i = 1; i < B.n; i++) b[i] = (B.c[i] > B.h[i - 1] && B.c[i] > B.o[i]) ? 1 : (B.c[i] < B.l[i - 1] && B.c[i] < B.o[i]) ? -1 : 0;
  return b;
}
function atrRma(h, l, c, n) {
  const m = c.length, a = new Float64Array(m).fill(nan);
  if (m < n) return a;
  const tr = new Float64Array(m); tr[0] = h[0] - l[0];
  for (let i = 1; i < m; i++) tr[i] = Math.max(h[i] - l[i], Math.abs(h[i] - c[i - 1]), Math.abs(l[i] - c[i - 1]));
  let s = 0; for (let i = 0; i < n; i++) s += tr[i];
  a[n - 1] = s / n;
  for (let i = n; i < m; i++) a[i] = (a[i - 1] * (n - 1) + tr[i]) / n;
  return a;
}
function atrSma(B, n) {
  const m = B.n, a = new Float64Array(m).fill(nan), tr = new Float64Array(m);
  for (let i = 0; i < m; i++) {
    const cp = i ? B.c[i - 1] : nan;
    tr[i] = i ? Math.max(B.h[i] - B.l[i], Math.abs(B.h[i] - cp), Math.abs(B.l[i] - cp)) : B.h[i] - B.l[i];
  }
  let s = 0;
  for (let i = 0; i < m; i++) { s += tr[i]; if (i >= n) s -= tr[i - n]; if (i >= n - 1) a[i] = s / n; }
  return a;
}

/* ---------- MMM Body Flip Trend engine (mirror of python/mmmlab/flip.py, which mirrors the Pine) ---------- */
const KN = { 1: 'FLIP (CDS / CDL)', 2: 'Trend line touch-hold', 3: 'Trend line break', 4: 'ATR line touch-hold', 5: 'ATR line break', 6: 'PO4 touch-hold', 7: 'PO4 break', 8: 'Old trend line touch-hold', 9: 'Old ATR line touch-hold' };
function flipRun(B, c2pct = 50, atrK = .5, openChk = true, keepPo = 10, keepOld = 20) {
  const { o, h, l, c, n } = B, atr = B.atr, NPO = 64, NOLD = 20;
  const trendA = new Int8Array(n), eI = [], eK = [], eS = [], eRef = [], eWk = [];
  const ev = (i, k, s, ref, wk) => { eI.push(i); eK.push(k); eS.push(s); eRef.push(ref); eWk.push(wk); };
  const pLv = new Float64Array(NPO), pSd = new Int8Array(NPO), pTr = new Int32Array(NPO); let pn = 0;
  const oLv = new Float64Array(NOLD), oSd = new Int8Array(NOLD), oAt = new Uint8Array(NOLD), oTr = new Int32Array(NOLD); let on_ = 0;
  let tr = 0, curTr = 0, trStart = 0, setOn = false, setSide = 0, setBody = 0, setBnd = 0, setAtr = nan, setBar = 0;
  let armed = false, oppDone = false, lnB = nan, lnW = nan, tlOn = false, tlLv = nan;
  let atOn = false, atBase = nan, atAtr = nan, atTch = nan, atLvP = nan, pbLv = nan, pbSd = 0, pbRk = 0, lastBuxO = nan, lastBexO = nan;
  const dropOld = () => { for (let m = 0; m < on_ - 1; m++) { oLv[m] = oLv[m + 1]; oSd[m] = oSd[m + 1]; oAt[m] = oAt[m + 1]; oTr[m] = oTr[m + 1]; } on_--; };
  for (let i = 1; i < n; i++) {
    const isBu = c[i] > h[i - 1] && c[i] > o[i], isBe = c[i] < l[i - 1] && c[i] < o[i];
    const body = Math.abs(c[i] - o[i]), bTop = Math.max(o[i], c[i]), bBot = Math.min(o[i], c[i]), a = atr[i];
    for (let k = pn - 1; k >= 0; k--) {
      const sd = pSd[k];
      if ((sd === -1 && c[i] > pLv[k]) || (sd === 1 && c[i] < pLv[k])) {
        ev(i, 7, -sd, pLv[k], sd === -1 ? h[i] : l[i]);
        for (let m = k; m < pn - 1; m++) { pLv[m] = pLv[m + 1]; pSd[m] = pSd[m + 1]; pTr[m] = pTr[m + 1]; } pn--;
      } else if ((sd === -1 && h[i] > pLv[k]) || (sd === 1 && l[i] < pLv[k])) {
        ev(i, 6, sd, pLv[k], sd === -1 ? h[i] : l[i]); pLv[k] = sd === -1 ? h[i] : l[i];
      }
    }
    let flipped = false;
    if (tr === 0) {
      if (isBu || isBe) {
        tr = isBu ? 1 : -1; trStart = i; lnB = isBu ? bBot : bTop; lnW = isBu ? l[i] : h[i];
        tlLv = lnW; tlOn = true; atBase = lnW; atAtr = a; atTch = nan; atOn = true;
      }
    } else {
      for (let k = on_ - 1; k >= 0; k--) {
        const sd = oSd[k];
        if ((sd === 1 && c[i] < oLv[k]) || (sd === -1 && c[i] > oLv[k])) {
          for (let m = k; m < on_ - 1; m++) { oLv[m] = oLv[m + 1]; oSd[m] = oSd[m + 1]; oAt[m] = oAt[m + 1]; oTr[m] = oTr[m + 1]; } on_--;
        } else if ((sd === 1 && l[i] < oLv[k]) || (sd === -1 && h[i] > oLv[k])) {
          ev(i, oAt[k] ? 9 : 8, sd, oLv[k], sd === 1 ? l[i] : h[i]); oLv[k] = sd === 1 ? l[i] : h[i];
        }
      }
      let tlDel = false, atDel = false, tlBrk = nan, atBrk = nan;
      if (tlOn) {
        if ((tr === 1 && c[i] < tlLv) || (tr === -1 && c[i] > tlLv)) {
          tlBrk = tlLv; tlOn = false; lnB = nan; lnW = nan; tlDel = true; ev(i, 3, -tr, tlBrk, tr === 1 ? h[i] : l[i]);
        } else if ((tr === 1 && l[i] < tlLv) || (tr === -1 && h[i] > tlLv)) {
          ev(i, 2, tr, tlLv, tr === 1 ? l[i] : h[i]); tlLv = tr === 1 ? l[i] : h[i];
        }
      }
      if (atOn && !isn(atLvP)) {
        if ((tr === 1 && c[i] < atLvP) || (tr === -1 && c[i] > atLvP)) {
          atBrk = atLvP; atOn = false; atDel = true; ev(i, 5, -tr, atBrk, tr === 1 ? h[i] : l[i]);
        } else if ((tr === 1 && l[i] < atLvP) || (tr === -1 && h[i] > atLvP)) {
          ev(i, 4, tr, atLvP, tr === 1 ? l[i] : h[i]); atTch = tr === 1 ? l[i] : h[i];
        }
      }
      if (!isn(pbLv) && ((pbSd === -1 && c[i] > pbLv) || (pbSd === 1 && c[i] < pbLv))) { pbLv = nan; pbRk = 0; }
      if (atDel || (tlDel && pbRk < 2)) {
        const ref = atDel ? atBrk : tlBrk, side = -tr; let bv = nan;
        const lb = Math.min(Math.min(400, i - 1), Math.max(i - trStart, 1));
        for (let kk = 1; kk <= lb; kk++) {
          const j = i - kk; if (j < 1) break;
          const isBc = side === -1 ? (c[j] > h[j - 1] && c[j] > o[j]) : (c[j] < l[j - 1] && c[j] < o[j]);
          if (isBc) {
            const lv = o[j];
            if ((side === -1 && lv > ref && c[i] < lv) || (side === 1 && lv < ref && c[i] > lv))
              if (isn(bv) || (side === -1 && lv < bv) || (side === 1 && lv > bv)) bv = lv;
          }
        }
        if (isn(bv)) bv = ref;
        pbLv = bv; pbSd = side; pbRk = atDel ? 2 : 1;
      }
      let cancelled = false, small = false;
      if (setOn) {
        const cancel = (setSide === -1 && c[i] > setBnd) || (setSide === 1 && c[i] < setBnd);
        const same = setSide === -1 ? isBe : isBu;
        const qual = same && body >= setBody * c2pct / 100;
        const oppO = setSide === -1 ? lastBuxO : lastBexO;
        if (!cancel && !oppDone && !isn(oppO) && ((setSide === -1 && c[i] < oppO) || (setSide === 1 && c[i] > oppO))) oppDone = true;
        const beyond = !openChk || isn(oppO) || oppDone;
        if (cancel) { setOn = false; armed = false; oppDone = false; cancelled = true; }
        else if (qual && !beyond && !armed) armed = true;
        else if ((qual || armed) && beyond) {
          armed = false; oppDone = false;
          if (tlOn) { if (on_ === NOLD || on_ >= keepOld) dropOld(); oLv[on_] = tlLv; oSd[on_] = tr; oAt[on_] = 0; oTr[on_] = curTr; on_++; }
          if (atOn && !isn(atLvP)) { if (on_ === NOLD || on_ >= keepOld) dropOld(); oLv[on_] = atLvP; oSd[on_] = tr; oAt[on_] = 1; oTr[on_] = curTr; on_++; }
          tr = setSide; curTr++; trStart = setBar;
          let exW = nan, exB = nan;
          for (let j = setBar; j <= i; j++) {
            const vw = tr === -1 ? h[j] : l[j], vb = tr === -1 ? Math.max(o[j], c[j]) : Math.min(o[j], c[j]);
            if (isn(exW) || (tr === -1 && vw > exW) || (tr === 1 && vw < exW)) exW = vw;
            if (isn(exB) || (tr === -1 && vb > exB) || (tr === 1 && vb < exB)) exB = vb;
          }
          lnB = exB; lnW = exW; tlLv = exW; tlOn = true; atBase = exW; atAtr = setAtr; atTch = nan; atOn = true;
          setOn = false; flipped = true;
          let cdsLv;
          if (!isn(pbLv) && pbSd === tr) cdsLv = pbLv;
          else { cdsLv = tr === -1 ? lastBuxO : lastBexO; if (isn(cdsLv)) cdsLv = o[i]; }
          pbLv = nan; pbRk = 0;
          const poPx = exW;
          if (pn === NPO) { for (let m = 0; m < pn - 1; m++) { pLv[m] = pLv[m + 1]; pSd[m] = pSd[m + 1]; pTr[m] = pTr[m + 1]; } pn--; }
          pLv[pn] = poPx; pSd[pn] = tr; pTr[pn] = curTr; pn++;
          while (pn > keepPo) {
            let drop = -1;
            for (let m = 0; m < pn; m++) {
              let live = pTr[m] === curTr;
              if (!live) for (let q = 0; q < on_; q++) if (oTr[q] === pTr[m]) { live = true; break; }
              if (!live) { drop = m; break; }
            }
            if (drop < 0) break;
            for (let m = drop; m < pn - 1; m++) { pLv[m] = pLv[m + 1]; pSd[m] = pSd[m + 1]; pTr[m] = pTr[m + 1]; } pn--;
          }
          ev(i, 1, tr, cdsLv, poPx);
        } else if (same && !armed) { setOn = false; small = true; }
      }
      if (!flipped) {
        const dirOk = tr === 1 ? isBu : isBe, bprev = Math.abs(c[i - 1] - o[i - 1]);
        if (dirOk && body > 0 && body >= bprev) {
          const candB = tr === 1 ? Math.min(o[i - 1], c[i - 1]) : Math.max(o[i - 1], c[i - 1]);
          const candW = tr === 1 ? l[i - 1] : h[i - 1], cur = lnW;
          if (isn(cur) || (tr === 1 && candW > cur) || (tr === -1 && candW < cur)) {
            lnB = candB; lnW = candW;
            if (!tlOn) { tlOn = true; tlLv = candW; }
            else if ((tr === 1 && candW > tlLv) || (tr === -1 && candW < tlLv)) tlLv = candW;
            const nb = candW, nLv = nb - tr * a * atrK; let curLv = nan;
            if (!isn(atBase) && !isn(a)) {
              curLv = atBase - tr * a * atrK;
              if (!isn(atTch)) curLv = tr === 1 ? Math.min(curLv, atTch) : Math.max(curLv, atTch);
            }
            if (!atOn) { atOn = true; atBase = nb; atAtr = atr[i - 1]; atTch = nan; }
            else if (isn(curLv) || (tr === 1 && nLv > curLv) || (tr === -1 && nLv < curLv)) { atBase = nb; atAtr = atr[i - 1]; atTch = nan; }
          }
        }
      }
      const opp = tr === 1 ? isBe : isBu;
      if (!setOn && !flipped && !cancelled && opp) {
        const oppC1 = tr === 1 ? lastBuxO : lastBexO;
        const c1Brk = !isn(oppC1) && ((tr === 1 && c[i] < oppC1) || (tr === -1 && c[i] > oppC1));
        oppDone = (small && oppDone) || c1Brk;
        setOn = true; setSide = -tr; setBody = body; setBnd = setSide === -1 ? bTop : bBot; setAtr = a; setBar = i;
      }
    }
    if (atOn && tr !== 0) {
      let lv = nan;
      if (!isn(atBase) && !isn(a)) { lv = atBase - tr * a * atrK; if (!isn(atTch)) lv = tr === 1 ? Math.min(lv, atTch) : Math.max(lv, atTch); }
      atLvP = lv;
    } else atLvP = nan;
    if (isBu) lastBuxO = o[i];
    if (isBe) lastBexO = o[i];
    trendA[i] = tr;
  }
  return { trend: trendA, eI, eK, eS, eRef, eWk };
}

/* ---------- levels ---------- */
function vp(F, idx, b) {
  if (!idx.length) return [nan, nan, nan];
  let lo = Infinity, hi = -Infinity, tv = 0;
  for (const i of idx) { if (F.l[i] < lo) lo = F.l[i]; if (F.h[i] > hi) hi = F.h[i]; tv += F.v[i]; }
  if (tv <= 0) return [nan, nan, nan];
  const p0 = Math.floor(lo / b) * b, nb = Math.floor((hi - p0) / b) + 1, df = new Float64Array(nb + 1);
  for (const i of idx) {
    const i0 = Math.min(nb - 1, Math.max(0, Math.floor((F.l[i] - p0) / b))), i1 = Math.min(nb - 1, Math.max(0, Math.floor((F.h[i] - p0) / b)));
    const w = F.v[i] / (i1 - i0 + 1); df[i0] += w; df[i1 + 1] -= w;
  }
  const hs = new Float64Array(nb); let s = 0, tot = 0, pc = 0;
  for (let k = 0; k < nb; k++) { s += df[k]; hs[k] = s; tot += s; if (s > hs[pc]) pc = k; }
  let a = pc, bb = pc, acc = hs[pc];
  while (acc < .7 * tot && (a > 0 || bb < nb - 1)) {
    const up = bb < nb - 1 ? hs[bb + 1] : -1, dn = a > 0 ? hs[a - 1] : -1;
    if (up >= dn) { bb++; acc += up; } else { a--; acc += dn; }
  }
  return [p0 + (pc + .5) * b, p0 + (bb + 1) * b, p0 + a * b];
}
function dayLevels(F, m) {
  const b = BIN[m], days = new Map(), weeks = new Map();
  for (let i = 0; i < F.n; i++) {
    const sd = sdOf(F.t[i]), mn = mnOf(F.t[i]);
    let D = days.get(sd); if (!D) { D = { all: [], ny: [], lon: [], as: [], on: [] }; days.set(sd, D); }
    D.all.push(i); if (mn >= 570 && mn < 960) D.ny.push(i); if (mn >= 120 && mn < 480) D.lon.push(i);
    if (mn >= 1080 && mn < 1200) D.as.push(i); if (mn >= 1080 || mn < 570) D.on.push(i);
    const wk = Math.floor((sd - 2) / 7);            // weeks Sat..Fri (W-FRI, like pandas)
    let W = weeks.get(wk); if (!W) { W = []; weeks.set(wk, W); } W.push(i);
  }
  const hiOf = ix => { let x = -Infinity; for (const i of ix) if (F.h[i] > x) x = F.h[i]; return ix.length ? x : nan; };
  const loOf = ix => { let x = Infinity; for (const i of ix) if (F.l[i] < x) x = F.l[i]; return ix.length ? x : nan; };
  const WV = new Map(); for (const [k, ix] of weeks) WV.set(k, vp(F, ix, b));
  const keys = [...days.keys()].sort((x, y) => x - y), out = new Map(); let prev = null;
  for (const sd of keys) {
    const D = days.get(sd), P = vp(F, m === 'GC' ? D.all : D.ny, b), wk = Math.floor((sd - 2) / 7), pw = WV.get(wk - 1) || [nan, nan, nan];
    const r = { H: hiOf(D.all), L: loOf(D.all), POC: P[0], VAH: P[1], VAL: P[2], lonH: hiOf(D.lon), lonL: loOf(D.lon), asH: hiOf(D.as), asL: loOf(D.as), onH: hiOf(D.on), onL: loOf(D.on), wPOC: pw[0], wVAH: pw[1], wVAL: pw[2] };
    r.pH = prev ? prev.H : nan; r.pL = prev ? prev.L : nan; r.pPOC = prev ? prev.POC : nan; r.pVAH = prev ? prev.VAH : nan; r.pVAL = prev ? prev.VAL : nan;
    out.set(sd, r); prev = r;
  }
  return out;
}
function zones(F, m, tf) {
  const Z = bars(F, tf), { o, h, l, c, n } = Z, atr = atrSma(Z, 14), tick = SPEC[m].tick, out = [];
  const dayList = [...new Set(Array.from(Z.sd))].sort((x, y) => x - y), dpos = new Map(dayList.map((d, k) => [d, k]));
  const dp = Int32Array.from(Z.sd, d => dpos.get(d));
  const firstOfDpos = k => { let lo = 0, hi = n; while (lo < hi) { const md = (lo + hi) >> 1; if (dp[md] < k) lo = md + 1; else hi = md; } return lo; };
  for (let j = 4; j < n; j++) {
    const a = atr[j - 1]; if (!(a > 0)) continue;
    const body = c[j] - o[j];
    for (const s of [1, -1]) {
      if (s * body < a) continue;
      if (!((s === 1 && c[j] > h[j - 1]) || (s === -1 && c[j] < l[j - 1]))) continue;
      let mx = -Infinity, mnn = Infinity; for (let q = j - 3; q < j; q++) { if (h[q] > mx) mx = h[q]; if (l[q] < mnn) mnn = l[q]; }
      const strict = s * body >= 1.5 * a && (mx - mnn) <= 2 * a;
      let top = Math.max(o[j - 1], c[j - 1]), bot = Math.min(o[j - 1], c[j - 1]);
      if (top - bot < 2 * tick) { top = h[j - 1]; bot = l[j - 1]; }
      const kmax = Math.min(n, j + 1 + 20 * Math.floor(1440 / tf));
      let kd = kmax - 1;
      for (let q = j + 1; q < kmax; q++) if ((s === 1 && c[q] < bot) || (s === -1 && c[q] > top)) { kd = q; break; }
      if (dp[j] + 20 <= dp[n - 1]) kd = Math.min(kd, firstOfDpos(dp[j] + 20));
      kd = Math.min(kd, n - 1);
      out.push({ tA: Z.t[j] + tf, tD: Z.t[kd] + tf, top, bot, s, tf, strict });
    }
  }
  return out;
}
function react(B, ks, L, s, eps, far, maxw = 12) {
  const { o, h, l, c } = B, res = {}; let pn = 0;
  const cand = [];
  for (let p = 0; p < ks.length; p++) { const k = ks[p]; if (s === 1 ? (l[k] <= L + eps && c[k - 1] > L) : (h[k] >= L - eps && c[k - 1] < L)) cand.push(p); }
  for (const p of cand) {
    if (p < pn) continue;
    const k0 = ks[p]; let ex = s === 1 ? l[k0] : h[k0]; const endp = Math.min(ks.length, p + maxw); let q = p;
    while (q < endp) {
      const j = ks[q];
      ex = s === 1 ? Math.min(ex, l[j]) : Math.max(ex, h[j]);
      if (far !== null && ((s === 1 && c[j] < far) || (s === -1 && c[j] > far))) return res;
      if ((s === 1 && c[j] > o[j] && c[j] > L) || (s === -1 && c[j] < o[j] && c[j] < L)) {
        if (!res.close) res.close = [j, ex, k0];
        if (!res.aggr && ((s === 1 && c[j] > h[j - 1]) || (s === -1 && c[j] < l[j - 1]))) res.aggr = [j, ex, k0];
        if (res.close && res.aggr) return res;
      }
      q++;
    }
    pn = q;
  }
  return res;
}

/* ---------- signal blocks ---------- */
function groupDays(B) { const g = new Map(); for (let i = 0; i < B.n; i++) { let a = g.get(B.sd[i]); if (!a) { a = []; g.set(B.sd[i], a); } a.push(i); } return g; }
function signals(ctx, P) {
  const { B, m } = ctx, sp = SPEC[m], tick = sp.tick, { o, h, l, c, mn, n } = B;
  const I = [], S = [], WK = [], LV = [], TAG = [], TP = [];
  const push = (i, s, wk, lv, tag, tp) => { I.push(i); S.push(s); WK.push(wk); LV.push(lv); TAG.push(tag || ''); TP.push(tp === undefined ? nan : tp); };
  const wick = (i, s) => s === 1 ? l[i] - tick : h[i] + tick;
  const k = P.idea;
  if (k === 'bc') {
    let run = 0, runSide = 0, nbc = 0;
    for (let i = 1; i < n; i++) {
      const b = B.bc[i];
      if (b !== 0) {
        if (b === runSide) run++; else { run = 1; runSide = b; }
        const okBody = !(P.minBody > 0) || Math.abs(c[i] - o[i]) >= P.minBody * B.atr[i];
        const okNbc = !(P.prevNbc > 0) || nbc >= P.prevNbc;
        const okNth = !(P.nth > 0) || run === P.nth;
        if (okBody && okNbc && okNth) push(i, P.fade ? -b : b, wick(i, P.fade ? -b : b), o[i]);
        nbc = 0;
      } else { nbc++; }
    }
  } else if (k === 'flip') {
    const E = ctx.flip;
    for (let q = 0; q < E.eI.length; q++) if (E.eK[q] === +P.event) {
      const i = E.eI[q], s = P.fade ? -E.eS[q] : E.eS[q];
      push(i, s, (+P.event === 1 && !P.fade) ? E.eWk[q] : wick(i, s), E.eRef[q], KN[E.eK[q]]);
    }
  } else if (k === 'orb') {
    const st = +P.orbStart, len = +P.orbLen, cut = +P.orbCut;
    for (const [, ix] of groupDays(B)) {
      const rng = ix.filter(i => mn[i] >= st && mn[i] < st + len), after = ix.filter(i => mn[i] >= st + len && mn[i] < cut);
      if (rng.length < 1 || after.length < 2) continue;
      let RH = -Infinity, RL = Infinity; for (const i of rng) { if (h[i] > RH) RH = h[i]; if (l[i] < RL) RL = l[i]; }
      for (const s of [1, -1]) {
        const edge = s === 1 ? RH : RL;
        if (P.orbMode === 'break') {
          for (const i of after) if (s * (c[i] - edge) > 0) { push(i, s, wick(i, s), edge); break; }
        } else if (P.orbMode === 'fail') {                // break out, then close back inside -> fade
          let out = false, ex = nan;
          for (const i of after) {
            if (!out && s * (h[i] * (s === 1) + l[i] * (s === -1) - edge) > 0) out = true;
            if (out) { ex = s === 1 ? Math.max(isn(ex) ? -Infinity : ex, h[i]) : Math.min(isn(ex) ? Infinity : ex, l[i]);
              if (s * (c[i] - edge) < 0) { push(i, -s, s === 1 ? ex + tick : ex - tick, edge); break; } }
          }
        } else {                                           // retest: close out, pull back to the edge, close back out in color
          let bo = false, tch = false, ex = nan;
          for (const i of after) {
            if (!bo) { if (s * (c[i] - edge) > 0) bo = true; continue; }
            if (s * (c[i] - (s === 1 ? RL : RH)) < 0) break;
            if (!tch && (s === 1 ? l[i] <= edge : h[i] >= edge)) { tch = true; ex = s === 1 ? l[i] : h[i]; }
            if (tch) { ex = s === 1 ? Math.min(ex, l[i]) : Math.max(ex, h[i]);
              if (s * (c[i] - edge) > 0 && s * (c[i] - o[i]) > 0) { push(i, s, s === 1 ? ex - tick : ex + tick, edge); break; } }
          }
        }
      }
    }
  } else if (k === 'ib') {
    const cut = +P.ibCut;
    for (const [, ix0] of groupDays(B)) {
      const ix = ix0.filter(i => mn[i] >= 570 && mn[i] < 960); if (!ix.length) continue;
      const ib = ix.filter(i => mn[i] < 630), rest = ix.filter(i => mn[i] >= 630 && mn[i] < cut);
      if (ib.length < 3 || ix.length - ib.length < 3 || rest.length < 2) continue;
      let IBH = -Infinity, IBL = Infinity; for (const i of ib) { if (h[i] > IBH) IBH = h[i]; if (l[i] < IBL) IBL = l[i]; }
      const MID = (IBH + IBL) / 2; if (!(IBH > IBL)) continue;
      const trend = c[ib[ib.length - 1]] > o[ib[0]] ? 1 : -1;
      if (P.ibSetup === 'FA' || P.ibSetup === 'both') for (const s of [1, -1]) {
        const edge = s === 1 ? IBL : IBH; let out = false, ex = nan;
        for (const j of rest) {
          if (!out && (s === 1 ? l[j] < edge : h[j] > edge)) out = true;
          if (out) { ex = s === 1 ? (isn(ex) ? l[j] : Math.min(ex, l[j])) : (isn(ex) ? h[j] : Math.max(ex, h[j]));
            if ((s === 1 && c[j] > edge) || (s === -1 && c[j] < edge)) { push(j, s, s === 1 ? ex - tick : ex + tick, edge, 'FA', MID); break; } }
        }
      }
      if (P.ibSetup === 'TC' || P.ibSetup === 'both') {
        const s = trend; let touched = false, ex = nan;
        for (const j of rest) {
          if ((s === 1 && c[j] < IBL) || (s === -1 && c[j] > IBH)) break;
          if (!touched && ((s === 1 && l[j] <= MID) || (s === -1 && h[j] >= MID))) touched = true;
          if (touched) { ex = s === 1 ? (isn(ex) ? l[j] : Math.min(ex, l[j])) : (isn(ex) ? h[j] : Math.max(ex, h[j]));
            if ((s === 1 && c[j] > MID && c[j] > o[j]) || (s === -1 && c[j] < MID && c[j] < o[j])) { push(j, s, s === 1 ? ex - tick : ex + tick, MID, 'TC', s === 1 ? IBH : IBL); break; } }
        }
      }
    }
  } else if (k === 'level') {
    const DL = ctx.levels(), eps = .05 * sp.stop, want = new Set(P.lvls || []);
    const ZZ = (want.has('Z30') || want.has('Z60')) ? ctx.zones() : [];
    const w0 = +P.lvFrom, w1 = +P.lvTo;
    for (const [sd, ix] of groupDays(B)) {
      const r = DL.get(sd); if (!r) continue;
      const ks = ix.filter(i => i > 0 && inWin(mn[i], w0, w1)); if (ks.length < 2) continue;
      const lines = [];
      if (want.has('PD')) lines.push(['Prev day high', r.pH], ['Prev day low', r.pL]);
      if (want.has('LON') && w0 >= 480) lines.push(['London high', r.lonH], ['London low', r.lonL]);
      if (want.has('ASIA') && (w0 >= 1200 || w0 < 1080)) lines.push(['Asia range high', r.asH], ['Asia range low', r.asL]);
      if (want.has('ON') && w0 >= 570 && w0 < 1080) lines.push(['Overnight high', r.onH], ['Overnight low', r.onL]);
      if (want.has('NYVP')) lines.push(['Prev session POC', r.pPOC], ['Prev session VAH', r.pVAH], ['Prev session VAL', r.pVAL]);
      if (want.has('WKVP')) lines.push(['Prev week POC', r.wPOC], ['Prev week VAH', r.wVAH], ['Prev week VAL', r.wVAL]);
      const todo = [];
      for (const [nm, p] of lines) if (!isn(p)) for (const s of [1, -1]) todo.push([nm, p, s, null, ks]);
      const t0 = B.t[ks[0]], t1 = B.t[ks[ks.length - 1]];
      for (const z of ZZ) {
        if (!want.has('Z' + z.tf) || (P.strict && !z.strict) || z.tA > t1 || z.tD <= t0) continue;
        const kk = ks.filter(i => B.t[i] >= z.tA && B.t[i] < z.tD); if (kk.length < 2) continue;
        todo.push([(z.s === 1 ? 'Demand ' : 'Supply ') + z.tf + 'm', z.s === 1 ? z.top : z.bot, z.s, z.s === 1 ? z.bot : z.top, kk]);
      }
      for (const [nm, L, s, far, kk] of todo) {
        const R = react(B, kk, L, s, eps, far);
        const hit = R[P.trig || 'aggr'];
        if (!hit) continue;
        const [j, ex] = hit, sd2 = P.fade ? -s : s;
        push(j, sd2, P.fade ? wick(j, sd2) : (s === 1 ? ex - tick : ex + tick), L, nm);
      }
    }
  } else if (k === 'time') {
    const at = +P.tAt;
    for (let i = 1; i < n; i++) if (mn[i] === at) {
      const col = Math.sign(c[i] - o[i]); if (!col) continue;
      if (P.tNeedBc && B.bc[i] === 0) continue;
      const s = P.fade ? -col : col; push(i, s, wick(i, s), (h[i] + l[i]) / 2);
    }
  } else if (k === 'custom') {
    let f;
    try { f = new Function('o', 'h', 'l', 'c', 'v', 'i', 'mn', 'bc', 'atr', 'day', 'wd', '"use strict"; return (' + (P.expr || '0') + ');'); }
    catch (e) { throw new Error('Formula error: ' + e.message); }
    for (let i = 20; i < n; i++) {
      let s; try { s = f(o, h, l, c, B.v, i, mn[i], B.bc, B.atr, B.sd[i], (B.sd[i] + 4) % 7); } catch (e) { throw new Error('Formula error at bar ' + i + ': ' + e.message); }
      s = s > 0 ? 1 : s < 0 ? -1 : 0;
      if (s) push(i, s, wick(i, s), o[i]);
    }
  }
  return { I, S, WK, LV, TAG, TP };
}
function inWin(x, a, b) { return a <= b ? (x >= a && x < b) : (x >= a || x < b); }

/* ---------- filters ---------- */
function htfTrend(F, B, tf) {
  const Hb = bars(F, tf), out = new Int8Array(B.n); let p = -1, last = 0;
  for (let i = 0; i < B.n; i++) {
    const close = B.t[i] + B.tf;
    while (p + 1 < Hb.n && Hb.t[p + 1] + tf <= close) { p++; if (Hb.bc[p] !== 0) last = Hb.bc[p]; }
    out[i] = last;
  }
  return out;
}
function applyFilters(ctx, sig, P) {
  const { B } = ctx, keep = [];
  const days = new Set((P.days || [1, 2, 3, 4, 5, 0]).map(Number));
  const ht = P.htf && P.htf !== 'off' ? htfTrend(ctx.F, B, +P.htfTf) : null;
  const fl = P.flipF && P.flipF !== 'off' ? ctx.flip.trend : null;
  const seen = new Set();
  for (let q = 0; q < sig.I.length; q++) {
    const i = sig.I[q], s = sig.S[q];
    if (P.side === 'long' && s !== 1) continue;
    if (P.side === 'short' && s !== -1) continue;
    if (P.useWin && !inWin(B.mn[i], +P.winFrom, +P.winTo)) continue;
    if (!days.has((B.sd[i] + 4) % 7)) continue;
    if (ht) { const t = ht[i]; if (P.htf === 'with' && t !== s) continue; if (P.htf === 'against' && t !== -s) continue; }
    if (fl) { const t = fl[i]; if (P.flipF === 'with' && t !== s) continue; if (P.flipF === 'against' && t !== -s) continue; }
    if (P.onePerDay) { const key = B.sd[i] * 3 + s; if (seen.has(key)) continue; seen.add(key); }
    keep.push(q);
  }
  return { I: keep.map(q => sig.I[q]), S: keep.map(q => sig.S[q]), WK: keep.map(q => sig.WK[q]), LV: keep.map(q => sig.LV[q]), TAG: keep.map(q => sig.TAG[q]), TP: keep.map(q => sig.TP[q]) };
}

/* ---------- grader ---------- */
function rng32(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function ends(B, cap) {
  const n = B.n, dayEnd = new Int32Array(n), segEnd = new Int32Array(n), seg = new Int32Array(n);
  for (let i = 0; i < n; i++) { const m = B.mn[i]; let k = 0; if (m < 1080) for (const b of SESS) if (b <= m) k++; seg[i] = B.sd[i] * 10 + k; }
  dayEnd[n - 1] = n - 1; segEnd[n - 1] = n - 1;
  for (let i = n - 2; i >= 0; i--) { dayEnd[i] = B.sd[i] === B.sd[i + 1] ? dayEnd[i + 1] : i; segEnd[i] = seg[i] === seg[i + 1] ? segEnd[i + 1] : i; }
  const capEnd = new Int32Array(n);
  for (let i = 0; i < n; i++) capEnd[i] = cap === 'day' && B.tf <= 60 ? dayEnd[i] : Math.min(n - 1, i + 2000);
  return { dayEnd, segEnd, capEnd };
}
/* one walk resolves every target at once. tg: absolute target prices (NaN = none). returns [R per target], exit bar per target */
function walk(B, fi, s, ep, sl, tg, jEnd, exitMask, cost, R, X) {
  const { o, h, l, c } = B, risk = s * (ep - sl), nt = tg.length; let left = nt;
  const done = new Uint8Array(nt);
  for (let j = fi + 1; j <= jEnd; j++) {
    if (s === 1 ? l[j] <= sl : h[j] >= sl) {
      const px = s === 1 ? Math.min(o[j], sl) : Math.max(o[j], sl), r = (s * (px - ep) - cost) / risk;
      for (let q = 0; q < nt; q++) if (!done[q]) { R[q] = r; X[q] = j; } return;
    }
    for (let q = 0; q < nt; q++) if (!done[q] && !isn(tg[q]) && (s === 1 ? h[j] >= tg[q] : l[j] <= tg[q])) { R[q] = (s * (tg[q] - ep) - cost) / risk; X[q] = j; done[q] = 1; left--; }
    if (!left) return;
    if (exitMask && exitMask[j]) { const r = (s * (c[j] - ep) - cost) / risk; for (let q = 0; q < nt; q++) if (!done[q]) { R[q] = r; X[q] = j; } return; }
  }
  const r = (s * (c[jEnd] - ep) - cost) / risk;
  for (let q = 0; q < nt; q++) if (!done[q]) { R[q] = r; X[q] = jEnd; }
}
function fillLimit(B, i, s, px, nmax) {
  for (let j = i + 1; j < Math.min(B.n, i + 1 + nmax); j++) if (s === 1 ? B.l[j] <= px : B.h[j] >= px) return j;
  return -1;
}
function comboList(P, m) {
  const sp = SPEC[m], k = sp.stop / 50;
  const E = (P.entries || ['market']), ST = [];
  for (const x of (P.fixed || [20, 40, 50, 60])) ST.push({ k: 'fixed', v: +x * k, name: 'fixed ' + (+(x * k).toFixed(2)) });
  for (const x of (P.stops || ['struct'])) {
    if (x === 'struct') ST.push({ k: 'struct', name: 'structure (swing / PO4)' });
    else if (x.startsWith('atr')) ST.push({ k: 'atr', v: +x.slice(3), name: 'ATR x' + x.slice(3) });
  }
  const T = (P.targets || [1, 2, 3, 4, 6, 'none']).map(x => x === 'none' ? nan : x === 'setup' ? 'setup' : +x);
  const X = (P.exits || ['st']);
  return { E, ST, T, X };
}
const EN = { market: 'market (signal close)', limit50: 'limit 50% of signal candle', limitOpen: 'limit signal open', limitLevel: 'limit at the level' };
const XN = { st: 'stop / target only', oppbc: 'out at the first opposite BC', sess: 'hold to next session open', flip: 'out at the next flip' };
const TN = t => t === 'setup' ? 'setup target' : isn(t) ? 'none' : '1:' + t;

function prepare(srcs, m, tf, P, onProgress) {
  const ctxs = [];
  for (const [sym, F] of srcs) {
    const B = bars(F, tf);
    if (B.n < 300) continue;
    const ctx = { F, B, m, sym, flip: flipRun(B, +P.c2pct || 50, .5, P.openChk !== false) };
    let DL = null, ZZ = null;
    ctx.levels = () => DL || (DL = dayLevels(F, m));
    ctx.zones = () => ZZ || (ZZ = zones(F, m, 30).concat(zones(F, m, 60)));
    // period per bar
    ctx.per = new Uint8Array(B.n);
    if (m === 'NQ') ctx.per.fill(sym === 'NQ' ? 0 : 1);
    else { const ds = [...new Set(Array.from(B.sd))].sort((a, b) => a - b), cut = ds[Math.floor(ds.length / 2)]; for (let i = 0; i < B.n; i++) ctx.per[i] = B.sd[i] < cut ? 0 : 1; }
    ctxs.push(ctx);
    if (onProgress) onProgress('Built ' + sym + ' ' + tf + 'm: ' + B.n.toLocaleString() + ' candles');
  }
  return ctxs;
}

function run(srcs, m, tf, P, onProgress) {
  const sp = SPEC[m], C = comboList(P, m), nE = C.E.length, nS = C.ST.length, nT = C.T.length, nX = C.X.length;
  const NC = nE * nS * nT * nX;
  const acc = new Float64Array(NC * 2 * 2 * 6);          // combo x period x (real, random) x [n, wins, sum, sumsq, pos, neg]
  const ctxs = prepare(srcs, m, tf, P, onProgress);
  const sigCount = [0, 0], found = [[], []];
  const R = new Float64Array(nT), Xb = new Int32Array(nT), RR = new Float64Array(nT), XR = new Int32Array(nT);
  for (const ctx of ctxs) {
    const B = ctx.B, en = ends(B, P.cap || 'day');
    let sig = signals(ctx, P); sig = applyFilters(ctx, sig, P);
    if (sig.I.length > 250000) throw new Error('Too many signals (' + sig.I.length.toLocaleString() + '). Add a filter or a time window.');
    if (onProgress) onProgress(ctx.sym + ': ' + sig.I.length.toLocaleString() + ' signals. Grading ' + NC + ' combos...');
    const masks = {};
    const oppMask = s => masks['o' + s] || (masks['o' + s] = Uint8Array.from(B.bc, b => b === -s ? 1 : 0));
    const flipMask = s => { if (masks['f' + s]) return masks['f' + s]; const a = new Uint8Array(B.n); const E = ctx.flip; for (let q = 0; q < E.eI.length; q++) if (E.eK[q] === 1 && E.eS[q] === -s) a[E.eI[q]] = 1; return (masks['f' + s] = a); };
    const rnd = rng32(1234 + tf);
    // random twin bars: same trading day, inside the filter window if one is set
    const dayIx = groupDays(B), pools = new Map();
    for (let q = 0; q < sig.I.length; q++) {
      const i = sig.I[q], s = sig.S[q], per = ctx.per[i]; if (i >= B.n - 2) continue;
      sigCount[per]++; found[per].push([i, s, ctx]);
      let pool = pools.get(B.sd[i]);
      if (!pool) { pool = dayIx.get(B.sd[i]); if (P.useWin) pool = pool.filter(j => inWin(B.mn[j], +P.winFrom, +P.winTo)); pool = pool.filter(j => j > 0 && j < B.n - 2); pools.set(B.sd[i], pool); }
      const rj = pool.length > 6 ? pool[Math.floor(rnd() * (pool.length - 5))] : i;
      for (let e = 0; e < nE; e++) {
        let fi, ep; const ek = C.E[e];
        if (ek === 'market') { fi = i; ep = B.c[i]; }
        else {
          const px = ek === 'limit50' ? (B.h[i] + B.l[i]) / 2 : ek === 'limitOpen' ? B.o[i] : sig.LV[q];
          if (!(px === px)) continue;
          fi = fillLimit(B, i, s, px, 10); if (fi < 0) continue;
          ep = (s === 1 && B.o[fi] < px) || (s === -1 && B.o[fi] > px) ? B.o[fi] : px;
        }
        for (let st = 0; st < nS; st++) {
          const S0 = C.ST[st]; let sl;
          if (S0.k === 'fixed') sl = ep - s * S0.v; else if (S0.k === 'struct') sl = sig.WK[q]; else sl = ep - s * S0.v * B.atr[i];
          const risk = s * (ep - sl);
          if (!(risk > .04 * sp.stop)) continue;
          const tpq = sig.TP[q], tpOk = tpq === tpq && s * (tpq - ep) > 0, tpR = tpOk ? s * (tpq - ep) / risk : nan;
          const tg = C.T.map(t => t === 'setup' ? (tpOk ? tpq : nan) : isn(t) ? nan : ep + s * t * risk), rtg = C.T.map(t => t === 'setup' ? (tpOk ? B.c[rj] + s * tpR * risk : nan) : isn(t) ? nan : B.c[rj] + s * t * risk);
          for (let x = 0; x < nX; x++) {
            const xk = C.X[x], cap = en.capEnd[fi];
            const jEnd = xk === 'sess' ? Math.min(en.segEnd[fi] === fi ? en.segEnd[Math.min(B.n - 1, fi + 1)] : en.segEnd[fi], cap) : cap;
            const mask = xk === 'oppbc' ? oppMask(s) : xk === 'flip' ? flipMask(s) : null;
            walk(B, fi, s, ep, sl, tg, Math.max(jEnd, fi), mask, sp.cost, R, Xb);
            const rcap = en.capEnd[rj], rjEnd = xk === 'sess' ? Math.min(en.segEnd[rj] === rj ? en.segEnd[Math.min(B.n - 1, rj + 1)] : en.segEnd[rj], rcap) : rcap;
            walk(B, rj, s, B.c[rj], B.c[rj] - s * risk, rtg, Math.max(rjEnd, rj + 1 < B.n ? rj + 1 : rj), mask, sp.cost, RR, XR);
            for (let t = 0; t < nT; t++) {
              if (C.T[t] === 'setup' && !tpOk) continue;
              const ci = ((e * nS + st) * nT + t) * nX + x;
              for (const [w, r] of [[0, R[t]], [1, RR[t]]]) {
                if (!(r === r)) continue;
                const b = ((ci * 2 + per) * 2 + w) * 6;
                acc[b] += 1; if (r > 0) { acc[b + 1] += 1; acc[b + 4] += r; } else acc[b + 5] -= r; acc[b + 2] += r; acc[b + 3] += r * r;
              }
            }
          }
        }
      }
    }
  }
  // stats
  const st6 = b => { const n = acc[b]; if (n < 2) return { n }; const av = acc[b + 2] / n, sd = Math.sqrt(Math.max(acc[b + 3] / n - av * av, 0) * n / (n - 1));
    return { n, wr: acc[b + 1] / n, avg: av, pf: acc[b + 5] > 0 ? acc[b + 4] / acc[b + 5] : null, t: sd > 0 ? av / sd * Math.sqrt(n) : null }; };
  const rows = [];
  for (let e = 0; e < nE; e++) for (let st = 0; st < nS; st++) for (let t = 0; t < nT; t++) for (let x = 0; x < nX; x++) {
    const ci = ((e * nS + st) * nT + t) * nX + x, r = { e: C.E[e], st: C.ST[st].name, stK: C.ST[st], t: C.T[t], x: C.X[x], key: [e, st, t, x] };
    for (let p = 0; p < 2; p++) { r['p' + p] = st6(((ci * 2 + p) * 2 + 0) * 6); r['r' + p] = st6(((ci * 2 + p) * 2 + 1) * 6); }
    if (r.p0.n || r.p1.n) rows.push(r);
  }
  const ok = r => r.p0.n >= 30 && r.p1.n >= 30;
  for (const r of rows) { r.pass = ok(r) && r.p0.t >= 2 && r.p1.t >= 2; r.rpass = ok(r) && r.r0.t >= 2 && r.r1.t >= 2; r.fixed12 = r.st.startsWith('fixed ' + (+sp.stop.toFixed(2))) && r.t === 2 && r.e === 'market' && r.x === 'st'; }
  // foundation
  const fnd = [0, 1].map(p => foundation(found[p]));
  return { rows, sigCount, fnd, combos: NC, tested: rows.filter(ok).length, passes: rows.filter(r => r.pass).length, rpasses: rows.filter(r => r.rpass).length,
    periods: ctxs.map(x => [x.sym, x.B.n, new Date(x.B.t[0] * 6e4).toISOString().slice(0, 10), new Date(x.B.t[x.B.n - 1] * 6e4).toISOString().slice(0, 10)]) };
}
function foundation(list) {
  let n = 0, a1 = 0, a2 = 0, p1 = 0, p5 = 0, p10 = 0, u5 = 0, n1 = 0, n5 = 0, n10 = 0;
  for (const [i, s, ctx] of list) {
    const { bc, c, n: N } = ctx.B; n++;
    let a = 0; for (let j = i + 1; j < Math.min(N, i + 500); j++) { if (bc[j] === -s) break; if (bc[j] === s) a++; } a1 += a;
    let z = 0; for (let j = i + 1; j < Math.min(N, i + 500); j++) { if (bc[j] === s) z++; else break; } a2 += z;
    if (i + 1 < N) { p1 += s * (c[i + 1] - c[i]); n1++; }
    if (i + 5 < N) { const d = s * (c[i + 5] - c[i]); p5 += d; n5++; if (d > 0) u5++; }
    if (i + 10 < N) { p10 += s * (c[i + 10] - c[i]); n10++; }
  }
  return { n, bcOpp: n ? a1 / n : null, bcNbc: n ? a2 / n : null, p1: n1 ? p1 / n1 : null, p5: n5 ? p5 / n5 : null, p10: n10 ? p10 / n10 : null, up5: n5 ? u5 / n5 : null };
}
/* trades for one combo (detail view) */
function tradesFor(srcs, m, tf, P, key) {
  const sp = SPEC[m], C = comboList(P, m), [e, st, t, x] = key, out = [];
  const ctxs = prepare(srcs, m, tf, P, null);
  const R = new Float64Array(1), Xb = new Int32Array(1), RR = new Float64Array(1), XR = new Int32Array(1);
  for (const ctx of ctxs) {
    const B = ctx.B, en = ends(B, P.cap || 'day');
    let sig = signals(ctx, P); sig = applyFilters(ctx, sig, P);
    const rnd = rng32(1234 + tf), dayIx = groupDays(B);
    const oppM = { 1: Uint8Array.from(B.bc, b => b === -1 ? 1 : 0), '-1': Uint8Array.from(B.bc, b => b === 1 ? 1 : 0) };
    const flM = {}; for (const s of [1, -1]) { const a = new Uint8Array(B.n); for (let q = 0; q < ctx.flip.eI.length; q++) if (ctx.flip.eK[q] === 1 && ctx.flip.eS[q] === -s) a[ctx.flip.eI[q]] = 1; flM[s] = a; }
    for (let q = 0; q < sig.I.length; q++) {
      const i = sig.I[q], s = sig.S[q]; if (i >= B.n - 2) continue;
      let pool = dayIx.get(B.sd[i]); if (P.useWin) pool = pool.filter(j => inWin(B.mn[j], +P.winFrom, +P.winTo));
      pool = pool.filter(j => j > 0 && j < B.n - 2);
      const rj = pool.length > 6 ? pool[Math.floor(rnd() * (pool.length - 5))] : i;
      let fi, ep; const ek = C.E[e];
      if (ek === 'market') { fi = i; ep = B.c[i]; }
      else { const px = ek === 'limit50' ? (B.h[i] + B.l[i]) / 2 : ek === 'limitOpen' ? B.o[i] : sig.LV[q]; if (!(px === px)) continue;
        fi = fillLimit(B, i, s, px, 10); if (fi < 0) continue; ep = (s === 1 && B.o[fi] < px) || (s === -1 && B.o[fi] > px) ? B.o[fi] : px; }
      const S0 = C.ST[st]; const sl = S0.k === 'fixed' ? ep - s * S0.v : S0.k === 'struct' ? sig.WK[q] : ep - s * S0.v * B.atr[i];
      const risk = s * (ep - sl); if (!(risk > .04 * sp.stop)) continue;
      let tt = C.T[t];
      if (tt === 'setup') { const tpq = sig.TP[q]; if (!(tpq === tpq && s * (tpq - ep) > 0)) continue; tt = s * (tpq - ep) / risk; }
      const xk = C.X[x], cap = en.capEnd[fi];
      const jEnd = xk === 'sess' ? Math.min(en.segEnd[fi] === fi ? en.segEnd[Math.min(B.n - 1, fi + 1)] : en.segEnd[fi], cap) : cap;
      const mask = xk === 'oppbc' ? oppM[s] : xk === 'flip' ? flM[s] : null;
      walk(B, fi, s, ep, sl, [isn(tt) ? nan : ep + s * tt * risk], Math.max(jEnd, fi), mask, sp.cost, R, Xb);
      out.push({ te: B.t[fi], tx: B.t[Xb[0]], sym: ctx.sym, per: ctx.per[i], s, ep, sl, tp: isn(tt) ? null : ep + s * tt * risk, risk, r: R[0], tag: sig.TAG[q] });
    }
  }
  out.sort((a, b) => a.te - b.te || a.tx - b.tx);
  return out;
}
/* money: one trade at a time, stop the day after N losses (counted when they close), $ per month, 50k evals */
function money(trades, riskUsd, maxLoss, oneAtATime) {
  const keep = [], los = new Map(); let busy = -Infinity;
  for (const T of trades) {
    const d = sdOf(T.te);
    if (oneAtATime && T.te < busy) continue;
    if (maxLoss > 0 && (los.get(d) || 0) >= maxLoss) continue;
    keep.push(T); busy = T.tx; if (T.r <= 0) los.set(d, (los.get(d) || 0) + 1);
  }
  const per = [0, 1].map(p => {
    const A = keep.filter(T => T.per === p), mo = new Map();
    for (const T of A) { const k = new Date(T.te * 6e4).toISOString().slice(0, 7); mo.set(k, (mo.get(k) || 0) + T.r * riskUsd); }
    const vals = [...mo.values()];
    const props = prop50(A, riskUsd);
    return { trades: A.length, months: vals.length, perMonth: vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : null,
      best: vals.length ? Math.max(...vals) : null, worst: vals.length ? Math.min(...vals) : null, green: vals.length ? vals.filter(v => v > 0).length / vals.length : null,
      monthly: [...mo.entries()], evals: props.length, passed: props.filter(x => x === 'pass').length };
  });
  return { kept: keep, per };
}
function prop50(A, riskUsd, target = 3000, trail = 2000, dloss = 1000) {
  const res = [], months = [...new Set(A.map(T => new Date(T.te * 6e4).toISOString().slice(0, 7)))];
  for (const mo of months) {
    const start = A.find(T => new Date(T.te * 6e4).toISOString().slice(0, 7) === mo).te;
    let bal = 0, peak = 0, out = 'open', day = null, dsum = 0;
    const S = A.filter(T => T.te >= start);
    for (let k = 0; k < S.length; k++) {
      const d = new Date(S[k].te * 6e4).toISOString().slice(0, 10);
      if (d !== day) { if (day !== null) { peak = Math.max(peak, bal); if (bal <= peak - trail) { out = 'fail'; break; } } day = d; dsum = 0; }
      if (dsum <= -dloss) continue;
      const u = S[k].r * riskUsd; dsum += u; bal += u;
      if (bal >= target) { out = 'pass'; break; }
    }
    if (out === 'open' && day !== null) { peak = Math.max(peak, bal); if (bal <= peak - trail) out = 'fail'; }
    res.push(out);
  }
  return res;
}

const API = { SPEC, MK, KN, EN, XN, TN, decode, bars, flipRun, dayLevels, zones, signals, applyFilters, run, tradesFor, money, vp };
if (typeof module !== 'undefined' && module.exports) module.exports = API;
G.MMM = API;

/* ---------- worker glue ---------- */
if (typeof importScripts === 'function' && typeof document === 'undefined') {
  const cache = {};
  async function load(sym) {
    if (cache[sym]) return cache[sym];
    const r = await fetch('data/' + sym + '.bin.gz'); if (!r.ok) throw new Error('No data file for ' + sym);
    let ab = await r.arrayBuffer();
    const u = new Uint8Array(ab, 0, 2);
    if (u[0] === 0x1f && u[1] === 0x8b) ab = await new Response(new Blob([ab]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer();
    return (cache[sym] = decode(new Int32Array(ab)));
  }
  self.onmessage = async ev => {
    const { id, cmd, m, tf, P, key } = ev.data;
    try {
      const prog = msg => self.postMessage({ id, prog: msg });
      prog('Loading ' + MK[m].join(' + ') + ' data...');
      const srcs = []; for (const s of MK[m]) { try { srcs.push([s, await load(s)]); } catch (e) { } }
      if (!srcs.length) throw new Error('No data for ' + m);
      if (cmd === 'run') { const t0 = Date.now(); const R = run(srcs, m, tf, P, prog); R.ms = Date.now() - t0; for (const r of R.rows) delete r.stK; self.postMessage({ id, done: R }); }
      else if (cmd === 'trades') { const T = tradesFor(srcs, m, tf, P, key); const M = money(T, +P.riskUsd || 200, +P.maxLoss, P.oneAtATime !== false); self.postMessage({ id, done: { trades: T, money: { per: M.per, keptN: M.kept.length } } }); }
    } catch (e) { self.postMessage({ id, err: e.message || String(e) }); }
  };
}
})(typeof self !== 'undefined' ? self : globalThis);
