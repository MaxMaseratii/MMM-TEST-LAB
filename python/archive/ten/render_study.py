# -*- coding: utf-8 -*-
import json
S=json.load(open('/home/claude/ten/study_sections.json'))
TITLE='9:30 AM to 11:30 AM Testing Studies'
CSS=r"""
:root{--bg:#07080a;--panel:#0f1114;--panel2:#0b0d10;--row:#14171b;--row2:#101317;--line:#252a31;--line2:#333a43;--fg:#d9dde3;--mute:#8f97a1;--gold:#e1b31a;--gold2:#f2cf5b;--teal:#4fd1c5;--up:#3ddc97;--dn:#ff5c6c;
--display:'Barlow Condensed','Arial Narrow',sans-serif;--body:'Barlow',system-ui,sans-serif;--mono:'IBM Plex Mono',ui-monospace,monospace;color-scheme:dark}
html,body{background:var(--bg);color:var(--fg)}
body{font-family:var(--body);font-size:16px;margin:0;-webkit-font-smoothing:antialiased}
.wrap{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:28px 64px}
.doc{max-width:1060px;margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr);gap:18px}
.cover{border:1px solid var(--line);background:radial-gradient(900px 280px at 0% 0%,rgba(225,179,26,.12),transparent 70%),var(--panel);padding:26px 24px 22px;border-top:3px solid var(--gold)}
.eyebrow{font:600 13px/1 var(--display);letter-spacing:.14em;text-transform:uppercase;color:var(--teal)}
.cover h1{font-family:var(--display);font-weight:700;letter-spacing:.03em;text-transform:uppercase;color:var(--gold);font-size:clamp(32px,5vw,54px);line-height:1;margin:10px 0 12px;text-wrap:balance}
.cover p.lede{font-size:17.5px;line-height:1.55;color:#cfd5da;max-width:72ch;margin:0}
.meta{display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:16px;font:600 13px/1.4 var(--mono);color:var(--mute)}
.meta b{color:var(--gold2);font-weight:600}
.min{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:10px}
.min div{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--gold);padding:12px 14px}
.min div.no{border-left-color:var(--dn)}
.min b{display:block;font:700 16px/1.15 var(--display);letter-spacing:.06em;text-transform:uppercase;color:var(--gold);margin-bottom:5px}
.min div.no b{color:var(--dn)}
.min p{margin:0;line-height:1.5;color:#d4dae0}
nav.toc{background:var(--panel2);border:1px solid var(--line);padding:12px 14px}
nav.toc h2{margin:0 0 8px;font:700 15px/1 var(--display);letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
nav.toc ol{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:4px 18px}
nav.toc a{color:#d4dae0;text-decoration:none;line-height:1.5}
nav.toc a span{display:inline-block;min-width:28px;font:600 13px var(--mono);color:var(--gold)}
nav.toc a:hover{color:var(--gold2)}
section.s{background:var(--panel);border:1px solid var(--line);min-width:0;scroll-margin-top:90px}
.sh{display:flex;gap:14px;align-items:flex-start;padding:14px 16px;border-bottom:1px solid var(--line)}
.sh .n{flex:0 0 auto;font:700 22px/1 var(--display);color:#0b0b0b;background:var(--gold);min-width:38px;height:38px;display:grid;place-items:center}
.sh h2{margin:0;font:700 clamp(21px,2.4vw,27px)/1.1 var(--display);letter-spacing:.04em;text-transform:uppercase;color:var(--gold);text-wrap:balance}
.sh h2 small{display:block;font:600 13.5px/1.3 var(--display);letter-spacing:.08em;color:var(--mute);margin-top:4px}
.sb{padding:14px 16px 16px;display:grid;gap:12px;min-width:0}
.sb ul.f{list-style:disc;margin:0;padding-left:20px;display:grid;gap:6px;line-height:1.6;max-width:90ch}
.sb ul.f b{color:var(--gold2)} .sb ul.f li::marker,.best li::marker{color:var(--gold)}
.tw{overflow:auto;border:1px solid var(--line)}
table{border-collapse:collapse;width:100%;font-family:var(--mono);font-size:13px;font-variant-numeric:tabular-nums}
th{background:#000;color:var(--gold);text-align:left;font:600 13.5px/1.25 var(--display);letter-spacing:.04em;text-transform:uppercase;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:bottom}
td{padding:7px 10px;border-bottom:1px solid #1a1e23;white-space:nowrap}
td:first-child{font-family:var(--body);font-weight:600;color:var(--fg)}
tbody tr:nth-child(odd){background:var(--row)} tbody tr:nth-child(even){background:var(--row2)}
.note{margin:0;color:var(--mute);font-size:14px;line-height:1.5;max-width:95ch}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:8px;margin:0}
.kpis div{background:var(--panel2);border:1px solid var(--line);padding:9px 11px}
.kpis dt{font:600 12.5px/1.3 var(--display);text-transform:uppercase;letter-spacing:.06em;color:var(--mute)}
.kpis dd{margin:4px 0 0;font:600 17px/1.25 var(--mono)}
.best{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));gap:10px}
.best div{background:var(--panel2);border:1px solid var(--line);border-left:3px solid var(--teal);padding:11px 13px}
.best b{display:block;font:700 20px/1 var(--display);letter-spacing:.05em;color:var(--teal);margin-bottom:6px}
.best ul{list-style:disc;margin:0;padding-left:18px;display:grid;gap:4px;line-height:1.5;color:#d4dae0}
ol.steps{list-style:none;margin:0;padding:0;display:grid;gap:0;counter-reset:s}
ol.steps li{counter-increment:s;display:grid;grid-template-columns:34px 140px minmax(0,1fr);gap:10px;padding:10px 0;border-top:1px solid var(--line);line-height:1.55}
ol.steps li:first-child{border-top:0}
ol.steps li::before{content:counter(s);font:700 15px/1 var(--display);color:#0b0b0b;background:var(--teal);width:26px;height:26px;display:grid;place-items:center}
ol.steps b{font:700 15px/1.3 var(--display);letter-spacing:.05em;text-transform:uppercase;color:var(--fg)}
dl.defs{margin:0;display:grid;grid-template-columns:170px minmax(0,1fr);gap:0}
dl.defs dt,dl.defs dd{padding:8px 10px;border-top:1px solid var(--line);margin:0;line-height:1.5}
dl.defs dt{font:600 13.5px/1.5 var(--mono);color:var(--gold2)}
dl.defs dd{color:#d4dae0}
.links{display:flex;flex-wrap:wrap;gap:10px}
.links a{font:700 15px/1 var(--display);letter-spacing:.07em;text-transform:uppercase;text-decoration:none;padding:12px 16px;border:1px solid var(--line2);color:var(--fg);background:var(--panel)}
.links a.try{background:var(--gold);color:#0b0b0b;border-color:var(--gold)}
.links button{font:700 15px/1 var(--display);letter-spacing:.07em;text-transform:uppercase;padding:12px 16px;border:1px solid var(--line2);color:var(--fg);background:var(--panel);cursor:pointer}
.legal{color:var(--mute);font-size:13px;line-height:1.5;margin:0}
a:focus-visible,button:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
@media (max-width:640px){ol.steps li{grid-template-columns:30px minmax(0,1fr)} ol.steps li span{grid-column:2} dl.defs{grid-template-columns:minmax(0,1fr)} dl.defs dd{border-top:0;padding-top:0}}
@media print{body{background:#fff;color:#111} .wrap{padding:0} #mmm-header,#mmm-footer,.links,nav.toc{display:none!important} .cover,.min div,section.s,.kpis div,.best div,nav.toc{background:#fff!important;border-color:#bbb!important;color:#111} .cover h1,.sh h2,.min b,th{color:#7a5d00!important} th{background:#f2f2f2!important} td,td:first-child,.min p,.sb ul.f,.best ul,dl.defs dd,.cover p.lede{color:#111!important} tbody tr:nth-child(odd),tbody tr:nth-child(even){background:#fff!important} section.s{break-inside:avoid}}
"""
def table(t):
    return '<div class="tw"><table><thead><tr>'+''.join(f'<th>{h}</th>' for h in t['h'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in t['rows'])+'</tbody></table></div>'
def body():
    out=[]
    out.append(f'''<header class="cover"><span class="eyebrow">MMM research desk · study document</span><h1>{TITLE}</h1>
<p class="lede">Everything tested on the New York morning, the two hours Max trades: when the high and low are made, what the 09:30 and 10:00 MMM candles tell you, the opening range, the opening gaps, and how far a run of body closes goes before the other side closes. In one document, in plain words.</p>
<div class="meta"><span><b>Updated</b> Oct 28 2026</span><span><b>Market</b> NQ / MNQ futures</span><span><b>Data</b> 763 days (2022–25) + 61 days (2026)</span><span><b>Window</b> 09:30–11:30 New York</span></div></header>''')
    out.append('''<section class="min" aria-label="In one minute">
<div><b>The morning is made early</b><p>The high or the low of 09:30–11:30 is in by 10:00 on 83 / 85% of days. The first 15 minutes make about a third of them.</p></div>
<div><b>BC+ points the way</b><p>A BC+ at 09:30 or at 10:00: the next candle takes its target first 82–92% of the time, on every timeframe.</p></div>
<div><b>The opening range breaks once</b><p>Price closes out of 09:30–10:00 on 94 / 92% of days and runs a median 51 / 71 pts. It breaks both sides only 14 / 11%.</p></div>
<div><b>Gaps with the 4H side hold</b><p>09:30–10:00 gaps get touched in about 5 minutes. With the 4H candle they react 68 / 79%. Against it, 47 / 29%.</p></div>
<div><b>Runs are 2 BCs long</b><p>After 10:00 a run makes a median 2 body closes and 30–36 pts (5m) before the other side closes. Take points; the opposite candle gives them back.</p></div>
<div class="no"><b>No trade by itself</b><p>The first BC after 10:00 with a 50 pt stop at 1:2 has no edge (t-score under 2). These are maps of the morning, not entries.</p></div>
</section>''')
    out.append('<nav class="toc" aria-label="Contents"><h2>Contents</h2><ol>'+''.join(f'<li><a href="#{s["id"]}"><span>{s["num"]}</span>{s["title"]}</a></li>' for s in S)+'</ol></nav>')
    for s in S:
        b=[]
        if s.get('kpis'): b.append('<dl class="kpis">'+''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k,v in s['kpis'])+'</dl>')
        if s.get('table'): b.append(table(s['table']))
        if s.get('table2'): b.append(table(s['table2']))
        if s.get('note'): b.append(f'<p class="note">{s["note"]}</p>')
        if s.get('best'): b.append('<div class="best">'+''.join(f'<div><b>{t}</b><ul>'+''.join(f'<li>{x}</li>' for x in L)+'</ul></div>' for t,L in s['best'])+'</div>')
        if s.get('steps'): b.append('<ol class="steps">'+''.join(f'<li><b>{t}</b><span>{x}</span></li>' for t,x in s['steps'])+'</ol>')
        if s.get('defs'): b.append('<dl class="defs">'+''.join(f'<dt>{t}</dt><dd>{x}</dd>' for t,x in s['defs'])+'</dl>')
        if s.get('bullets'): b.append('<ul class="f">'+''.join(f'<li>{x}</li>' for x in s['bullets'])+'</ul>')
        sub=f'<small>{s["sub"]}</small>' if s.get('sub') else ''
        out.append(f'<section class="s" id="{s["id"]}" aria-labelledby="h-{s["id"]}"><div class="sh"><span class="n">{s["num"]}</span><h2 id="h-{s["id"]}">{s["title"]}{sub}</h2></div><div class="sb">{"".join(b)}</div></section>')
    return '\n'.join(out)
LEGAL='<p class="legal">Education only, not financial advice. Backtests describe the past and do not promise future results. Futures trading carries a high risk of loss. Parts 1–8 are counts of what price did, not tested strategies. The 2026 sample is 61 days.</p>'
HEAD='''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;600&display=swap">'''
B=body()
site=f'''<!DOCTYPE html>
<html lang="en">
<head>
{HEAD}
<title>9:30 AM to 11:30 AM Testing Studies | MMM Trading</title>
<meta name="description" content="The full summary of every MMM test on the New York morning, 09:30 to 11:30: high and low timing, the 09:30 and 10:00 candles, the opening range, opening gaps, BC runs and a 50 pt 1:2 check. NQ 2022–25 + MNQ 2026.">
<link rel="canonical" href="https://www.maxmaserati.com/backtests/ny-open/study/">
<meta name="mmm-page" content="nyopen">
<link rel="icon" href="/favicon.ico" sizes="any">
<meta name="theme-color" content="#07080a">
<script src="https://cdn.tailwindcss.com"></script>
<style>{CSS}
main .doc h1,main .doc h2{{font-family:var(--display)}}
</style>
</head>
<body>
<div id="mmm-header"></div>
<div class="wrap"><main class="doc">
{B}
<div class="links"><a class="try" href="https://whop.com/mmmtrading/products/" target="_blank" rel="noopener">Try the indicators for free</a><a href="/backtests/ny-open/">Open the interactive NY open lab</a><a href="/strategies/">The strategy book</a><a href="/backtests/">All backtests</a><button type="button" onclick="window.print()">Print or save as PDF</button></div>
{LEGAL}
</main></div>
<div id="mmm-footer"></div>
<script src="/assets/nav.js"></script>
<script src="/assets/site.js"></script>
<script src="/i18n.js"></script>
</body>
</html>
'''
open('/home/claude/mmmpro-journal/backtests/ny-open/study/index.html','w').write(site)
art=f'''<!DOCTYPE html>
<html lang="en">
<head>
{HEAD}
<title>9:30 to 11:30 Studies</title>
<style>{CSS}
:root:not([data-theme="light"]){{color-scheme:dark}}
</style>
</head>
<body>
<div class="wrap"><main class="doc">
{B}
<div class="links"><a href="https://www.maxmaserati.com/backtests/ny-open/" target="_blank" rel="noopener">Open the interactive NY open lab</a><a href="https://www.maxmaserati.com/backtests/ny-open/study/" target="_blank" rel="noopener">This study on maxmaserati.com</a></div>
{LEGAL}
</main></div>
</body>
</html>
'''
import os
os.makedirs('/tmp/claude-0/-home-claude/2f55ff78-2cd0-5f42-a374-6a674bbb5d06/scratchpad/study',exist_ok=True)
open('/tmp/claude-0/-home-claude/2f55ff78-2cd0-5f42-a374-6a674bbb5d06/scratchpad/study/MMM_0930_1130_Testing_Studies.html','w').write(art)
# markdown
import re
def md(x): 
    x=re.sub(r'</?b>','**',x); x=x.replace('&amp;','&'); return re.sub(r'<[^>]+>','',x)
M=[f'# {TITLE}','','MMM research desk · updated Oct 28 2026 · NQ 1m Dec 2022–Dec 2025 (763 days) / MNQ 1m 2026 (61 days). Every cell = 2022–25 / 2026.','']
for s in S:
    M.append(f'## {s["num"]}. {md(s["title"])}'+(f' — {md(s["sub"])}' if s.get('sub') else '')); M.append('')
    if s.get('kpis'): M+= [f'- **{md(k)}:** {md(v)}' for k,v in s['kpis']]+['']
    for tk in ('table','table2'):
        if s.get(tk):
            t=s[tk]; M.append('| '+' | '.join(md(h) for h in t['h'])+' |'); M.append('|'+'---|'*len(t['h']))
            M+= ['| '+' | '.join(md(c) for c in r)+' |' for r in t['rows']]; M.append('')
    if s.get('note'): M+=[md(s['note']),'']
    if s.get('best'):
        for t,L in s['best']: M.append(f'**{t}**'); M+= [f'- {md(x)}' for x in L]; M.append('')
    if s.get('steps'): M+= [f'{i+1}. **{md(t)}** — {md(x)}' for i,(t,x) in enumerate(s['steps'])]+['']
    if s.get('defs'): M+= [f'- **{md(t)}** = {md(x)}' for t,x in s['defs']]+['']
    if s.get('bullets'): M+= [f'- {md(x)}' for x in s['bullets']]+['']
M.append('Education only, not financial advice. Parts 1–8 are counts of what price did, not tested strategies.')
open('/home/claude/ten/MMM_0930_1130_Testing_Studies.md','w').write('\n'.join(M))
print('ok')
