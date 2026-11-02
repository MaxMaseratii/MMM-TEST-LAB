import sys
src = open('/home/claude/v36/concepts_template.pine').read()
def rep(old, new, count=1):
    global src
    c = src.count(old)
    if c != count:
        print("FAIL", c, old[:300]); sys.exit(1)
    src = src.replace(old, new)
def between(start, end, new):
    global src
    i0 = src.find(start); assert i0 >= 0, start[:60]
    i1 = src.find(end, i0 + len(start)); assert i1 > i0, end[:60]
    src = src[:i0] + new + src[i1:]

rep('indicator("MMM Concepts Pro+ @MaxMaserati 3.6", "MMM Concepts Pro+ 3.6"', 'indicator("MMM Concepts Pro+ @MaxMaserati 3.7", "MMM Concepts Pro+ 3.7"')
rep('// MMM CONCEPTS PRO+ 3.6', '// MMM CONCEPTS PRO+ 3.7')
rep('''//  P#    = the FIRST box after T# = the pullback start (bull: its high,
//          bear: its low). We trade between T# and P#.
//  R#    = the first box after the P# box ended = the resumption base
//          (bull: its low, bear: its high). A close back through it erases it.''',
'''//  P#    = the FIRST box after T# = the pullback start (bull: its high =
//          BeP#x, bear: its low = BuP#x). We trade between T# and P#.
//  R#    = the first box after the P# box ended = the resumption base
//          (bull: its low = BuR#x, bear: its high = BeR#x). A close back
//          through it erases it.''')
rep('''//  Block TF data = last CLOSED block candle only. No repaint.''',
'''//  Structure TF data = last CLOSED structure candle only. No repaint.
//  MAX ITEMS: everything between the highest and lowest 🟢🟩🔴🟥 marker is
//  always drawn; outside it only "Max Items" (50 / 50 bull / bear, a PO4 +
//  its break + its zone = ONE). 0 = nothing outside.''')

# inputs: TF module replaces the block TF inputs
between('grp_tf = "1. Block Timeframe (HTF in LTF)"\n', 'grp_cndl = "2. Candle Classification"\n', '//@@TF_INPUTS@@\n\n')
rep('grp_cndl = "2. Candle Classification"', 'grp_cndl = "1. Candle Classification"')
rep('grp_strc = "3. Zone Structure (Engine x)"', 'grp_strc = "2. Zone Structure (Engine x)"')
rep('''maxBoxes      = input.int(8, "Max Past Boxes", minval=0, maxval=50, inline="bx2", group=grp_strc)''',
    '''maxBoxes      = input.int(8, "Max Past Boxes (cap)", minval=0, maxval=50, inline="bx2", group=grp_strc, tooltip="A hard cap on past boxes. They also follow the Max Items rule below.")''')
i0 = src.find('maxLines      = input.int(10'); i1 = src.find('\n', i0)
src = src[:i0] + src[i1+1:]
i0 = src.find('show_tn_step  = input.bool(true'); i1 = src.find('\n', i0)
src = src[:i0] + src[i1+1:]
rep('''//@@GATE_INPUTS@@''', '''//@@RANGE_INPUTS@@
//@@TN_INPUT@@

//@@GATE_INPUTS@@''')
rep('''//@@NEWS_INPUTS@@''', '''//@@NEWS_INPUTS@@
//@@STATS_INPUTS@@''')
rep('''//@@GATE_ENGINE@@
//@@ZONE_HELPERS@@
//@@LEVELS@@
//@@ZONE_ENGINE@@
//@@HTF_ENGINE@@
//@@NEWS_ENGINE@@''', '''//@@GATE_ENGINE@@
//@@TF_ENGINE@@
//@@ZONE_HELPERS@@
//@@LEVELS@@
//@@RANGE_HELPERS@@
//@@ZONE_ENGINE@@
//@@HTF_ENGINE@@
//@@NEWS_ENGINE@@
//@@STATS_ENGINE@@
//@@XDXP_ENGINE@@''')
# remove the local block TF section (now in TF_ENGINE)
between('// BLOCK TIMEFRAME — last CLOSED block candle', '// ENGINE CALL (every bar', '''// ═══════════════════════════════════════════════════════════════
''')
# the line before that header is a ═ rule; keep structure tidy
rep('f_zoneEngine(stepNow, bO, bH, bL, bC, bV, bPH, bPL, bT, boxGrow, expMode)', 'f_zoneEngine(stepNow, bO, bH, bL, bC, bV, bH1, bL1, bT, boxGrow, expMode, gateOn, gHi, gLo)')
rep('eEndF, eEndH, eEndL, eEndT, eEndRole, eEndNdb] = f_zoneEngine(', 'eEndF, eEndH, eEndL, eEndT, eEndRole, eEndNdb, ePConf] = f_zoneEngine(')
rep('        bool pass   = not gateOn or (isFlip ? (up ? hitXD : hitXP) : (up ? (bullImp and bullPb) : (bearImp and bearPb)))', '        bool pass   = true   // the gate shapes the structure itself (small p until confirmed)')
rep('''    f_draw_groups()
''', '''    f_draw_groups()
    f_xdxpDraw()
''')

# Bu / Be prefixes on P# / R#
rep('''        if not na(zPP)
            f_add_level(zPP, TFP + "P" + str.tostring(zTier) + "x", zSide == 1 ? c_bear_po4 : c_bull_po4, 1, line.style_dashed, zPT, futureT, 4, lvl_size, "P# = pullback start. A block close " + (zSide == 1 ? "above" : "below") + " it = " + (zSide == 1 ? "LDx" : "SDx") + str.tostring(zTier) + ".")''',
'''        if not na(zPP)
            f_add_level(zPP, TFP + (pCf ? (zSide == 1 ? "BeP" : "BuP") : (zSide == 1 ? "bep" : "bup")) + str.tostring(zTier) + "x" + (pCf ? "" : " · p"), color.new(zSide == 1 ? c_bear_po4 : c_bull_po4, pCf ? 0 : 40), 1, line.style_dashed, zPT, futureT, 4, lvl_size, pCf ? "P# = pullback start. A block close " + (zSide == 1 ? "above" : "below") + " it = " + (zSide == 1 ? "LDx" : "SDx") + str.tostring(zTier) + "." : "small p: the " + gate_mode + " gate has not confirmed this pullback yet (leg's own extreme, then the opposite extreme). A close through it deletes it: no LDx / SDx.")''')
rep('''f_add_level(zRP, TFP + "R" + str.tostring(zTier) + "x", ''', '''f_add_level(zRP, TFP + (zSide == 1 ? "BuR" : "BeR") + str.tostring(zTier) + "x", ''')
rep('''text=eLiveRole == 1 ? "P" + str.tostring(zTier) + "x" : eLiveRole == 2 ? "R" + str.tostring(zTier) + "x" : ""''',
    '''text=eLiveRole == 1 ? TFP + (pCf ? (zSide == 1 ? "BeP" : "BuP") : (zSide == 1 ? "bep" : "bup")) + str.tostring(zTier) + "x" : eLiveRole == 2 ? TFP + (zSide == 1 ? "BuR" : "BeR") + str.tostring(zTier) + "x" : ""''')

# ---- RENDER: range rule with the 50 / 50 allocator
old_range_start = '''    float rHi = na
    float rLo = na
    if not na(lastBull)'''
old_range_end = '''    // PO4 lines + married breaks + eBlock / iBlock'''
between(old_range_start, old_range_end, '''    // The always-drawn range = highest to lowest marker, and their candles.
    float rHi = na
    float rLo = na
    int   hiT = na
    int   loT = na
    for m in array.from(lastBull, starBull, lastBear, starBear)
        if not na(m)
            if na(rHi) or m.price > rHi
                rHi := m.price
                hiT := m.t
            if na(rLo) or m.price < rLo
                rLo := m.price
                loT := m.t
    int spanMs = timeframe.in_seconds(blockTF) * 1000
    array<int> q = f_quota()
    bool pCf = not gateOn or ePConf   // GATE: P# is a small p until confirmed

    // 1. PO4s, newest first (PO4 + break + zone = ONE item)
    array<ZPO> vis = array.new<ZPO>()
    if po4s.size() > 0
        array<int> sq = array.new<int>()
        for p in po4s
            sq.push(p.seq)
        array<int> ord = sq.sort_indices(order.descending)
        for k = 0 to ord.size() - 1
            ZPO p = po4s.get(ord.get(k))
            if f_take(q, f_inR(p.price, rHi, rLo) or f_onMarker(p.t, hiT, loT, spanMs), p.side == 1)
                vis.push(p)

''')
rep('''                drawn_labels.push(label.new(int(math.avg(cz.t1, cz.t2)), cz.price, cz.pass ? cz.kind : str.lower(cz.kind),''',
    '''                drawn_labels.push(label.new(int(math.avg(cz.t1, cz.t2)), cz.price, cz.pass ? cz.kind : TFP + str.lower(str.substring(cz.kind, str.length(TFP))),''')
rep('''text=zone_show_name ? f_zoneName(p.tier == 1, isBull, ENG) : ""''', '''text=zone_show_name ? TFP + f_zoneName(p.tier == 1, isBull, ENG) : ""''')

# P# / R#: live range (exempt when showLiveAlways)
rep('''    if showPR and zSide != 0
        if not na(zPP)
''', '''    if showPR and zSide != 0
        bool pOk = not na(zPP) and (showLiveAlways or f_take(q, f_inR(zPP, rHi, rLo) or f_onMarker(zPT, hiT, loT, spanMs), zSide == -1))
        bool rOk = not na(zRP) and (showLiveAlways or f_take(q, f_inR(zRP, rHi, rLo) or f_onMarker(zRT, hiT, loT, spanMs), zSide == 1))
        if pOk
''')
rep('''        if not na(zRP)
            f_add_level(zRP''', '''        if rOk
            f_add_level(zRP''')
rep('''    if showLiveBox and eLive and not na(eBxH)
''', '''    if showLiveBox and eLive and not na(eBxH) and (showLiveAlways or f_take(q, f_boxInR(eBxH, eBxL, rHi, rLo) or f_onMarker(eBxT, hiT, loT, spanMs), zSide == 1))
''')
rep('''            bool want = zb.role > 0 ? showRoleBoxes : showIntBoxes
            if want
''', '''            bool want = zb.role > 0 ? showRoleBoxes : showIntBoxes
            bool onM  = (not na(hiT) and zb.t1 <= hiT and zb.t2 >= hiT) or (not na(loT) and zb.t1 <= loT and zb.t2 >= loT)
            if want and f_take(q, f_boxInR(zb.top, zb.bot, rHi, rLo) or onM, zb.ndb >= 0)
''')

# ── box lifetime: a box that did not turn into a PO4 dies on a close through it
rep('''            ZPO p = po4s.get(i)
            if (p.side == 1 and bC < p.price) or (p.side == -1 and bC > p.price)
                po4s.remove(i)
''', '''            ZPO p = po4s.get(i)
            if (p.side == 1 and bC < p.price) or (p.side == -1 and bC > p.price)
                // husband & wife: the box the PO4 came from goes with it
                if pastBox.size() > 0
                    for j = pastBox.size() - 1 to 0
                        if pastBox.get(j).t1 == p.oT
                            pastBox.remove(j)
                po4s.remove(i)
''')
rep('''    prevSide := zSide
''', '''    // BOX LIFETIME: a box that did NOT turn into a CDLx / CDSx / LDx / SDx PO4
    // (and is not the live P# / R#) is deleted on a block close through it:
    // bearish box (red, distribution) = a close ABOVE its top,
    // bullish box (green, accumulation) = a close BELOW its bottom.
    if pastBox.size() > 0
        for i = pastBox.size() - 1 to 0
            ZBox zb = pastBox.get(i)
            bool married = (not na(zPT) and zb.t1 == zPT) or (not na(zRT) and zb.t1 == zRT)
            if not married and po4s.size() > 0
                for p in po4s
                    if p.oT == zb.t1
                        married := true
                        break
            bool bearBox = zb.ndb < 0
            if not married and ((bearBox and bC > zb.top) or (not bearBox and bC < zb.bot))
                pastBox.remove(i)
    prevSide := zSide
''')
open('/home/claude/v36/concepts37_template.pine', 'w').write(src)
print('ok', src.count('\n'))
