"""MMM PRO PLUS standalone: remove every test / statistics / points-test part, add white NBC candles and the HTF SuperTrend bias."""
L = open('proplus_full.pine', encoding='utf-8').read().replace('\r\n', '\n').split('\n')
N = len(L)
keep = [True] * (N + 1)          # 1-indexed
rep = {}                          # line -> list of new lines (replaces that line)

def drop(a, b):
    for i in range(a, b + 1): keep[i] = False

def chk(i, s):
    assert s in L[i - 1], (i, s, L[i - 1][:90])

# ── inputs ──
chk(25, 'show_panel'); drop(25, 25)
chk(51, 'panel_pos_s'); chk(56, 'panel2_pos_s'); drop(51, 56)
chk(61, 'flip_test_n'); drop(61, 61)
chk(67, '5. Points Test'); chk(88, 'pts_t4_pos'); drop(67, 89)
chk(106, 'T1_WAIT'); drop(106, 106)
chk(24, 'show_sigs')
L[23] = L[23].replace('First body close after structure, SuperTrend and VWAP all line up. Never during a Stall.',
                      'First body close after structure, SuperTrend and VWAP all line up. Never during a Stall.\\nWith the HTF bias filter ON (group 5): only in the direction of the higher-timeframe SuperTrend.')
# colors: white NBC candles
chk(38, 'vw_neut_col')
rep[38] = [L[37],
           'nbc_on       = input.bool(false, "Color NBC Candles", inline="c4", group=grp_col, tooltip="NBC = no body close: the candle did not close above the prior candle high or below its low (not a BuX / BeX).\\nON: every NBC candle is painted this color (white by default). Bright GMC candles keep their GMC color.\\nOn a white chart background, pick another color.")',
           'col_nbc      = input.color(color.white, "", inline="c4", group=grp_col)']
# HTF bias inputs, after the Stall Exit Rule group
chk(65, 'exit_rule')
rep[65] = [L[64], '',
           '// ─── 5. HTF SuperTrend Bias ───',
           'grp_htf      = "5. HTF SuperTrend Bias"',
           'htf_on       = input.bool(true, "HTF SuperTrend Bias", group=grp_htf, tooltip="The standard SuperTrend (2 x 14) of a HIGHER timeframe, shown on this chart.\\nIt uses the last CLOSED higher-timeframe candle, so it never repaints: it updates when that candle closes.\\nBias BULL = the HTF SuperTrend is green. BEAR = red.")',
           'htf_tf       = input.timeframe("15", "Timeframe", group=grp_htf, tooltip="Pick a timeframe HIGHER than the chart. Default 15 minutes.\\nExample: 1m / 2m / 5m chart + 15m bias. 15m chart + 1h bias.\\nIf it is not higher than the chart, the bias is switched off and the badge says so.")',
           'htf_line     = input.bool(true, "HTF SuperTrend Line", inline="hl", group=grp_htf)',
           'htf_width    = input.int(2, "Width", minval=1, maxval=5, inline="hl", group=grp_htf)',
           'htf_badge    = input.bool(true, "Bias Badge", inline="hb", group=grp_htf)',
           'htf_pos_s    = input.string("Top Right", "", options=["Top Right", "Top Center", "Top Left", "Middle Right", "Middle Left", "Bottom Right", "Bottom Center", "Bottom Left"], inline="hb", group=grp_htf)',
           'htf_size_s   = input.string("Small", "Badge Size", options=["Tiny", "Small", "Normal", "Large"], group=grp_htf)',
           'htf_arrows   = input.bool(true, "BULL / BEAR Arrows Only With The HTF Bias", group=grp_htf, tooltip="ON: a BULL arrow needs the HTF SuperTrend green, a BEAR arrow needs it red. Turn the arrows on in group 0.")',
           'htf_fade     = input.bool(false, "Fade Trend Candles Against The HTF Bias", group=grp_htf, tooltip="ON: bull trend candles while the HTF bias is BEAR (and bear trend candles while it is BULL) are drawn lighter.")']

# ── types ──
chk(154, '// EXIT test'); chk(162, 'string txt')
rep[154] = ['// EXIT label. side -1 = EXIT SHORT (bear stall broke), 1 = EXIT LONG. hi / lo = the EXIT candle range.',
            '// The first close outside that range adds ✓ (reversed: the exit was right) or ✕ (the trend came back).',
            'type ExitTest', '    int    side', '    float  hi', '    float  lo', '    label  lbl', '    string txt']
drop(155, 162)
chk(164, 'PO4 T1 touch test'); chk(174, 'float lo'); drop(164, 175)
chk(176, 'After-EXIT test'); chk(191, 'bool  gmc')
rep[176] = ['// After EXIT. side 1 = bull stall (EXIT LONG), -1 = bear stall (EXIT SHORT).',
            '// ext = box far edge (bull high / bear low). mid = RE-ENTRY 50% between ext and the SuperTrend line.',
            '// Live until the box breaks (close beyond ext) or the SuperTrend flips. stRej = the ST rejection alert already fired.',
            'type PxTest', '    int   side', '    float ext', '    float mid', '    int   t0', '    bool  stRej = false']
drop(177, 192)
chk(193, 'Points-test trade'); chk(206, 'stopPx'); drop(193, 207)
chk(251, 'panel_sz'); drop(251, 251)
chk(254, 'Stats start'); drop(254, 256)
chk(294, 'prevLow'); chk(295, 'prevHigh'); drop(294, 295)

# ── structure ──
chk(369, 't1Tests'); chk(372, 't1Expired'); drop(369, 372)
chk(395, 'scLd'); chk(396, 'scCds'); drop(395, 396)
chk(415, 'evGateNew'); chk(424, 'evT1Fake'); drop(415, 424)
chk(430, 'PO4 T1 Touch Test'); chk(477, 't1Tests.shift()'); drop(430, 478)
for i in (518, 519, 520, 525, 526, 527):
    assert any(k in L[i - 1] for k in ('flipOuter', 'flipStB', 'flipPoB')), L[i - 1]
    drop(i, i)
for a in (579, 643):
    chk(a, 'if src.score >= 0'); chk(a + 1, 'scCds.set'); drop(a, a + 1)
for a in (616, 680):
    chk(a, 'if fsP.score >= 0'); chk(a + 1, 'scLd.set'); drop(a, a + 1)
for a in (720, 749):
    chk(a, 'evGateNew := true'); drop(a, a)

# ── stall zones: rewrite the state part (keep f_zone / f_farBreak) ──
chk(796, 'var Stall          liveZ'); chk(1020, 'bool stallOn')
NEW_STALL = r'''var Stall          liveZ     = na
var Stall          pendZ     = na
var Stall          keptBear  = na
var Stall          keptBull  = na
var int            liveBar0  = na
var bool           liveTouch = false
var array<ExitTest> exTests  = array.new<ExitTest>()
// One after-EXIT watch per side: once you are out, a later EXIT on the same side does not draw a new 50% line.
var array<PxTest>  pxTests   = array.new<PxTest>()

bool evPxRej     = false
bool evPxBreak   = false
bool evStallOn   = false
bool evStallBrk  = false
bool evStallCont = false
bool evRej       = false
bool evExitRev   = false
bool evExitCont  = false

if barstate.isconfirmed and not na(st_raw) and not na(st_raw[1])
    bool flipNow = dir_raw != dir_raw[1]
    bool stepNow = not flipNow and (stUp ? st_raw > st_raw[1] : st_raw < st_raw[1])

    // EXIT label result: the first close outside the EXIT candle range.
    if exTests.size() > 0
        for i = exTests.size() - 1 to 0
            ExitTest x = exTests.get(i)
            bool upOut = close > x.hi
            bool dnOut = close < x.lo
            if upOut or dnOut
                bool rev = x.side == -1 ? upOut : dnOut
                if rev
                    evExitRev := true
                else
                    evExitCont := true
                if not na(x.lbl)
                    label.set_text(x.lbl, x.txt + (rev ? " ✓" : " ✕"))
                exTests.remove(i)

    // After EXIT: the RE-ENTRY 50% line lives until the box breaks or the SuperTrend flips.
    if pxTests.size() > 0
        for i = pxTests.size() - 1 to 0
            PxTest x = pxTests.get(i)
            if flipNow
                pxTests.remove(i)
            else
                bool isBull = x.side == 1
                if isBull ? (low <= st_raw and close > st_raw) : (high >= st_raw and close < st_raw)
                    if not x.stRej
                        evPxRej := true
                    x.stRej := true
                if isBull ? close > x.ext : close < x.ext
                    evPxBreak := true
                    pxTests.remove(i)

    if not na(keptBear) and f_farBreak(keptBear)
        f_kill(keptBear)
        keptBear := na
    if not na(keptBull) and f_farBreak(keptBull)
        f_kill(keptBull)
        keptBull := na
    if not na(pendZ) and f_farBreak(pendZ)
        f_kill(pendZ)
        pendZ := na

    if not na(liveZ)
        [zs, zt, zr] = f_zone(liveZ, liveBar0, liveTouch)
        liveTouch := zt
        bool isBear = liveZ.side == -1
        if zr
            evRej := true
            if show_rej
                if isBear
                    liveZ.lbls.push(label.new(bar_index, high, "REJ" + str.tostring(liveZ.rej), yloc=yloc.abovebar, style=label.style_label_down, color=color.new(col_stall, 20), textcolor=color.white, size=exit_sz))
                else
                    liveZ.lbls.push(label.new(bar_index, low, "REJ" + str.tostring(liveZ.rej), yloc=yloc.belowbar, style=label.style_label_up, color=color.new(col_stall, 20), textcolor=color.white, size=exit_sz))
        if zs == 0 and liveZ.bars == STALL_BARS
            evStallOn := true
        if zs == 1
            evStallBrk := true
            string exTxt = isBear ? "EXIT SHORT" : "EXIT LONG"
            label  exL   = na
            if show_exits
                if isBear
                    exL := label.new(bar_index, low, exTxt, yloc=yloc.belowbar, style=label.style_label_up, color=col_bull, textcolor=color.white, size=exit_sz)
                else
                    exL := label.new(bar_index, high, exTxt, yloc=yloc.abovebar, style=label.style_label_down, color=col_bear, textcolor=color.white, size=exit_sz)
                liveZ.lbls.push(exL)
            exTests.push(ExitTest.new(liveZ.side, high, low, exL, exTxt))
            while exTests.size() > MAX_TEST
                exTests.shift()
            bool sideBusy = false
            if pxTests.size() > 0
                for px in pxTests
                    if px.side == liveZ.side
                        sideBusy := true
            if not sideBusy and not flipNow
                pxTests.push(PxTest.new(liveZ.side, liveZ.ext, (liveZ.ext + stPrev) / 2, time))
            f_kill(pendZ)
            pendZ := liveZ
            liveZ := na
        else if zs == 2
            evStallCont := true
            f_kill(liveZ)
            liveZ := na

    if flipNow
        if not na(pendZ)
            pendZ.tFlip := time
            if pendZ.side == -1
                f_kill(keptBear)
                keptBear := pendZ
            else
                f_kill(keptBull)
                keptBull := pendZ
            pendZ := na
        if not na(liveZ)
            f_kill(liveZ)
            liveZ := na
    if stepNow
        if not na(liveZ)
            f_kill(liveZ)
            liveZ := na
    if flipNow or stepNow
        int sd = stUp ? 1 : -1
        liveZ     := Stall.new(time, time, sd == 1 ? math.min(open, close) : math.max(open, close), sd == 1 ? high : low, sd, 0, 0, 0, array.new<label>(), na)
        liveBar0  := bar_index
        liveTouch := false

bool stallOn = not na(liveZ) and liveZ.bars >= STALL_BARS'''.split('\n')
rep[796] = NEW_STALL
drop(797, 1020)

# ── flip test, flip ladder, points test ──
chk(1022, 'Flip Test'); chk(1406, 'Bu GMC / Be GMC Lines'); drop(1022, 1405)

# ── candle coloring with NBC + HTF fade ──
chk(1436, 'Candle Coloring'); chk(1464, 'barcolor(')
COLOR = r'''// ─── Candle Coloring ───
bool isNbc = not isBuX and not isBeX
color barCol = na
if barstate.isconfirmed
    if fsTrend == 1
        if stUp
            barCol := close > vwap_val ? col_bull : color.new(col_bull, 55)
            if htfFade and htfDir == -1
                barCol := color.new(col_bull, 75)
        else
            bool pastGate = not na(gatePx) and close > gatePx
            barCol := pastGate ? color.new(col_pb, 55) : col_pb
    else if fsTrend == -1
        if not stUp
            barCol := close < vwap_val ? col_bear : color.new(col_bear, 55)
            if htfFade and htfDir == 1
                barCol := color.new(col_bear, 75)
        else
            bool pastGate = not na(gatePx) and close < gatePx
            barCol := pastGate ? color.new(col_pb, 55) : col_pb
    if nbc_on and isNbc
        barCol := col_nbc'''.split('\n')
rep[1436] = COLOR
drop(1437, 1450)

# ── HTF bias block, before the plots ──
chk(1432, '// ─── Plots ───')
HTF = r'''// ─── HTF SuperTrend Bias ───
// Standard SuperTrend (2 x 14) of the chosen timeframe, from its last CLOSED candle (no repaint).
f_htfSt() =>
    [hSt, hD] = ta.supertrend(ST_MULT, ST_LEN)
    [hSt[1], hD[1] < 0 ? 1 : -1]

f_tfName(string tf) =>
    int s = timeframe.in_seconds(tf)
    s < 60 ? str.tostring(s) + "s" : s < 3600 ? str.tostring(s / 60, "#") + "m" : s < 86400 ? str.tostring(s / 3600, "#") + "h" : tf

[htfStRaw, htfDirRaw] = request.security(syminfo.tickerid, htf_tf, f_htfSt(), lookahead=barmerge.lookahead_on)
bool  htfValid = htf_on and timeframe.isintraday and timeframe.in_seconds(htf_tf) > timeframe.in_seconds()
float htfSt    = htfValid ? htfStRaw : na
int   htfDir   = htfValid and not na(htfStRaw) ? htfDirRaw : 0
bool  htfFilt  = htfValid and htf_arrows
bool  htfFade  = htfValid and htf_fade

plot(htf_line ? htfSt : na, "HTF SuperTrend", color=color.new(htfDir == 1 ? col_bull : col_bear, 35), style=plot.style_stepline, linewidth=htf_width)

var table htfTbl = table.new(f_pos(htf_pos_s), 2, 2, bgcolor=PANEL_BG, border_width=1, border_color=color.new(PANEL_TXT, 80))
if barstate.islast and htf_on and htf_badge
    string bsz = f_size(htf_size_s)
    string tfn = f_tfName(htf_tf)
    if not htfValid
        table.cell(htfTbl, 0, 0, "HTF " + tfn, text_color=PANEL_TXT, text_size=bsz, text_halign=text.align_left)
        table.cell(htfTbl, 1, 0, "PICK A TIMEFRAME HIGHER THAN THE CHART", text_color=color.orange, text_size=bsz, text_halign=text.align_left)
        table.cell(htfTbl, 0, 1, "", text_size=bsz)
        table.cell(htfTbl, 1, 1, "", text_size=bsz)
    else
        int    chDir = stUp ? 1 : -1
        color  hc    = htfDir == 1 ? col_bull : htfDir == -1 ? col_bear : color.gray
        string ht    = htfDir == 1 ? "BULL" : htfDir == -1 ? "BEAR" : "LOADING"
        bool   agree = htfDir != 0 and chDir == htfDir
        table.cell(htfTbl, 0, 0, "HTF " + tfn + " BIAS", text_color=PANEL_TXT, text_size=bsz, text_halign=text.align_left)
        table.cell(htfTbl, 1, 0, ht, text_color=hc, text_size=bsz, text_halign=text.align_left)
        table.cell(htfTbl, 0, 1, "CHART " + (chDir == 1 ? "BULL" : "BEAR"), text_color=chDir == 1 ? col_bull : col_bear, text_size=bsz, text_halign=text.align_left)
        table.cell(htfTbl, 1, 1, htfDir == 0 ? "-" : agree ? "WITH BIAS" : "AGAINST BIAS", text_color=agree ? col_bull : color.orange, text_size=bsz, text_halign=text.align_left)

'''.split('\n')
rep[1432] = HTF + [L[1431]]

# ── arrows: HTF filter ──
chk(1467, 'bool bullAlign'); chk(1468, 'bool bearAlign')
L[1466] = L[1466] + ' and (not htfFilt or htfDir == 1)'
L[1467] = L[1467] + ' and (not htfFilt or htfDir == -1)'

# ── drawing: 50% line no longer has a state ──
chk(1612, 'x.state == 0 and not na(x.mid)')
L[1611] = L[1611].replace('x.state == 0 and not na(x.mid)', 'not na(x.mid)')

# ── dashboard ──
chk(1652, 'Dashboard and Scorecard'); chk(2022, '// ─── Alerts ───'); drop(1652, 2021)
# ── alerts ──
chk(2036, 'evT1Rej'); chk(2038, 'evT1Fake'); drop(2036, 2038)
rep[2048] = [L[2047],
             'alertcondition(htfValid and htfDir == 1 and htfDir[1] == -1, "HTF Bias Turned Bullish", "The higher-timeframe SuperTrend turned green - HTF bias BULL")',
             'alertcondition(htfValid and htfDir == -1 and htfDir[1] == 1, "HTF Bias Turned Bearish", "The higher-timeframe SuperTrend turned red - HTF bias BEAR")']

# header note
rep[2] = [L[1], '',
          '// Standalone (Nov 2 2026): all test tables, statistics and the points test removed.',
          '// New: color NBC candles (white by default) · HTF SuperTrend bias (15m by default) with line, badge, arrow filter and alerts.']

out = []
for i in range(1, N + 1):
    if i in rep:
        out += rep[i]
    elif keep[i]:
        out.append(L[i - 1])
src = '\n'.join(out)
while '\n\n\n' in src: src = src.replace('\n\n\n', '\n\n')
open('MMM_PRO_PLUS.pine', 'w', encoding='utf-8').write(src.rstrip() + '\n')
print('lines', len(src.split('\n')))
