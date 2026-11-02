from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment

FONT = "Arial"
HDR_FILL = PatternFill("solid", fgColor="000000")
TITLE_FILL = PatternFill("solid", fgColor="1A1A1A")
BULL = PatternFill("solid", fgColor="D9FFF4")
BEAR = PatternFill("solid", fgColor="F3E5F5")
INPUT_FILL = PatternFill("solid", fgColor="FFFF00")
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")

wb = Workbook()


def make_sheet(title, heading, headers, rows, widths, fills=None):
    ws = wb.create_sheet(title)
    ws.append([heading])
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
    c = ws.cell(row=1, column=1)
    c.font = Font(name=FONT, bold=True, size=13, color="27FFC3")
    c.fill = TITLE_FILL
    c.alignment = Alignment(vertical="center")
    ws.row_dimensions[1].height = 24
    ws.append(headers)
    for col in range(1, len(headers) + 1):
        h = ws.cell(row=2, column=col)
        h.font = Font(name=FONT, bold=True, color="FFFFFF")
        h.fill = HDR_FILL
        h.alignment = WRAP
        h.border = BORDER
    for i, r in enumerate(rows):
        ws.append(r)
        rr = ws.max_row
        for col in range(1, len(headers) + 1):
            cell = ws.cell(row=rr, column=col)
            cell.font = Font(name=FONT, bold=(col == 1))
            cell.alignment = WRAP
            cell.border = BORDER
            if fills and fills[i] is not None:
                cell.fill = fills[i]
    for idx, w in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + idx)].width = w
    ws.freeze_panes = "A3"
    return ws


# 1. Break Engines
make_sheet(
    "Break Engines",
    "MMM Order Flow Foundation — 3 break engines",
    ["Engine", "Letter", "Level watched", "Flip", "Continuation", "Event code", "Comes from", "Notes"],
    [
        ["Zone", "x", "BZ edge (BZH / BZL)", "CDLx / CDSx", "LDx / SDx", "ZBrk", "MMM Concepts Pro+",
         "BZ grows with FTB wicks (G1) or stays fixed (G0) — test both"],
        ["Candle", "c", "Last GMC of the other side", "CDLc / CDSc", "LDc / SDc", "CBrk", "MMM Pro / B&C",
         "Two test modes: c-O = close through the GMC Open; c-L = close through the whole GMC candle"],
        ["Swing", "s", "Swing High / Low locked by the first opposite BC", "CDLs / CDSs", "LDs / SDs", "SBrk",
         "MMM Order Flow Suite", "LD/SD only for swings made after the last flip; older swings deleted silently"],
        ["Single BC", "—", "Previous candle High / Low", "—", "—", "none (just BuBC / BeBC)", "All",
         "Any single body close needs no break code"],
        ["Break Origin Zone (BOZ)", "—", "Break Open (E2) ↔ Leg 50 (E6)", "—", "—", "—", "All engines",
         "Default entry area after a graded flip or continuation"],
    ],
    [22, 8, 34, 14, 14, 20, 22, 60],
)

# 2. Test Controls
make_sheet(
    "Test Controls",
    "Test controls — your questions and the rule for each",
    ["#", "Issue", "Fixable?", "Rule", "What to report"],
    [
        [1, "Same-candle order (fill / stop / target in one candle)", "Mostly",
         "Replay the test candle on its magnifier timeframe (see Magnifier Map). If one magnifier candle still holds two events: stop beats target; fill + target = filled, no win yet.",
         "Tie % = trades that needed the rule. Above 5% → use a smaller magnifier"],
        [2, "Look-ahead (repaint) bias", "Yes — 100%",
         "A level exists only from the close of the candle that confirms it. Limits go live on the next candle and keep their placed price. HTF values only from the last closed HTF candle.",
         "Nothing extra — it is a coding rule"],
        [3, "Trade timeout + BC trail (X4)", "Added",
         "X4: once in profit, the stop moves to the Low (long) / High (short) of each new same-direction BC that locks profit. At the next session open (18:00 → 02:00, 02:00 → 08:00, 08:30 → 09:30): in profit → keep trailing with X4; flat or losing → exit at that open.",
         "X4 as its own exit-mode column"],
        [4, "News (CPI / NFP / FOMC)", "Added",
         "Flag the days, block the windows (see News Windows). No new entries, unfilled limits cancelled.",
         "Every test twice: News Included vs News Blocked + news days on their own row"],
        [5, "Volatility", "Added",
         "S6 stop = k × ATR(14) of the test timeframe, k = 1.0 / 1.5 / 2.0. Fixed S0 (50 / 20 pts) stays the baseline.",
         "Every combo split low / mid / high by daily ATR(14) thirds"],
        [6, "HTF bias", "Added",
         "Compare B0–B4 (see HTF Bias) + origin tag on every HTF BC.",
         "Results per bias option and per origin tag"],
        [7, "Box growth", "Test switch",
         "G1 = grow with FTB wicks (default) vs G0 = edges fixed at the anchor candle.",
         "Same combos under G1 and G0 side by side"],
    ],
    [5, 34, 14, 80, 46],
)

# 3. Magnifier Map
make_sheet(
    "Magnifier Map",
    "Magnifier timeframe for each test timeframe",
    ["Test timeframe", "Magnifier timeframe", "Note"],
    [
        ["1H", "1m", "Shorter 1m history = fewer months tested"],
        ["15m", "1m", ""],
        ["5m", "1m", ""],
        ["1m", "5s", "Seconds charts need TradingView Premium"],
    ],
    [18, 22, 50],
)

# 4. News Windows
make_sheet(
    "News Windows",
    "News days — flagged and blocked (New York time)",
    ["Event", "Release time (ET)", "Blocked window (ET)", "Date source"],
    [
        ["CPI", "08:30", "08:25 – 08:45", "Date-list input (Pine has no event calendar)"],
        ["NFP", "08:30", "08:25 – 08:45", "First Friday of the month — check the exceptions"],
        ["FOMC", "14:00 statement / 14:30 press conference", "13:55 – 15:00", "Date-list input"],
    ],
    [12, 36, 22, 48],
)

# 5. HTF Bias
make_sheet(
    "HTF Bias",
    "HTF bias options — compare all",
    ["Code", "HTF bias = direction of…", "Note"],
    [
        ["B0", "None", "Baseline"],
        ["B1", "The last HTF BC", "Your current rule"],
        ["B2", "The last HTF ZBrk", ""],
        ["B3", "The last HTF CBrk", ""],
        ["B4", "The last HTF SBrk", ""],
        ["Origin tag", "ZBrk · CBrk · SBrk · Continuation (BC right after a same-side BC) · Plain",
         "Put on every HTF BC so results split by where the bias candle came from"],
    ],
    [14, 60, 56],
    fills=[None, BULL, None, None, None, None],
)

# 6. Switches
make_sheet(
    "Switches",
    "Structure switches — change one at a time against the default",
    ["Switch", "Option A", "Option B", "Option C", "Default", "Expected (to confirm with data)"],
    [
        ["BZ growth", "G1 grow with FTB wicks", "G0 fixed at anchor", "—", "G1",
         "G1: stop past liquidity already taken = fewer fake breaks. G0: earlier breaks, more fakes"],
        ["Candle engine mode", "c-O close through GMC Open", "c-L close through whole GMC candle", "—", "c-O",
         "c-L: fewer but stronger flips"],
        ["Break engine", "x zone", "c candle", "s swing", "—", "Same entries and stops → head-to-head"],
        ["News", "Included", "Blocked", "—", "Blocked (live)", "Shows the cost / gain of trading news"],
        ["Fill rule", "Touch", "Through (1 tick past)", "—", "Through", "Trust only results that hold under Through"],
    ],
    [22, 30, 34, 14, 16, 60],
)

# 7. Test Count (formulas)
ws = wb.create_sheet("Test Count")
ws.append(["Test count — change the yellow cells"])
ws.merge_cells("A1:C1")
ws["A1"].font = Font(name=FONT, bold=True, size=13, color="27FFC3")
ws["A1"].fill = TITLE_FILL
ws.append(["Item", "Value", "Meaning"])
for col in range(1, 4):
    h = ws.cell(row=2, column=col)
    h.font = Font(name=FONT, bold=True, color="FFFFFF")
    h.fill = HDR_FILL
    h.border = BORDER
rows = [
    ["Entries (E1–E6)", 6, "Break Close, Break Open, BZ edge, OC Zone, BZ 50, Leg 50"],
    ["Structural stops (S1–S6)", 6, "Break candle, broken edge, OCL/OCH, PL, protected swing, ATR"],
    ["Exit modes (X)", 6, "X1, X2-O, X2-C, X3-O, X3-C, X4"],
    ["Targets", 6, "1:2 to 1:7"],
    ["Luck rate at t = 2", 0.05, "About 5 in 100 combos pass by luck"],
    ["Combos per direction", "=B3*B4*B5", "Entries × stops × exit modes"],
    ["Fixed-stop baselines (S0)", "=B3", "One per entry"],
    ["Combo-target pairs", "=(B8+B9)*B6", "Every combo scored at every target"],
    ["Pairs passing by luck", "=ROUND(B10*B7,0)", "Why winners need t ≥ 3"],
]
for r in rows:
    ws.append(r)
for rr in range(3, ws.max_row + 1):
    for col in range(1, 4):
        cell = ws.cell(row=rr, column=col)
        cell.font = Font(name=FONT, bold=(col == 1))
        cell.border = BORDER
        cell.alignment = WRAP
for rr in range(3, 8):
    ws.cell(row=rr, column=2).fill = INPUT_FILL
    ws.cell(row=rr, column=2).font = Font(name=FONT, color="0000FF")
ws["B7"].number_format = "0%"
ws["B7"].comment = Comment("Standard 5% false-positive rate at t = 2 (about 95% confidence).", "Claude")
ws.column_dimensions["A"].width = 30
ws.column_dimensions["B"].width = 12
ws.column_dimensions["C"].width = 62
ws.freeze_panes = "A3"

del wb["Sheet"]
wb.save("MMM_Order_Flow_Foundation.xlsx")
print("saved")
