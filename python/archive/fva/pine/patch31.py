"""Fair Value Area Break 3.0 -> 3.1: honest trade grading."""
import re
src = '\n'.join(l.rstrip() for l in open('/home/claude/fva/pine/fva_3.0.pine', encoding='utf-8').read().replace('\r\n', '\n').split('\n'))
s = src


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f'expected {count} x {old[:80]!r}, found {n}')
    s = s.replace(old, new)


# ── title
rep('indicator("MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.0", "Fair Value Area Break @MaxMaserati 3.0",',
    'indicator("MMM Perfect Entry: Fair Value Area Break @MaxMaserati 3.1", "Fair Value Area Break @MaxMaserati 3.1",')

# ── history: stats on 500 bars = about one week of 15m
rep('max_bars_back  = input.int(500, "Max History Bars", minval=100, maxval=20000, group=group_global)',
    'max_bars_back  = input.int(2000, "Max History Bars", minval=100, maxval=20000, group=group_global, tooltip="Bars used to build setups and the stats table. 2000 bars of 15m = about one month. More bars = more trades in the stats, slower load.")')

# ── entry tooltips with the Oct 2026 re-test (NQ 15m Dec 2022 - Dec 2025, real fills, 1m check)
T = {
    'usePesPelPoc       = input.bool(true, "① PES/PEL Touch", group=grp_entry_types, tooltip="Limit entry directly at the Point of Control (highest volume price) of the originating FVA block.")':
    'usePesPelPoc       = input.bool(true, "① PES/PEL Touch", group=grp_entry_types, tooltip="Limit entry directly at the Point of Control (highest volume price) of the originating FVA block.\\nRe-test NQ 15m 2023-25 (real fills): WR 29.5% · PF 0.84 · avg RR −0.11 · t-score −9.4.")',
    'usePesPelPlusPoc   = input.bool(true, "② PES/PEL+ Touch", group=grp_entry_types, tooltip="High-conviction limit entry at the POC specifically following a major trend flip.")':
    'usePesPelPlusPoc   = input.bool(true, "② PES/PEL+ Touch", group=grp_entry_types, tooltip="High-conviction limit entry at the POC specifically following a major trend flip.\\nRe-test NQ 15m 2023-25 (real fills): box stop WR 37.1% · avg RR +0.11 (−0.11 after fees) · fixed 50 pt stop at 1:2: WR 39.4% · avg RR +0.18 · t-score 5.1.")',
    'useCdlCdsBlock     = input.bool(true, "③ CDL/CDS Touch", group=grp_entry_types, tooltip="Limit entry directly at the structural boundary (midpoint) of the originating FVA block.")':
    'useCdlCdsBlock     = input.bool(true, "③ CDL/CDS Touch", group=grp_entry_types, tooltip="Limit entry directly at the structural boundary (midpoint) of the originating FVA block.\\nRe-test NQ 15m 2023-25 (real fills): WR 31.1% · PF 0.91 · avg RR −0.06 · t-score −4.9.")',
    'useCdlCdsPlusBlock = input.bool(true, "④ CDL/CDS+ Touch", group=grp_entry_types, tooltip="Entry at the structural boundary following a major trend flip.")':
    'useCdlCdsPlusBlock = input.bool(true, "④ CDL/CDS+ Touch", group=grp_entry_types, tooltip="Entry at the structural boundary following a major trend flip.\\nBEST ENTRY. Re-test NQ 15m 2023-25 (real fills): WR 41.1% · PF 1.40 · avg RR +0.23 · t-score 7.3 · +0.13 after fees, positive every year. NQ 1h +0.22, MNQ 15m 2026 +0.26.")',
    'useNestedPoc        = input.bool(true, "Nested PES/PEL", inline="ne1", group=grp_nested_entry, tooltip="Triggers when price forms a new POC inside a larger active consolidation structure.")':
    'useNestedPoc        = input.bool(true, "Nested PES/PEL", inline="ne1", group=grp_nested_entry, tooltip="Triggers when price forms a new POC inside a larger active consolidation structure.\\nRe-test NQ 15m 2023-25 (real fills): WR 30.7% · avg RR −0.08.")',
    'useNestedBlock      = input.bool(true, "Nested CDL/CDS", inline="ne3", group=grp_nested_entry, tooltip="Triggers when price forms a block entry entirely inside an older structure.")':
    'useNestedBlock      = input.bool(true, "Nested CDL/CDS", inline="ne3", group=grp_nested_entry, tooltip="Triggers when price forms a block entry entirely inside an older structure.\\nRe-test NQ 15m 2023-25 (real fills): WR 33.3% · avg RR +0.01 (−0.22 after fees).")',
}
for a, b in T.items():
    rep(a, b)

# ⑤ / ⑥ entry point: the candle OPEN is a price already gone when the candle closes
rep('useBuxBexEntry   = input.bool(true, "Enable ⑤ BuX (Long) / BeX (Short) Entry", group=grp_buxbex_entry, tooltip="Momentum entry directly on the breakout expansion candle.")',
    'useBuxBexEntry   = input.bool(true, "Enable ⑤ BuX (Long) / BeX (Short) Entry", group=grp_buxbex_entry, tooltip="Momentum entry directly on the breakout expansion candle.\\nRe-test NQ 15m 2023-25 (market at close): WR 33.6% · avg RR +0.01 · t-score 0.8 (no edge).")')
rep('buxBexEntryPoint = input.string("Open", "Entry Point on Candle", options=["Close", "Open", "50% High-Low", "50% Open-Close"], group=grp_buxbex_entry)',
    'buxBexEntryPoint = input.string("Close", "Entry Point on Candle", options=["Close", "Open", "50% High-Low", "50% Open-Close"], group=grp_buxbex_entry, tooltip="Close = market order when the candle closes (the real price you can get).\\nOpen / 50% = a limit order working from the NEXT candle. It is skipped if the target comes first.")')
rep('useLqgEntry   = input.bool(true, "⑥ Enable LQG Break Momentum Entry", group=grp_lqg_entry, tooltip="Momentum entry directly on the candle that confirms an LQG liquidity sweep.")',
    'useLqgEntry   = input.bool(true, "⑥ Enable LQG Break Momentum Entry", group=grp_lqg_entry, tooltip="Momentum entry directly on the candle that confirms an LQG liquidity sweep.\\nRe-test NQ 15m 2023-25 (market at close): WR 33.7% · avg RR +0.01 · t-score 0.6 (no edge).")')
rep('lqgEntryPoint = input.string("Open", "Entry Point on Candle", options=["Close", "Open", "50% High-Low", "50% Open-Close"], group=grp_lqg_entry)',
    'lqgEntryPoint = input.string("Close", "Entry Point on Candle", options=["Close", "Open", "50% High-Low", "50% Open-Close"], group=grp_lqg_entry, tooltip="Close = market order when the candle closes.\\nOpen / 50% = a limit order working from the NEXT candle. It is skipped if the target comes first.")')

# ── grading + fees inputs (risk group)
rep('cancelOnOppositeBreak = input.bool(false, "Emergency Exit on Opposite Structure Break", group=grp_risk, tooltip="Automatically cancels pending orders if the market structure flips to the opposite bias before entry.")',
    'cancelOnOppositeBreak = input.bool(false, "Emergency Exit on Opposite Structure Break", group=grp_risk, tooltip="Automatically cancels pending orders if the market structure flips to the opposite bias before entry.")\n'
    'useIntrabar        = input.bool(true, "Grade Trades With Intrabar Data", inline="ib", group=grp_risk, tooltip="Reads the small candles inside each chart candle, in order, to see what really came first: the entry, the stop or the target.\\nA small candle that touches both the stop and the target counts as a LOSS. With no intrabar data (old history), a chart candle that touches both counts as a loss and the target never counts on the fill candle.")\n'
    'ibTF               = input.timeframe("1", "", inline="ib", group=grp_risk)\n'
    'feePerContract     = input.float(1.50, "Fees per Contract, Round Trip ($)", minval=0.0, step=0.1, group=grp_risk, tooltip="Commission + exchange fees for one contract in and out. Micros about $1.50, minis about $4.50. Taken off every closed trade in the stats.")')

# ── EntrySignal: start grading on the next candle (market entries at the close, limits placed after the close)
rep('    bool    forceExit\n    string  forceExitReason\n', '    bool    forceExit\n    string  forceExitReason\n    bool    startNext\n')
rep('createTrade(bool isLong, float ep, float slIn, string entryType, int tid, bool activateNow = false) =>',
    'createTrade(bool isLong, float ep, float slIn, string entryType, int tid, bool activateNow = false, bool startNext = false) =>')
rep('_aRisk, na, na, true, ps, false, "")'.replace('_aRisk', 'aRisk'), 'aRisk, na, na, true, ps, false, "", startNext)')

# touch + BuX/BeX confirmation entries are market orders at the close
s, k = re.subn(r'createTrade\((true|false), close, _slP, (e_poc_name|e_blk_name), globalTradeId\)',
               r'createTrade(\1, close, _slP, \2, globalTradeId, true, true)', s)
assert k == 8, k
rep('createTrade(true, ep, _sl - (stopLossTicks * tickSize), "⑥ LQG", globalTradeId)',
    'createTrade(true, ep, _sl - (stopLossTicks * tickSize), "⑥ LQG", globalTradeId, lqgEntryPoint == "Close", true)')
rep('createTrade(false, ep, _sl + (stopLossTicks * tickSize), "⑥ LQG", globalTradeId)',
    'createTrade(false, ep, _sl + (stopLossTicks * tickSize), "⑥ LQG", globalTradeId, lqgEntryPoint == "Close", true)')
rep('createTrade(true, ep, _slBux, "⑤ BuX", globalTradeId)', 'createTrade(true, ep, _slBux, "⑤ BuX", globalTradeId, buxBexEntryPoint == "Close", true)', 2)
rep('createTrade(false, ep, _slBex, "⑤ BeX", globalTradeId)', 'createTrade(false, ep, _slBex, "⑤ BeX", globalTradeId, buxBexEntryPoint == "Close", true)', 2)

# ── intrabar data + grading function + stats accumulators (before TRADE CREATION)
GRADE = '''// ═══════════════════════════════════════════════════════════════════════
// TRADE GRADING (3.1) — what really came first
// ═══════════════════════════════════════════════════════════════════════
// 3.0 graded a trade on the candle that created it, read the target before the stop,
// and filled ⑤/⑥ at the candle open after it closed. That showed ~87% WR.
// 3.1: market entries (close) and limits placed after a close start on the NEXT candle,
// touch limits fill at the first intrabar that touches them, the stop is read first,
// the target never counts in the fill intrabar, and fees come off every trade.
string ibTFuse = timeframe.in_seconds(ibTF) < timeframe.in_seconds(timeframe.period) ? ibTF : timeframe.period
[ibH, ibL] = request.security_lower_tf(syminfo.tickerid, ibTFuse, [high, low])

// returns [result, activated]: result 0 = still open / pending · 1 = target · -1 = stop · 2 = missed (target before entry)
f_grade(bool isLong, float ep, float sl, float tp, bool actIn) =>
    bool act = actIn
    int  res = 0
    int  n   = useIntrabar and not na(ibH) ? array.size(ibH) : 0
    if n > 0
        for k = 0 to n - 1
            float hh = array.get(ibH, k)
            float ll = array.get(ibL, k)
            if na(hh) or na(ll)
                continue
            if not act
                if isLong ? ll <= ep : hh >= ep
                    act := true
                    if isLong ? ll <= sl : hh >= sl
                        res := -1
                        break
                else if isLong ? hh >= tp : ll <= tp
                    res := 2
                    break
            else
                if isLong ? ll <= sl : hh >= sl
                    res := -1
                    break
                if isLong ? hh >= tp : ll <= tp
                    res := 1
                    break
    else
        if not act
            if isLong ? low <= ep : high >= ep
                act := true
                if isLong ? low <= sl : high >= sl
                    res := -1
            else if isLong ? high >= tp : low <= tp
                res := 2
        else
            if isLong ? low <= sl : high >= sl
                res := -1
            else if isLong ? high >= tp : low <= tp
                res := 1
    [res, act]

// stats in risk units: [sum avg RR, sum of squares, trades] and per entry type
var float[] statR = array.new_float(3, 0.0)
var int[]   catW  = array.new_int(8, 0)
var int[]   catL  = array.new_int(8, 0)
var float[] catR  = array.new_float(8, 0.0)

f_cat(string ct) =>
    str.contains(ct, "Nested") and str.contains(ct, "PES/PEL") ? 0 : str.contains(ct, "Nested") and str.contains(ct, "CDL/CDS") ? 1 : str.contains(ct, "①") ? 2 : str.contains(ct, "②") ? 3 : str.contains(ct, "③") ? 4 : str.contains(ct, "④") ? 5 : str.contains(ct, "⑤") ? 6 : 7

f_book(string ct, float rr) =>
    int c = f_cat(ct)
    array.set(statR, 0, array.get(statR, 0) + rr)
    array.set(statR, 1, array.get(statR, 1) + rr * rr)
    array.set(statR, 2, array.get(statR, 2) + 1)
    if rr >= 0
        array.set(catW, c, array.get(catW, c) + 1)
    else
        array.set(catL, c, array.get(catL, c) + 1)
    array.set(catR, c, array.get(catR, c) + rr)
    c

f_avgTx(float sumR, int n) =>
    n > 0 ? (sumR / n >= 0 ? "+" : "") + str.tostring(sumR / n, "0.00") : "—"

'''
rep('''// ═══════════════════════════════════════════════════════════════════════
// TRADE CREATION
// ═══════════════════════════════════════════════════════════════════════''',
    GRADE + '''// ═══════════════════════════════════════════════════════════════════════
// TRADE CREATION
// ═══════════════════════════════════════════════════════════════════════''')

# ── Layer 1 visual hiding: not on the creation candle of next-candle trades
rep('''            bool hitEntry = _tcv.isLong ? (low <= _tcv.entryPrice) : (high >= _tcv.entryPrice)
            bool isAct = _tcv.activated or hitEntry''',
    '''            bool _waitNext = _tcv.startNext and bar_index == _tcv.creationBar
            bool hitEntry = not _waitNext and (_tcv.isLong ? (low <= _tcv.entryPrice) : (high >= _tcv.entryPrice))
            bool isAct = (_tcv.activated and not _waitNext) or hitEntry''')

# ── Layer 3 grading
rep('''            if not _tc2.activated
                bool hitEntry = _tc2.isLong ? (low <= _tc2.entryPrice) : (high >= _tc2.entryPrice)
                if hitEntry
                    _tc2.activated := true
                else
                    bool hitTpEarly = _tc2.isLong ? (high >= _tc2.takeProfit) : (low <= _tc2.takeProfit)
                    bool hitSlEarly = _tc2.isLong ? (low <= _tc2.stopLoss) : (high >= _tc2.stopLoss)
                    if hitTpEarly or hitSlEarly
                        _tc2.forceExit := true
                        _tc2.forceExitReason := "Missed (TGT/SL Hit Before Entry)"

            if _tc2.activated and not _tc2.forceExit
                float _riskDist2 = math.abs(_tc2.entryPrice - _tc2.stopLoss)
                bool _tpH2 = _tc2.isLong ? (high >= _tc2.takeProfit) : (low  <= _tc2.takeProfit)
                bool _slH2 = _tc2.isLong ? (low  <= _tc2.stopLoss) : (high >= _tc2.stopLoss)

                if _tpH2 or _slH2
                    bool isWin = _tpH2
                    _tc2.outcome := isWin ? "win" : "loss"
                    float _exitPrice2  = isWin ? _tc2.takeProfit : _tc2.stopLoss
                    float _finalDist2  = _tc2.isLong ? (_exitPrice2 - _tc2.entryPrice) : (_tc2.entryPrice - _exitPrice2)
                    float _pnl2        = (_finalDist2 / math.max(_riskDist2, syminfo.mintick)) * _tc2.actualRiskDollars
                    float _rr2         = _pnl2 / math.max(_tc2.actualRiskDollars, 1e-9)

                    string _ct = _tc2.candleType''',
    '''            int  _g2     = 0
            bool _wait2  = _tc2.startNext and bar_index == _tc2.creationBar
            if not _wait2 and not _tc2.forceExit
                [_gr2, _ac2] = f_grade(_tc2.isLong, _tc2.entryPrice, _tc2.stopLoss, _tc2.takeProfit, _tc2.activated)
                _g2 := _gr2
                _tc2.activated := _ac2
                if _g2 == 2
                    _tc2.forceExit := true
                    _tc2.forceExitReason := "Missed (TGT Hit Before Entry)"

            if _tc2.activated and not _tc2.forceExit
                float _riskDist2 = math.abs(_tc2.entryPrice - _tc2.stopLoss)

                if _g2 == 1 or _g2 == -1
                    bool isWin = _g2 == 1
                    _tc2.outcome := isWin ? "win" : "loss"
                    float _exitPrice2  = isWin ? _tc2.takeProfit : _tc2.stopLoss
                    float _finalDist2  = _tc2.isLong ? (_exitPrice2 - _tc2.entryPrice) : (_tc2.entryPrice - _exitPrice2)
                    float _pnl2        = (_finalDist2 / math.max(_riskDist2, syminfo.mintick)) * _tc2.actualRiskDollars - _tc2.positionSize * feePerContract
                    float _rr2         = _pnl2 / math.max(_tc2.actualRiskDollars, 1e-9)

                    string _ct = _tc2.candleType
                    f_book(_ct, _rr2)''')

rep('''                        float _xPnl  = (_xDist / math.max(_rP, syminfo.mintick)) * _tc2.actualRiskDollars
                        float _xRR   = _xDist / math.max(_rP, syminfo.mintick)

                        string _ct = _tc2.candleType''',
    '''                        float _xPnl  = (_xDist / math.max(_rP, syminfo.mintick)) * _tc2.actualRiskDollars - _tc2.positionSize * feePerContract
                        float _xRR   = _xPnl / math.max(_tc2.actualRiskDollars, 1e-9)

                        string _ct = _tc2.candleType
                        f_book(_ct, _xRR)''')

# ── stats table: real-fill header, avg RR, t-score, fees, by-entry avg RR
rep('var table _sT = table.new(getTablePosition(statsTablePos), 3, 28,', 'var table _sT = table.new(getTablePosition(statsTablePos), 3, 34,')
rep('''    table.cell(_sT, 0, st, "═ STATISTICS ═", bgcolor=#000000, text_color=#e1b31a, text_size=getTableTextSize(_sz))
    table.merge_cells(_sT, 0, st, 2, st)
    st += 1''',
    '''    table.cell(_sT, 0, st, "═ STATISTICS · REAL FILLS ═", bgcolor=#000000, text_color=#e1b31a, text_size=getTableTextSize(_sz))
    table.merge_cells(_sT, 0, st, 2, st)
    st += 1
    bool _ibOn = useIntrabar and timeframe.in_seconds(ibTFuse) < timeframe.in_seconds(timeframe.period)
    table.cell(_sT, 0, st, "Grading",      bgcolor=#000000, text_color=color.rgb(210,210,210), text_size=getTableTextSize(_sz))
    table.cell(_sT, 1, st, (_ibOn ? ibTFuse + "m intrabar" : "chart candles") + " · stop first", bgcolor=#000000, text_color=color.white, text_size=getTableTextSize(_sz))
    table.merge_cells(_sT, 1, st, 2, st)
    st += 1''')
rep('table.cell(_sT, 0, st, "WR / RR",     bgcolor=_rr_bg,', 'table.cell(_sT, 0, st, "WR (win rate) / RR", bgcolor=_rr_bg,')
rep('table.cell(_sT, 0, st, "Need",          bgcolor=_rr_bg,', 'table.cell(_sT, 0, st, "WR needed",     bgcolor=_rr_bg,')
rep('table.cell(_sT, 0, st, "Avg R W/L",   bgcolor=#000000,', 'table.cell(_sT, 0, st, "avg RR W/L",  bgcolor=#000000,')
rep('''    table.cell(_sT, 0, st, "Prof Factor", bgcolor=#000000, text_color=color.rgb(210,210,210), text_size=getTableTextSize(_sz))
    table.cell(_sT, 1, st, _pfTx, bgcolor=#000000, text_color=_pfCl, text_size=getTableTextSize(_sz))
    table.merge_cells(_sT, 1, st, 2, st)
    st += 1''',
    '''    table.cell(_sT, 0, st, "PF (profit factor)", bgcolor=#000000, text_color=color.rgb(210,210,210), text_size=getTableTextSize(_sz))
    table.cell(_sT, 1, st, _pfTx, bgcolor=#000000, text_color=_pfCl, text_size=getTableTextSize(_sz))
    table.merge_cells(_sT, 1, st, 2, st)
    st += 1
    float _sR  = array.get(statR, 0)
    float _sR2 = array.get(statR, 1)
    int   _nR  = int(array.get(statR, 2))
    float _aR  = _nR > 0 ? _sR / _nR : na
    float _sdR = _nR > 1 ? math.sqrt(math.max((_sR2 - _sR * _sR / _nR) / (_nR - 1), 0.0)) : na
    float _tS  = _nR > 1 and _sdR > 0 ? _aR / (_sdR / math.sqrt(_nR)) : na
    table.cell(_sT, 0, st, "avg RR / trade", bgcolor=#000000, text_color=color.rgb(210,210,210), text_size=getTableTextSize(_sz))
    table.cell(_sT, 1, st, f_avgTx(_sR, _nR), bgcolor=#000000, text_color=na(_aR) ? color.gray : _aR > 0 ? color.lime : color.red, text_size=getTableTextSize(_sz))
    table.merge_cells(_sT, 1, st, 2, st)
    st += 1
    table.cell(_sT, 0, st, "t-score",     bgcolor=#000000, text_color=color.rgb(210,210,210), text_size=getTableTextSize(_sz))
    table.cell(_sT, 1, st, na(_tS) ? "—" : str.tostring(_tS, "0.0") + (_tS >= 2 ? "  edge" : _tS <= -2 ? "  losing" : "  luck zone"), bgcolor=#000000, text_color=na(_tS) ? color.gray : _tS >= 2 ? color.lime : _tS <= -2 ? color.red : color.orange, text_size=getTableTextSize(_sz))
    table.merge_cells(_sT, 1, st, 2, st)
    st += 1
    table.cell(_sT, 0, st, "Fees",        bgcolor=#000000, text_color=color.rgb(210,210,210), text_size=getTableTextSize(_sz))
    table.cell(_sT, 1, st, "$" + str.tostring(feePerContract, "0.00") + " / contract", bgcolor=#000000, text_color=color.white, text_size=getTableTextSize(_sz))
    table.merge_cells(_sT, 1, st, 2, st)
    st += 1''')
rep('''    table.cell(_sT, 0, st, "── BY ENTRY ──", bgcolor=#000000, text_color=#e1b31a, text_size=getTableTextSize(_sz))
    table.merge_cells(_sT, 0, st, 2, st)
    st += 1''',
    '''    table.cell(_sT, 0, st, "── BY ENTRY ──", bgcolor=#000000, text_color=#e1b31a, text_size=getTableTextSize(_sz))
    table.cell(_sT, 1, st, "W/L (WR)", bgcolor=#000000, text_color=#e1b31a, text_size=getTableTextSize(_sz))
    table.cell(_sT, 2, st, "avg RR", bgcolor=#000000, text_color=#e1b31a, text_size=getTableTextSize(_sz))
    st += 1''')
# by-entry rows: W/L in col 1, avg RR in col 2 (no merge)
for wins, losses, idx in [('pocWins, pocLosses', None, 2), ('pocPlusWins, pocPlusLosses', None, 3), ('blockWins, blockLosses', None, 4),
                          ('blockPlusWins, blockPlusLosses', None, 5), ('nestPocW, nestPocL', None, 0), ('nestBlkW, nestBlkL', None, 1),
                          ('buxbexWins, buxbexLosses', None, 6), ('lqgWins, lqgLosses', None, 7)]:
    old = f'table.cell(_sT, 1, st, f_wl({wins}), bgcolor=#000000, text_color=color.white, text_size=getTableTextSize(_sz))\n        table.merge_cells(_sT, 1, st, 2, st)'
    new = (f'table.cell(_sT, 1, st, f_wl({wins}), bgcolor=#000000, text_color=color.white, text_size=getTableTextSize(_sz))\n'
           f'        float _cr{idx} = array.get(catR, {idx})\n'
           f'        int _cn{idx} = array.get(catW, {idx}) + array.get(catL, {idx})\n'
           f'        table.cell(_sT, 2, st, f_avgTx(_cr{idx}, _cn{idx}), bgcolor=#000000, text_color=_cn{idx} == 0 ? color.gray : _cr{idx} > 0 ? color.lime : color.red, text_size=getTableTextSize(_sz))')
    rep(old, new)

# alerts: say market or limit
rep('''_alertMsg := t.entryText + " | " + t.direction + " Limit @ "''',
    '''_alertMsg := t.entryText + " | " + t.direction + (t.activated ? " Market @ " : " Limit @ ")''')

open('/home/claude/fva/pine/MMM_FVA_Break_3.1.pine', 'w', encoding='utf-8').write(s)
print('ok', s.count('\n') + 1, 'lines')
