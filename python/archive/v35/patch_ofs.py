import sys, re
sys.path.insert(0, '/home/claude/v35')
from news_module import NEWS_INPUTS, NEWS_ENGINE
src = open('/home/claude/MMM_Order_Flow_Suite_3.4.pine').read()

def rep(old, new, count=1):
    global src
    c = src.count(old)
    if c != count:
        print("FAIL count=%d for:\n%s" % (c, old[:400])); sys.exit(1)
    src = src.replace(old, new)

def rep_block(start, end, new):
    global src
    i0 = src.find(start); assert i0 >= 0, start[:80]
    i1 = src.find(end, i0); assert i1 > i0, end[:80]
    src = src[:i0] + new + src[i1 + len(end):]

rep('indicator("MMM Market Structure & Order Flow Suite @MaxMaserati 3.4", "MMM Order Flow @MaxMaserati 3.4"', 'indicator("MMM Market Structure & Order Flow Suite @MaxMaserati 3.5", "MMM Order Flow @MaxMaserati 3.5"')
rep('// MMM ORDER FLOW SUITE 3.4 — the SWING engine of the MMM foundation', '// MMM ORDER FLOW SUITE 3.5 — the SWING engine of the MMM foundation')
rep('''//          SH1, SH2… / SL1, SL2… = the number of the break each swing
//          will make if it is taken next.''', '''//          SL1, SL2… (bull) / SH1, SH2… (bear) = the swing that MADE
//          that break (the start of the leg that broke). Every other
//          swing is a plain lowercase sh / sl.
//          Labels: CDL / LD above the middle of the break line,
//                  CDS / SD below the middle of the break line.''')

# ---- inputs
rep('''showNumbers         = input.bool(true, "Number Breaks + Swings", group=grp_strc, tooltip="After a CDL: LD1, LD2, LD3… until the next CDS. Swing highs of the new leg show SH1, SH2… = the LD number they make if taken next. Mirror for CDS / SD / SL.")''',
    '''showNumbers         = input.bool(true, "Number Breaks + Swings", group=grp_strc, tooltip="After a CDL: LD1, LD2, LD3… until the next CDS. The swing low that MADE each break gets the same number: SL1 made LD1, SL2 made LD2… (the swing that made the CDL is plain SL). Every other swing is lowercase sh / sl. Mirror for CDS / SD / SH. The count resets on every flip.")''')

rep_block('grp_news = "News Block (no trades)"\n', 'news_bg    = input.bool(true, "Shade News Windows", group=grp_news)\n', NEWS_INPUTS.format(grp="News Block (no trades)"))

rep('''show_uh_ul      = input.bool(true, "Enable UH$/UL$ Detection", group=grp_wick, tooltip="Candles closing flat at their extreme leave un-auctioned price. Deleted when a candle CLOSES beyond the level (above UH$, below UL$).")''',
    '''show_uh_ul      = input.bool(true, "Enable UH$/UL$ Detection", group=grp_wick, tooltip="Candles closing flat at their extreme leave un-auctioned price.")
uh_del_mode     = input.string("Close Beyond", "Delete UH$/UL$ On", options=["Close Beyond", "Touch"], group=grp_wick, tooltip="Close Beyond = deleted when a later candle CLOSES above UH$ / below UL$.\\nTouch = deleted the first time a later candle's wick reaches the level.")''')

# ---- news engine
rep_block('f_inWin(int startMin, int endMin) =>\n', "bgcolor(news_bg and newsBlock ? color.new(color.orange, 85) : na, title=\"News Window\")\n", NEWS_ENGINE)

# ---- swing type: number of the break it made
rep('''    bool         isProtected
    array<line>  breakLines''', '''    bool         isProtected
    int          num
    array<line>  breakLines''')
rep('''        lb := label.new(showLabelsRight ? futureTime : t, price, isHigh ? "SH" : "SL", xloc=xloc.bar_time''', '''        lb := label.new(showLabelsRight ? futureTime : t, price, isHigh ? "sh" : "sl", xloc=xloc.bar_time''')
rep('''    SwingLine.new(ln, lb, price, t, bar_index, false, array.new<line>(), array.new<label>())''', '''    SwingLine.new(ln, lb, price, t, bar_index, false, -1, array.new<line>(), array.new<label>())''')

rep_block('unprotectSwing(SwingLine s, bool isHigh) =>\n', '''        s.lbl.set_tooltip("")
''', '''// Name of a swing: SL3 = it made LD3 · SL = it made the flip · sl = plain swing
f_swingName(SwingLine s, bool isHigh) =>
    string base = isHigh ? "SH" : "SL"
    s.num > 0 ? base + (showNumbers ? str.tostring(s.num) : "") : s.num == 0 ? base : str.lower(base)

unprotectSwing(SwingLine s, bool isHigh) =>
    s.isProtected := false
    if not na(s.id)
        s.id.set_color(isHigh ? LINE_BEAR : LINE_BULL)
        s.id.set_width(1)
    if not na(s.lbl)
        s.lbl.set_text(f_swingName(s, isHigh))
        s.lbl.set_textcolor(isHigh ? LINE_BEAR : LINE_BULL)
        s.lbl.set_tooltip("")
''')

rep_block('// Only ONE protected level per side: the newest one\n', '''                s.lbl.set_style(label.style_label_left)
''', '''// A flip ends the continuous swing range: every old number is cleared.
clearNums(SwingLine[] arr, bool isHigh) =>
    if arr.size() > 0
        for s in arr
            s.num := -1
            if not na(s.lbl) and not s.isProtected
                s.lbl.set_text(f_swingName(s, isHigh))

// Only ONE protected level per side: the newest one. It is the swing that
// MADE this break, so it takes the break number (0 = the flip).
highlightLastSwing(SwingLine[] swings, int num, bool pass, color baseColor, bool isHigh) =>
    int n = swings.size()
    if n > 0
        if n > 1
            for j = 0 to n - 2
                SwingLine o = swings.get(j)
                if o.isProtected
                    unprotectSwing(o, isHigh)
        SwingLine s = swings.last()
        s.isProtected := true
        s.num := num
        if not na(s.lbl)
            s.lbl.set_text(f_swingName(s, isHigh) + (showProtectedLevels ? " PL" : ""))
            s.lbl.set_style(label.style_label_left)
        if showProtectedLevels
            if not na(s.id)
                s.id.set_color(baseColor)
                s.id.set_width(2)
            if not na(s.lbl)
                s.lbl.set_textcolor(pass ? baseColor : FAIL_COL)
                s.lbl.set_tooltip("Protected Level (PL) - the swing that made this break. A body close through it flips the structure.")
''')

# remove the old forward numbering of swings
rep_block('// Swings of the CURRENT leg get the number of the break they make if taken next.\n', '''            s.lbl.set_text((isHigh ? "SH" : "SL") + str.tostring(cnt + k + 1))
''', '')
rep('''    // 2g. Number the swings of the current leg (SH1, SH2… / SL1, SL2…)
    f_numberSwings(swingHighs, true, 1, ldCount, lastCdlBar)
    f_numberSwings(swingLows, false, -1, sdCount, lastCdsBar)

''', '')

# break label: middle of the break line, CDL/LD above, CDS/SD below
rep('''    label bb = label.new(time, s.price, txt, xloc=xloc.bar_time, color=color(na), textcolor=c, style=label.style_label_left, size=size.tiny, tooltip=f_breakTip(kind, isBull, pass))''',
    '''    int   mid = int(math.avg(s.t1, time))
    label bb = label.new(mid, s.price, txt, xloc=xloc.bar_time, color=color(na), textcolor=c, style=isBull ? label.style_label_down : label.style_label_up, size=size.tiny, tooltip=f_breakTip(kind, isBull, pass))''')
rep('''// Break line from the swing to the break candle; label at the MIDDLE RIGHT of the line end''', '''// Break line from the swing to the break candle. Label in the MIDDLE of the
// line: CDL / LD above it, CDS / SD below it.''')

# protected-level calls
rep('''                        if isFlip
                            unprotectAll(swingLows, false)
                        if showBreaks and (pass or show_failed)
                            f_drawBreak(s, swingHighs, kind, false, pass)
                        highlightLastSwing(swingHighs, (pass ? kind : str.lower(kind)) + " SH", PROT_BEAR, true)''',
    '''                        if isFlip
                            unprotectAll(swingLows, false)
                            clearNums(swingLows, false)
                            clearNums(swingHighs, true)
                        if showBreaks and (pass or show_failed)
                            f_drawBreak(s, swingHighs, kind, false, pass)
                        highlightLastSwing(swingHighs, num, pass, PROT_BEAR, true)''')
rep('''                        if isFlip
                            unprotectAll(swingHighs, true)
                        if showBreaks and (pass or show_failed)
                            f_drawBreak(s, swingLows, kind, true, pass)
                        highlightLastSwing(swingLows, (pass ? kind : str.lower(kind)) + " SL", PROT_BULL, false)''',
    '''                        if isFlip
                            unprotectAll(swingHighs, true)
                            clearNums(swingHighs, true)
                            clearNums(swingLows, false)
                        if showBreaks and (pass or show_failed)
                            f_drawBreak(s, swingLows, kind, true, pass)
                        highlightLastSwing(swingLows, num, pass, PROT_BULL, false)''')

# UH / UL deletion mode
rep('''            if close > uh_prices.get(i)''', '''            if uh_del_mode == "Touch" ? high >= uh_prices.get(i) : close > uh_prices.get(i)''')
rep('''            if close < ul_prices.get(i)''', '''            if uh_del_mode == "Touch" ? low <= ul_prices.get(i) : close < ul_prices.get(i)''')
rep('''tooltip="Un-auctioned high: deleted when a candle closes above it"''', '''tooltip="Un-auctioned high (UH$): price never traded above this close"''')
rep('''tooltip="Un-auctioned low: deleted when a candle closes below it"''', '''tooltip="Un-auctioned low (UL$): price never traded below this close"''')

open('/home/claude/v35/MMM_Order_Flow_Suite_3.5.pine', 'w').write(src)
print("ok", src.count('\n'))
