import sys
sys.path.insert(0, '/home/claude/v36')
from ofs37_parts import TYPES, STEP2, RENDER
src = open('/home/claude/v36/ofs_template.pine').read()

def rep(old, new, count=1):
    global src
    c = src.count(old)
    if c != count:
        print("FAIL", c, old[:200]); sys.exit(1)
    src = src.replace(old, new)

def between(start, end, new, keep_end=True):
    global src
    i0 = src.find(start); assert i0 >= 0, start[:60]
    i1 = src.find(end, i0 + len(start)); assert i1 > i0, end[:60]
    src = src[:i0] + new + (src[i1:] if keep_end else src[i1 + len(end):])

rep('indicator("MMM Market Structure & Order Flow Suite @MaxMaserati 3.6", "MMM Order Flow @MaxMaserati 3.6"', 'indicator("MMM Market Structure & Order Flow Suite @MaxMaserati 3.7", "MMM Order Flow @MaxMaserati 3.7"')
rep('''// MMM ORDER FLOW SUITE 3.6 — the SWING engine "s" of the MMM foundation
//''', '''// MMM ORDER FLOW SUITE 3.7 — the SWING engine "s" of the MMM foundation
//
//  HTF IN LTF: the swings are built on the STRUCTURE timeframe (closed
//            candles only) and drawn on the chart. AX, UH$/UL$ and voids
//            stay on the chart timeframe.''')
rep('''//            Every other swing is a plain lowercase sh / sl.''', '''//            Live range: BeP#s / BuP#s = the newest swing a close past
//            makes the next LD / SD · BuR#s / BeR#s = the newest swing after
//            it (the next T#). Every other swing is a plain lowercase sh / sl.''')
rep('''//  🟢 / 🔴 = T1 of the newest leg · 🟩 / 🟥 = its newest T#. Every line
//            between the highest and lowest marker is ALWAYS drawn; the max
//            line setting only counts lines OUTSIDE that range.''', '''//  🟢 / 🔴 = T1 of the newest leg · 🟩 / 🟥 = its newest T#. Everything
//            between the highest and lowest marker is ALWAYS drawn; outside
//            it only "Max Items" show (50 / 50 bull / bear, husband & wife = 1;
//            0 = nothing outside).''')

# inputs
rep('''grp_cndl = "1. Auction State (Candles)"''', '''//@@TF_INPUTS@@

grp_cndl = "1. Auction State (Candles)"''')
rep('''maxLines     = input.int(10, "Max Lines Outside the 🟢🟩 Range", minval=0, maxval=100, group=grp_strc, tooltip="Lines between the highest and lowest 🟢🟩🔴🟥 marker are ALWAYS drawn, with their labels.\\nThis number only counts the lines OUTSIDE that range (newest first). 0 = none outside.")
''', '')
rep('''show_tn_step = input.bool(true, "Trend Markers 🟢🟩 / 🔴🟥", group=grp_strc, tooltip="🟢 / 🔴 = T1 of the newest leg (where it started).\\n🟩 / 🟥 = the newest T# of that leg.")
''', '''
//@@RANGE_INPUTS@@
//@@TN_INPUT@@
''')
rep('''gap_lbl_col     = input.color(color.white, "Text Color", inline="g5", group=grp_gaps)
''', '''gap_lbl_col     = input.color(color.white, "Text Color", inline="g5", group=grp_gaps)

//@@STATS_INPUTS@@
''')
# modules order
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
rep('''[gHi, gLo] = f_gateNow()
float candle_range''', '''float candle_range''')

# types / helpers, structure step, render
between('// TYPES & STATE\n', '// STEP 2 — STRUCTURE + VOIDS (confirmed bars only)\n', TYPES + '// ═══════════════════════════════════════════════════════════════\n')
between('// STEP 2 — STRUCTURE + VOIDS (confirmed bars only)\n', '    bool   fixedStop = gapExtMode == "3 Candles (Fixed)"\n', STEP2)
between('// RENDER — on the last bar everything structural is deleted and redrawn from\n', '//@@HTF_TABLE@@', RENDER)

# overlays: remember when they were born (for the marker-candle rule)
rep('''var label[] uh_lbls   = array.new<label>()
var float[] uh_prices = array.new<float>()
var label[] ul_lbls   = array.new<label>()
var float[] ul_prices = array.new<float>()''', '''var label[] uh_lbls   = array.new<label>()
var float[] uh_prices = array.new<float>()
var int[]   uh_t      = array.new<int>()
var label[] ul_lbls   = array.new<label>()
var float[] ul_prices = array.new<float>()
var int[]   ul_t      = array.new<int>()''')
rep('''                label.delete(uh_lbls.get(i))
                uh_lbls.remove(i)
                uh_prices.remove(i)''', '''                label.delete(uh_lbls.get(i))
                uh_lbls.remove(i)
                uh_prices.remove(i)
                uh_t.remove(i)''')
rep('''                label.delete(ul_lbls.get(i))
                ul_lbls.remove(i)
                ul_prices.remove(i)''', '''                label.delete(ul_lbls.get(i))
                ul_lbls.remove(i)
                ul_prices.remove(i)
                ul_t.remove(i)''')
rep('''            label.delete(uh_lbls.shift())
            uh_prices.shift()''', '''            label.delete(uh_lbls.shift())
            uh_prices.shift()
            uh_t.shift()''')
rep('''            label.delete(ul_lbls.shift())
            ul_prices.shift()''', '''            label.delete(ul_lbls.shift())
            ul_prices.shift()
            ul_t.shift()''')
rep('''        uh_prices.push(high)''', '''        uh_prices.push(high)
        uh_t.push(time)''')
rep('''        ul_prices.push(low)''', '''        ul_prices.push(low)
        ul_t.push(time)''')
rep('''        active_axs.push(AxData.new(lbl, tri, low, true))''', '''        active_axs.push(AxData.new(lbl, tri, low, true, time))''')
rep('''        active_axs.push(AxData.new(lbl, tri, high, false))''', '''        active_axs.push(AxData.new(lbl, tri, high, false, time))''')

open('/home/claude/v36/ofs37_template.pine', 'w').write(src)
print('ok', src.count('\n'))
