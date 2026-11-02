"""Bar-by-bar replica of 'MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.0' (default inputs).

Generates the SAME setups the indicator creates (entry, stop, target, bar, entry type) on closed bars.
Defaults copied from the script:
  wait_for_close on, MMPD / trend filters off, cycle limit off, SL = Box H/L (sl_use_box), SL buffer 4 ticks,
  RR 2.0, Fixed Risk $ = 4500 / 20 = $225, skip if $ risk > 225 * 1.05, entry point Open for BuX/BeX and LQG,
  LQG stop = entry candle H/L, vp_bins 20, VP lookback 200, max_swings 100, trade expiry 500 bars.
Only difference: the script processes only the last 500 bars ('Limit Historical Bars'); this runs every bar.
"""
import numpy as np, math

TICK = 0.25
RR = 2.0
RISK = 4500.0 / 20.0
BUF = 4 * TICK
VP_BINS = 20
VP_LB = 200
MAX_SW = 100


class S:  # generic structure record
    __slots__ = ('kind', 'is_bull', 'sl_drawn', 'nbc_high', 'nbc_low', 'break_bar', 'origin_bar', 'swing_price',
                 'cb_violated', 'cb_poc', 'cb_mid', 'poc_touched', 'poc_taken', 'blk_touched', 'blk_taken',
                 'fva_top', 'fva_bot', 'fva_filled', 'sl_violated', 'poc_deleted', 'is_sig', 'sig_state',
                 'grey', 'has_swing_line', 'is_nested', 'creation_bar', 'del_level', 'is_violated', 'bch', 'bcl', 'rej_done')

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


def volume_profile(o, h, l, c, v, i, swingH, swingL, lb):
    """calcVolumeProfile(swingH, swingL, barsBackStart=lb, barsBackEnd=0) -> POC price (or nan)."""
    if not (swingH > swingL) or lb < 0:
        return np.nan
    bins = VP_BINS
    step = max((swingH - swingL) / bins, TICK)
    levels = swingL + np.arange(bins) * step
    vols = np.zeros(bins)
    safe = min(VP_LB, lb)
    for k in range(0, safe + 1):
        j = i - k
        if j < 0:
            break
        cH, cL, cV = h[j], l[j], v[j]
        if cV > 0 and cH >= swingL and cL <= swingH:
            pr = max(cH - cL, TICK)
            # binary_search_rightmost(levels, cL - step) / leftmost(levels, cH + step), clipped
            sB = max(0, int(np.searchsorted(levels, cL - step, side='right')) - 1)
            eB = min(bins - 1, int(np.searchsorted(levels, cH + step, side='left')))
            for b in range(sB, eB + 1):
                bb = levels[b]; bt = bb + step
                if cH >= bb and cL <= bt:
                    oF = (min(cH, bt) - max(cL, bb)) / pr
                    if oF > 0:
                        vols[b] += cV * oF
    mx = vols.max()
    if mx <= 0:
        return np.nan
    p = int(np.argmax(vols))  # first max, like the script's strict '>' scan
    return swingL + p * step + step / 2


def make_trade(is_long, ep, sl_in, etype, i, t, pv):
    sl = sl_in
    rp = math.floor(abs(ep - sl) / TICK + 0.5) * TICK
    if rp < 4 * TICK:
        rp = 4 * TICK
        sl = ep - rp if is_long else ep + rp
    tp = ep + rp * RR if is_long else ep - rp * RR
    if is_long and (sl >= ep or tp <= ep):
        return None
    if (not is_long) and (sl <= ep or tp >= ep):
        return None
    ps = int(max(1, math.floor(RISK / max(rp * pv, TICK) + 0.5)))
    arisk = rp * pv * ps
    if arisk > RISK * 1.05:
        return None
    return dict(long=is_long, ep=ep, sl=sl, tp=tp, rp=rp, ps=ps, arisk=arisk, etype=etype, i=i, t=t)


def category(etype):
    if 'Nested' in etype and 'PES/PEL' in etype:
        return 'Nest PES/PEL(+)'
    if 'Nested' in etype and 'CDL/CDS' in etype:
        return 'Nest CDL/CDS(+)'
    for k, n in (('①', 'PES/PEL'), ('②', 'PES/PEL+'), ('③', 'CDL/CDS'), ('④', 'CDL/CDS+'), ('⑤', 'BuX/BeX'), ('⑥', 'LQG Brk')):
        if k in etype:
            return n
    return '?'


def run(df, pv=2.0):
    o = df.open.values; h = df.high.values; l = df.low.values; c = df.close.values; v = df.volume.values
    tm = df.index
    n = len(df)
    bulls, bears, pes = [], [], []
    trades = []
    state = -999  # 0 NBC, 1 BULL, -1 BEAR
    run_top = run_bot = run_high = run_low = np.nan
    start_bar = None
    last_nbc_high = last_nbc_low = np.nan; last_nbc_bar = None
    last_bc_high = last_bc_low = last_bc_open = last_bc_close = np.nan; last_bc_bar = None
    rsl = rsh = np.nan; rsl_bar = rsh_bar = None
    last_bc_dir = 0
    lqg_bull_pending = lqg_bear_pending = False
    lqg_bull_count = lqg_bear_count = 0
    cur_nested = False; par_start = None; par_high = par_low = np.nan

    def add(tr):
        if tr is not None:
            trades.append(tr)

    def rec(lg, ep, slbox, et, i, swing, tgt, mkt=False):
        trades.append(dict(long=lg, ep=ep, sl=slbox, swing=swing, tgt=tgt, etype=et, i=i, t=tm[i], mkt=mkt))

    for i in range(n):
        if i < 2:
            # need high[1], high[2]
            if i == 0:
                continue
        is_bux = c[i] > h[i - 1]
        is_bex = c[i] < l[i - 1]
        is_nbc = not is_bux and not is_bex
        if i >= 2:
            if l[i - 1] < l[i - 2] and l[i - 1] < l[i]:
                rsl = l[i - 1]; rsl_bar = i - 1
            if h[i - 1] > h[i - 2] and h[i - 1] > h[i]:
                rsh = h[i - 1]; rsh_bar = i - 1

        # 2. nested FVA detection
        if is_nbc:
            cur_nested = False
            for s in reversed(bulls):
                if not s.cb_violated and not s.is_sig and s.fva_bot <= c[i] <= s.fva_top:
                    s.is_sig = True; s.sig_state = 0; cur_nested = True
                    par_start = s.origin_bar; par_high = s.fva_top; par_low = s.fva_bot
            if not cur_nested:
                for s in reversed(bears):
                    if not s.cb_violated and not s.is_sig and s.fva_bot <= c[i] <= s.fva_top:
                        s.is_sig = True; s.sig_state = 0; cur_nested = True
                        par_start = s.origin_bar; par_high = s.fva_top; par_low = s.fva_bot
            if not cur_nested:
                for s in reversed(pes):
                    if not s.is_violated and not s.is_sig and s.fva_bot <= c[i] <= s.fva_top:
                        s.is_sig = True; s.sig_state = 0; cur_nested = True
                        par_start = s.creation_bar; par_high = s.fva_top; par_low = s.fva_bot

        # 3a. bull structures
        for idx in range(len(bulls) - 1, -1, -1):
            s = bulls[idx]
            if s.kind == 'cdl' and not s.rej_done and i > s.break_bar and not s.cb_violated and l[i] <= s.fva_top:
                s.rej_done = True
                if c[i] > s.fva_top:
                    rec(True, c[i], s.fva_bot - BUF, 'Rej FVA', i, s.swing_price - BUF, s.bch, True)
            if i > s.break_bar and not np.isnan(s.swing_price) and l[i] <= s.swing_price and not s.sl_violated:
                s.sl_violated = True
                if c[i] < s.swing_price:
                    lqg_bull_pending = False; lqg_bull_count = 0
            if not s.fva_filled and i > s.break_bar and l[i] <= s.fva_bot:
                s.fva_filled = True
            if s.fva_filled and not s.cb_violated and not s.is_sig:
                if s.grey == 0 and c[i] > s.fva_top: s.grey = 1
                elif s.grey == 1 and l[i] <= s.fva_top: s.grey = 2
                elif s.grey == 2 and c[i] > s.fva_top:
                    s.grey = 3
                    if s.kind == 'cdl': rec(True, c[i], s.fva_bot - BUF, 'G3 FVA', i, s.swing_price - BUF, s.bch, True)
            if s.is_sig and s.sig_state == 0:
                if c[i] > s.fva_top:
                    s.sig_state = 1
                    if s.kind in ('cdl', 'cds'): rec(True, c[i], s.fva_bot - BUF, 'Sig FVA', i, (rsl - BUF) if not np.isnan(rsl) else np.nan, np.nan, True)
                elif c[i] < s.fva_bot:
                    s.sig_state = -1
                    if s.kind in ('cdl', 'cds'): rec(False, c[i], s.fva_top + BUF, 'Sig FVA', i, (rsh + BUF) if not np.isnan(rsh) else np.nan, np.nan, True)
            if s.is_sig:
                brk = (s.sig_state == 1 and c[i] < s.fva_bot) or (s.sig_state == -1 and c[i] > s.fva_top)
            else:
                brk = (not s.cb_violated) and c[i] < s.fva_bot
            if brk and not s.cb_violated and s.kind == 'cdl':
                rec(False, c[i], s.fva_top + BUF, '⑦ Fail', i, (rsh + BUF) if not np.isnan(rsh) else np.nan, np.nan, True)
                if c[i] < s.fva_bot:
                    rec(False, c[i], s.fva_top + BUF, 'FailC', i, (rsh + BUF) if not np.isnan(rsh) else np.nan, np.nan, True)
                    rec(False, s.fva_bot, s.fva_top + BUF, 'FailC RT', i, (rsh + BUF) if not np.isnan(rsh) else np.nan, np.nan, False)
            if brk:
                s.cb_violated = True
                if not s.has_swing_line and not s.sl_violated:
                    s.sl_violated = True
            if s.sl_violated and s.cb_violated and s.poc_deleted:
                del bulls[idx]; continue
            if not s.cb_violated and l[i] < s.nbc_low and c[i] >= s.nbc_low:
                lqg_bull_pending = True; lqg_bull_count += 1
            if not s.poc_deleted:
                if not np.isnan(s.cb_poc) and l[i] <= s.cb_poc:
                    s.poc_touched = True; s.poc_deleted = True
            nest = s.is_nested
            if not np.isnan(s.cb_poc) and not s.poc_taken and l[i] <= s.cb_poc:
                s.poc_taken = True
                rec(True, s.cb_poc, s.fva_bot - BUF, '① Nested PES/PEL' if nest else '① PES/PEL', i, s.swing_price - BUF, s.bch)
            if not np.isnan(s.cb_mid):
                if l[i] <= s.cb_mid: s.blk_touched = True
                if not s.blk_taken and l[i] <= s.cb_mid:
                    s.blk_taken = True
                    rec(True, s.cb_mid, s.fva_bot - BUF, '③ Nested CDL/CDS' if nest else '③ CDL/CDS', i, s.swing_price - BUF, s.bch)

        # 3b. bear structures
        for idx in range(len(bears) - 1, -1, -1):
            s = bears[idx]
            if s.kind == 'cds' and not s.rej_done and i > s.break_bar and not s.cb_violated and h[i] >= s.fva_bot:
                s.rej_done = True
                if c[i] < s.fva_bot:
                    rec(False, c[i], s.fva_top + BUF, 'Rej FVA', i, s.swing_price + BUF, s.bcl, True)
            if i > s.break_bar and not np.isnan(s.swing_price) and h[i] >= s.swing_price and not s.sl_violated:
                s.sl_violated = True
                if c[i] > s.swing_price:
                    lqg_bear_pending = False; lqg_bear_count = 0
            if not s.fva_filled and i > s.break_bar and h[i] >= s.fva_top:
                s.fva_filled = True
            if s.fva_filled and not s.cb_violated and not s.is_sig:
                if s.grey == 0 and c[i] < s.fva_bot: s.grey = 1
                elif s.grey == 1 and h[i] >= s.fva_bot: s.grey = 2
                elif s.grey == 2 and c[i] < s.fva_bot:
                    s.grey = 3
                    if s.kind == 'cds': rec(False, c[i], s.fva_top + BUF, 'G3 FVA', i, s.swing_price + BUF, s.bcl, True)
            if s.is_sig and s.sig_state == 0:
                if c[i] > s.fva_top:
                    s.sig_state = 1
                    if s.kind in ('cdl', 'cds'): rec(True, c[i], s.fva_bot - BUF, 'Sig FVA', i, (rsl - BUF) if not np.isnan(rsl) else np.nan, np.nan, True)
                elif c[i] < s.fva_bot:
                    s.sig_state = -1
                    if s.kind in ('cdl', 'cds'): rec(False, c[i], s.fva_top + BUF, 'Sig FVA', i, (rsh + BUF) if not np.isnan(rsh) else np.nan, np.nan, True)
            if s.is_sig:
                brk = (s.sig_state == 1 and c[i] < s.fva_bot) or (s.sig_state == -1 and c[i] > s.fva_top)
            else:
                brk = (not s.cb_violated) and c[i] > s.fva_top
            if brk and not s.cb_violated and s.kind == 'cds':
                rec(True, c[i], s.fva_bot - BUF, '⑦ Fail', i, (rsl - BUF) if not np.isnan(rsl) else np.nan, np.nan, True)
                if c[i] > s.fva_top:
                    rec(True, c[i], s.fva_bot - BUF, 'FailC', i, (rsl - BUF) if not np.isnan(rsl) else np.nan, np.nan, True)
                    rec(True, s.fva_top, s.fva_bot - BUF, 'FailC RT', i, (rsl - BUF) if not np.isnan(rsl) else np.nan, np.nan, False)
            if brk:
                s.cb_violated = True
                if not s.has_swing_line and not s.sl_violated:
                    s.sl_violated = True
            if s.sl_violated and s.cb_violated and s.poc_deleted:
                del bears[idx]; continue
            if not s.cb_violated and h[i] > s.nbc_high and c[i] <= s.nbc_high:
                lqg_bear_pending = True; lqg_bear_count += 1
            if not s.poc_deleted:
                if not np.isnan(s.cb_poc) and h[i] >= s.cb_poc:
                    s.poc_touched = True; s.poc_deleted = True
            nest = s.is_nested
            if not np.isnan(s.cb_poc) and not s.poc_taken and h[i] >= s.cb_poc:
                s.poc_taken = True
                rec(False, s.cb_poc, s.fva_top + BUF, '① Nested PES/PEL' if nest else '① PES/PEL', i, s.swing_price + BUF, s.bcl)
            if not np.isnan(s.cb_mid):
                if h[i] >= s.cb_mid: s.blk_touched = True
                if not s.blk_taken and h[i] >= s.cb_mid:
                    s.blk_taken = True
                    rec(False, s.cb_mid, s.fva_top + BUF, '③ Nested CDL/CDS' if nest else '③ CDL/CDS', i, s.swing_price + BUF, s.bcl)

        # 5. PE boxes (②④)
        for idx in range(len(pes) - 1, -1, -1):
            p = pes[idx]
            if not p.rej_done and i > p.creation_bar and not p.is_violated:
                if p.is_bull and l[i] <= p.fva_top:
                    p.rej_done = True
                    if c[i] > p.fva_top:
                        rec(True, c[i], p.fva_bot - BUF, 'Rej Zone', i, p.del_level - BUF, p.bch, True)
                elif (not p.is_bull) and h[i] >= p.fva_bot:
                    p.rej_done = True
                    if c[i] < p.fva_bot:
                        rec(False, c[i], p.fva_top + BUF, 'Rej Zone', i, p.del_level + BUF, p.bcl, True)
            if p.is_bull:
                sl_touch = not np.isnan(p.del_level) and l[i] <= p.del_level
            else:
                sl_touch = not np.isnan(p.del_level) and h[i] >= p.del_level
            if sl_touch and not p.sl_violated:
                p.sl_violated = True
            if not p.fva_filled and i > p.creation_bar:
                if p.is_bull and l[i] <= p.fva_bot: p.fva_filled = True
                elif (not p.is_bull) and h[i] >= p.fva_top: p.fva_filled = True
            if p.fva_filled and not p.is_violated and not p.is_sig:
                if p.is_bull:
                    if p.grey == 0 and c[i] > p.fva_top: p.grey = 1
                    elif p.grey == 1 and l[i] <= p.fva_top: p.grey = 2
                    elif p.grey == 2 and c[i] > p.fva_top:
                        p.grey = 3
                        rec(True, c[i], p.fva_bot - BUF, 'G3 Zone', i, p.del_level - BUF, p.bch, True)
                else:
                    if p.grey == 0 and c[i] < p.fva_bot: p.grey = 1
                    elif p.grey == 1 and h[i] >= p.fva_bot: p.grey = 2
                    elif p.grey == 2 and c[i] < p.fva_bot:
                        p.grey = 3
                        rec(False, c[i], p.fva_top + BUF, 'G3 Zone', i, p.del_level + BUF, p.bcl, True)
            if p.is_sig and p.sig_state == 0:
                if c[i] > p.fva_top:
                    p.sig_state = 1
                    rec(True, c[i], p.fva_bot - BUF, 'Sig Zone', i, (rsl - BUF) if not np.isnan(rsl) else np.nan, np.nan, True)
                elif c[i] < p.fva_bot:
                    p.sig_state = -1
                    rec(False, c[i], p.fva_top + BUF, 'Sig Zone', i, (rsh + BUF) if not np.isnan(rsh) else np.nan, np.nan, True)
            if p.is_sig:
                inv = (p.sig_state == 1 and c[i] < p.fva_bot) or (p.sig_state == -1 and c[i] > p.fva_top)
            else:
                inv = (p.is_bull and c[i] < p.fva_bot) or ((not p.is_bull) and c[i] > p.fva_top)
            if inv and not p.is_violated:
                if p.is_bull:
                    rec(False, c[i], p.fva_top + BUF, '⑦ Fail+', i, (rsh + BUF) if not np.isnan(rsh) else np.nan, np.nan, True)
                    if c[i] < p.fva_bot:
                        rec(False, c[i], p.fva_top + BUF, 'Fail+C', i, (rsh + BUF) if not np.isnan(rsh) else np.nan, np.nan, True)
                        rec(False, p.fva_bot, p.fva_top + BUF, 'Fail+C RT', i, (rsh + BUF) if not np.isnan(rsh) else np.nan, np.nan, False)
                else:
                    rec(True, c[i], p.fva_bot - BUF, '⑦ Fail+', i, (rsl - BUF) if not np.isnan(rsl) else np.nan, np.nan, True)
                    if c[i] > p.fva_top:
                        rec(True, c[i], p.fva_bot - BUF, 'Fail+C', i, (rsl - BUF) if not np.isnan(rsl) else np.nan, np.nan, True)
                        rec(True, p.fva_top, p.fva_bot - BUF, 'Fail+C RT', i, (rsl - BUF) if not np.isnan(rsl) else np.nan, np.nan, False)
                p.is_violated = True
                if not p.has_swing_line and not p.sl_violated:
                    p.sl_violated = True
            if not p.poc_deleted:
                if p.is_bull and not np.isnan(p.cb_poc) and l[i] <= p.cb_poc:
                    p.poc_touched = True
                elif (not p.is_bull) and not np.isnan(p.cb_poc) and h[i] >= p.cb_poc:
                    p.poc_touched = True
                if p.poc_touched:
                    p.poc_deleted = True
            if p.sl_violated and p.is_violated and p.poc_deleted:
                del pes[idx]; continue
            nest = p.is_nested
            if p.is_bull and not p.is_violated:
                if not p.poc_taken and p.poc_touched:
                    p.poc_taken = True
                    rec(True, p.cb_poc, p.fva_bot - BUF, '② Nested PES/PEL+' if nest else '② PES/PEL+', i, p.del_level - BUF, p.bch)
                if l[i] <= p.fva_top: p.blk_touched = True
                if not p.blk_taken and l[i] <= p.fva_top:
                    p.blk_taken = True
                    rec(True, p.fva_top, p.fva_bot - BUF, '④ Nested CDL/CDS+' if nest else '④ CDL/CDS+', i, p.del_level - BUF, p.bch)
            elif (not p.is_bull) and not p.is_violated:
                if not p.poc_taken and p.poc_touched:
                    p.poc_taken = True
                    rec(False, p.cb_poc, p.fva_top + BUF, '② Nested PES/PEL+' if nest else '② PES/PEL+', i, p.del_level + BUF, p.bcl)
                if h[i] >= p.fva_bot: p.blk_touched = True
                if not p.blk_taken and h[i] >= p.fva_bot:
                    p.blk_taken = True
                    rec(False, p.fva_bot, p.fva_top + BUF, '④ Nested CDL/CDS+' if nest else '④ CDL/CDS+', i, p.del_level + BUF, p.bcl)

        # 6. LQG break entries
        if lqg_bull_pending and is_bux:
            lqg_bull_pending = False; lqg_bull_count = 0
            ep = o[i]; sl = l[i]
            if sl >= ep: sl = l[i]
            rec(True, ep, sl - BUF, '⑥ LQG', i, rsl - BUF, np.nan, True)
        if lqg_bear_pending and is_bex:
            lqg_bear_pending = False; lqg_bear_count = 0
            ep = o[i]; sl = h[i]
            if sl <= ep: sl = h[i]
            rec(False, ep, sl + BUF, '⑥ LQG', i, rsh + BUF, np.nan, True)
        if lqg_bull_count >= 2: lqg_bull_count = 0
        if lqg_bear_count >= 2: lqg_bear_count = 0

        # 8. state machine
        if is_nbc and state in (1, -1, -999):
            run_top = max(o[i], c[i]); run_bot = min(o[i], c[i]); run_high = h[i]; run_low = l[i]
            start_bar = i; last_nbc_high = h[i]; last_nbc_low = l[i]; last_nbc_bar = i; state = 0
        elif state == 0:
            if is_bux and c[i] > last_nbc_high:
                first = last_bc_dir != 1
                slp, slb = (rsl, rsl_bar) if not np.isnan(rsl) else (l[i], i)
                slEx = any(s.swing_price == slp and s.sl_drawn for s in bulls)
                sl_drawn = (not slEx) and first          # CDL SL line on; LD SL line off by default
                if cur_nested:
                    vps, vpH, vpL = par_start, max(run_high, par_high), min(run_low, par_low)
                else:
                    vps, vpH, vpL = start_bar, max(run_high, h[i]), min(run_low, l[i])
                poc = volume_profile(o, h, l, c, v, i, vpH, vpL, min(i - vps, VP_LB))
                mid = (run_top + run_bot) / 2
                bulls.append(S(kind='cdl', bch=h[i], bcl=l[i], is_bull=True, sl_drawn=sl_drawn, nbc_high=last_nbc_high, nbc_low=last_nbc_low,
                               break_bar=i, origin_bar=slb, swing_price=slp, cb_violated=False, cb_poc=poc, cb_mid=mid,
                               poc_touched=False, poc_taken=False, blk_touched=False, blk_taken=False,
                               fva_top=run_top, fva_bot=run_bot, fva_filled=False, sl_violated=False, poc_deleted=False,
                               is_sig=False, sig_state=0, grey=0, has_swing_line=not slEx, is_nested=cur_nested))
                rec(True, o[i], run_bot - BUF, '⑤ BuX', i, slp - BUF, np.nan, True)
                rec(True, c[i], run_bot - BUF, 'BrkBC', i, slp - BUF, np.nan, True)
                state = 1; last_bc_dir = 1
                last_bc_high, last_bc_low, last_bc_open, last_bc_close, last_bc_bar = h[i], l[i], o[i], c[i], i
            elif is_bex and c[i] < last_nbc_low:
                first = last_bc_dir != -1
                shp, shb = (rsh, rsh_bar) if not np.isnan(rsh) else (h[i], i)
                shEx = any(s.swing_price == shp and s.sl_drawn for s in bears)
                sl_drawn = (not shEx) and first
                if cur_nested:
                    vps, vpH, vpL = par_start, max(run_high, par_high), min(run_low, par_low)
                else:
                    vps, vpH, vpL = start_bar, max(run_high, h[i]), min(run_low, l[i])
                poc = volume_profile(o, h, l, c, v, i, vpH, vpL, min(i - vps, VP_LB))
                mid = (run_top + run_bot) / 2
                bears.append(S(kind='cds', bch=h[i], bcl=l[i], is_bull=False, sl_drawn=sl_drawn, nbc_high=last_nbc_high, nbc_low=last_nbc_low,
                               break_bar=i, origin_bar=shb, swing_price=shp, cb_violated=False, cb_poc=poc, cb_mid=mid,
                               poc_touched=False, poc_taken=False, blk_touched=False, blk_taken=False,
                               fva_top=run_top, fva_bot=run_bot, fva_filled=False, sl_violated=False, poc_deleted=False,
                               is_sig=False, sig_state=0, grey=0, has_swing_line=not shEx, is_nested=cur_nested))
                rec(False, o[i], run_top + BUF, '⑤ BeX', i, shp + BUF, np.nan, True)
                rec(False, c[i], run_top + BUF, 'BrkBC', i, shp + BUF, np.nan, True)
                state = -1; last_bc_dir = -1
                last_bc_high, last_bc_low, last_bc_open, last_bc_close, last_bc_bar = h[i], l[i], o[i], c[i], i
            elif is_nbc:
                if h[i] > run_high: run_high = h[i]; last_nbc_bar = i
                if l[i] < run_low: run_low = l[i]; last_nbc_bar = i
                run_top = max(run_top, o[i], c[i]); run_bot = min(run_bot, o[i], c[i])
                last_nbc_high = h[i]; last_nbc_low = l[i]
        elif is_bux:
            if state == -1:
                pelT = max(last_bc_open, last_bc_close); pelB = min(last_bc_open, last_bc_close)
                vps, vpH, vpL = last_bc_bar, max(last_bc_high, h[i]), min(last_bc_low, l[i])
                fn = False
                for b in bears:
                    if b.break_bar == last_bc_bar:
                        if b.is_nested or b.grey >= 3:
                            vps = b.origin_bar; vpH = max(b.fva_top, vpH); vpL = min(b.fva_bot, vpL); fn = True
                        break
                poc = volume_profile(o, h, l, c, v, i, vpH, vpL, min(i - vps, VP_LB))
                slp, slb = (rsl, rsl_bar) if not np.isnan(rsl) else (l[i], i)
                slEx = any(s.swing_price == slp and s.sl_drawn for s in bulls)
                pes.append(S(kind='pel', bch=h[i], bcl=l[i], is_bull=True, del_level=slp, is_violated=False, cb_poc=poc, poc_touched=False,
                             poc_taken=False, blk_touched=False, blk_taken=False, fva_top=pelT, fva_bot=pelB,
                             fva_filled=False, sl_violated=False, creation_bar=i, poc_deleted=False, is_sig=False,
                             sig_state=0, grey=0, has_swing_line=not slEx, is_nested=fn))
                bulls.append(S(kind='flip', is_bull=True, sl_drawn=not slEx, nbc_high=last_bc_high, nbc_low=last_bc_low,
                               break_bar=i, origin_bar=i - 1, swing_price=slp, cb_violated=False, cb_poc=np.nan,
                               cb_mid=np.nan, poc_touched=False, poc_taken=False, blk_touched=False, blk_taken=False,
                               fva_top=pelT, fva_bot=pelB, fva_filled=False, sl_violated=False, poc_deleted=False,
                               is_sig=False, sig_state=0, grey=0, has_swing_line=not slEx, is_nested=fn))
                rec(True, o[i], pelB - BUF, '⑤ BuX', i, slp - BUF, np.nan, True)
                rec(True, c[i], pelB - BUF, 'FlipBC', i, slp - BUF, np.nan, True)
            state = 1; last_bc_dir = 1
            last_bc_high, last_bc_low, last_bc_open, last_bc_close, last_bc_bar = h[i], l[i], o[i], c[i], i
        elif is_bex:
            if state == 1:
                pesT = max(last_bc_open, last_bc_close); pesB = min(last_bc_open, last_bc_close)
                vps, vpH, vpL = last_bc_bar, max(last_bc_high, h[i]), min(last_bc_low, l[i])
                fn = False
                for b in bulls:
                    if b.break_bar == last_bc_bar:
                        if b.is_nested or b.grey >= 3:
                            vps = b.origin_bar; vpH = max(b.fva_top, vpH); vpL = min(b.fva_bot, vpL); fn = True
                        break
                poc = volume_profile(o, h, l, c, v, i, vpH, vpL, min(i - vps, VP_LB))
                shp, shb = (rsh, rsh_bar) if not np.isnan(rsh) else (h[i], i)
                shEx = any(s.swing_price == shp and s.sl_drawn for s in bears)
                pes.append(S(kind='pes', bch=h[i], bcl=l[i], is_bull=False, del_level=shp, is_violated=False, cb_poc=poc, poc_touched=False,
                             poc_taken=False, blk_touched=False, blk_taken=False, fva_top=pesT, fva_bot=pesB,
                             fva_filled=False, sl_violated=False, creation_bar=i, poc_deleted=False, is_sig=False,
                             sig_state=0, grey=0, has_swing_line=not shEx, is_nested=fn))
                bears.append(S(kind='flip', is_bull=False, sl_drawn=not shEx, nbc_high=last_bc_high, nbc_low=last_bc_low,
                               break_bar=i, origin_bar=i - 1, swing_price=shp, cb_violated=False, cb_poc=np.nan,
                               cb_mid=np.nan, poc_touched=False, poc_taken=False, blk_touched=False, blk_taken=False,
                               fva_top=pesT, fva_bot=pesB, fva_filled=False, sl_violated=False, poc_deleted=False,
                               is_sig=False, sig_state=0, grey=0, has_swing_line=not shEx, is_nested=fn))
                rec(False, o[i], pesT + BUF, '⑤ BeX', i, shp + BUF, np.nan, True)
                rec(False, c[i], pesT + BUF, 'FlipBC', i, shp + BUF, np.nan, True)
            state = -1; last_bc_dir = -1
            last_bc_high, last_bc_low, last_bc_open, last_bc_close, last_bc_bar = h[i], l[i], o[i], c[i], i

        while len(bulls) > MAX_SW: bulls.pop(0)
        while len(bears) > MAX_SW: bears.pop(0)
        while len(pes) > MAX_SW: pes.pop(0)
    return trades
