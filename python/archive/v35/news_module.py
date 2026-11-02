# Shared MMM news module (inputs + engine). Same code in every MMM indicator.
NEWS_INPUTS = '''grp_news     = "{grp}"
news_on      = input.bool(true, "Block Entries Around News", group=grp_news, tooltip="No new entry, and every NOT-YET-FILLED entry is cancelled, on a candle that touches a news window (New York time). Intraday charts only.")
news_builtin = input.bool(true, "Built-in: CPI · FOMC · NFP", group=grp_news, tooltip="Always-on safety list for the 3 biggest US events, all year (no paste needed).\\nCPI 08:30 · NFP first Friday 08:30 · FOMC 14:00 statement + 14:30 press conference (New York).\\nThe CPI / FOMC dates live in the two boxes at the bottom of this group.")
news_paste   = input.text_area("", "Pasted Calendar (from MMM News Converter)", group=grp_news, tooltip="Paste the lines made by the MMM News Converter page. One event per line:\\nYYYY-MM-DD HH:MM CUR I Title\\nTime = New York. I = H (red) · M (orange) · L (yellow) · N (grey).\\nExample: 2026-10-14 08:30 USD H CPI m/m\\nForexFactory only exports the CURRENT week, so paste once a week (Sunday / Monday). You can keep several weeks in the box.")
news_cur     = input.string("USD", "Currencies", group=grp_news, tooltip="Comma list of currencies to use from the pasted calendar. ES / NQ = USD.")
news_red     = input.bool(true,  "🔴 High", inline="imp", group=grp_news, tooltip="Which pasted impacts are used: red = High, orange = Medium, yellow = Low, grey = non-economic / holiday.")
news_org     = input.bool(false, "🟠 Medium", inline="imp", group=grp_news)
news_yel     = input.bool(false, "🟡 Low", inline="imp", group=grp_news)
news_gry     = input.bool(false, "⚪ Grey", inline="imp", group=grp_news)
news_pre     = input.int(5, "Block: Min Before", minval=0, maxval=120, inline="nw", group=grp_news)
news_post    = input.int(15, "Min After", minval=0, maxval=240, inline="nw", group=grp_news)
news_dot     = input.bool(true, "Warning Dot", inline="dot", group=grp_news, tooltip="A dot on the candle where the warning time sits (15 or 30 minutes before the news) — the closed candle or the live one. Hover it to read the event.")
news_dot_min = input.string("30", "Min Before", options=["15", "30"], inline="dot", group=grp_news)
news_dot_at  = input.string("High", "At", options=["High", "Low"], inline="dot", group=grp_news)
news_dot_txt = input.bool(false, "Name", inline="dot", group=grp_news)
news_bg      = input.bool(true, "Shade News Windows", group=grp_news)
cpi_dates    = input.text_area("2026-01-13,2026-02-13,2026-03-11,2026-04-10,2026-05-12,2026-06-10,2026-07-14,2026-08-12,2026-09-11,2026-10-14,2026-11-10,2026-12-10,2027-01-13,2027-02-11,2027-03-10,2027-04-13,2027-05-12,2027-06-10,2027-07-14,2027-08-11,2027-09-14,2027-10-14,2027-11-10,2027-12-10", "Built-in CPI Dates", group=grp_news, tooltip="Comma separated, New York date. Source: BLS release schedule.")
fomc_dates   = input.text_area("2025-01-29,2025-03-19,2025-05-07,2025-06-18,2025-07-30,2025-09-17,2025-10-29,2025-12-10,2026-01-28,2026-03-18,2026-04-29,2026-06-17,2026-07-29,2026-09-16,2026-10-28,2026-12-09,2027-01-27,2027-03-17,2027-04-28,2027-06-09,2027-07-28,2027-09-15,2027-10-27,2027-12-08", "Built-in FOMC Dates", group=grp_news, tooltip="Comma separated, decision day only. 2027 dates are tentative — check federalreserve.gov.")
'''

NEWS_ENGINE = '''// ═══════════════════════════════════════════════════════════════
// NEWS ENGINE (shared by every MMM indicator) — light: no library,
// no external request. Events = built-in CPI/FOMC/NFP + pasted calendar.
// ═══════════════════════════════════════════════════════════════
const string NWS_TZ = "America/New_York"

f_nwImpOk(string imp) =>
    imp == "H" ? news_red : imp == "M" ? news_org : imp == "L" ? news_yel : imp == "N" ? news_gry : false

f_nwCol(string imp) =>
    imp == "H" ? color.red : imp == "M" ? color.orange : imp == "L" ? color.yellow : color.gray

f_nwRank(string imp) =>
    imp == "H" ? 4 : imp == "M" ? 3 : imp == "L" ? 2 : 1

f_nwDate(string d, int hh, int mm) =>
    int t = na
    if str.length(d) == 10
        float y = str.tonumber(str.substring(d, 0, 4))
        float m = str.tonumber(str.substring(d, 5, 7))
        float dd = str.tonumber(str.substring(d, 8, 10))
        if not na(y) and not na(m) and not na(dd)
            t := timestamp(NWS_TZ, int(y), int(m), int(dd), hh, mm)
    t

var array<int>    nwT = array.new<int>()
var array<string> nwI = array.new<string>()
var array<string> nwN = array.new<string>()

if barstate.isfirst
    array<int>    tT = array.new<int>()
    array<string> tI = array.new<string>()
    array<string> tN = array.new<string>()
    if news_builtin
        for d in str.split(cpi_dates, ",")
            int t = f_nwDate(str.trim(d), 8, 30)
            if not na(t)
                tT.push(t)
                tI.push("H")
                tN.push("USD CPI")
        for d in str.split(fomc_dates, ",")
            int t1 = f_nwDate(str.trim(d), 14, 0)
            int t2 = f_nwDate(str.trim(d), 14, 30)
            if not na(t1)
                tT.push(t1)
                tI.push("H")
                tN.push("USD FOMC Statement")
                tT.push(t2)
                tI.push("H")
                tN.push("USD FOMC Press Conference")
        for y = 2024 to 2028
            for m = 1 to 12
                for dd = 1 to 7
                    int t = timestamp(NWS_TZ, y, m, dd, 8, 30)
                    if dayofweek(t, NWS_TZ) == dayofweek.friday
                        tT.push(t)
                        tI.push("H")
                        tN.push("USD NFP")
                        break
    string curList = "," + str.replace_all(str.upper(news_cur), " ", "") + ","
    for ln in str.split(str.replace_all(news_paste, ";", "\\n"), "\\n")
        array<string> tk = str.split(str.trim(ln), " ")
        if tk.size() >= 4
            string dS  = tk.get(0)
            string tS  = tk.get(1)
            string cur = str.upper(tk.get(2))
            string imp = str.upper(tk.get(3))
            if str.length(tS) == 5 and str.contains(curList, "," + cur + ",") and f_nwImpOk(imp)
                float hh = str.tonumber(str.substring(tS, 0, 2))
                float mm = str.tonumber(str.substring(tS, 3, 5))
                if not na(hh) and not na(mm)
                    int t = f_nwDate(dS, int(hh), int(mm))
                    if not na(t)
                        string ttl = cur
                        if tk.size() > 4
                            for k = 4 to tk.size() - 1
                                ttl += " " + tk.get(k)
                        tT.push(t)
                        tI.push(imp)
                        tN.push(ttl)
    if tT.size() > 0
        array<int> ord = tT.sort_indices(order.ascending)
        for k = 0 to ord.size() - 1
            nwT.push(tT.get(ord.get(k)))
            nwI.push(tI.get(ord.get(k)))
            nwN.push(tN.get(ord.get(k)))

int    nwPre   = news_pre * 60000
int    nwPost  = news_post * 60000
int    nwWarn  = (news_dot_min == "15" ? 15 : 30) * 60000
int    nwBarMs = timeframe.in_seconds(timeframe.period) * 1000
int    nwEnd   = nz(time_close, time + nwBarMs)
var int nwPtr  = 0
bool   nwHit   = false
string nwWarnTxt = ""
string nwWarnImp = ""
if timeframe.isintraday and nwT.size() > 0
    while nwPtr < nwT.size()
        if nwT.get(nwPtr) + math.max(nwPost, 0) < time
            nwPtr += 1
        else
            break
    if nwPtr < nwT.size()
        for j = nwPtr to nwT.size() - 1
            int et = nwT.get(j)
            if et - math.max(nwPre, nwWarn) >= nwEnd
                break
            if time < et + nwPost and nwEnd > et - nwPre
                nwHit := true
            int wt = et - nwWarn
            if wt >= time and wt < nwEnd
                nwWarnTxt += (str.length(nwWarnTxt) > 0 ? "\\n" : "") + str.format_time(et, "HH:mm", NWS_TZ) + " NY · " + nwI.get(j) + " · " + nwN.get(j)
                if str.length(nwWarnImp) == 0 or f_nwRank(nwI.get(j)) > f_nwRank(nwWarnImp)
                    nwWarnImp := nwI.get(j)
bool newsBlock = news_on and nwHit

bgcolor(news_bg and nwHit ? color.new(color.orange, 85) : na, title="News Window")

// Warning dot — on the candle holding (news time - 15/30 min), live or closed.
var label[] nwDots = array.new<label>()
if news_dot and str.length(nwWarnTxt) > 0
    color  dc   = f_nwCol(nwWarnImp)
    bool   atHi = news_dot_at == "High"
    string dTx  = news_dot_txt ? "◉ " + nwWarnTxt : ""
    label  dl   = label.new(bar_index, atHi ? high : low, dTx, yloc=atHi ? yloc.abovebar : yloc.belowbar, style=news_dot_txt ? (atHi ? label.style_label_down : label.style_label_up) : label.style_circle, color=news_dot_txt ? color(na) : dc, textcolor=dc, size=size.tiny, tooltip="News in " + news_dot_min + " min:\\n" + nwWarnTxt)
    if barstate.isconfirmed
        nwDots.push(dl)
        if nwDots.size() > 100
            label.delete(nwDots.shift())
'''
