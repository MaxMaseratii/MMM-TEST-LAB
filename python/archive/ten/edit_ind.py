p='/home/claude/mmmpro-journal/indicators/index.html'; s=open(p).read()
ODDS=open('/home/claude/ten/odds_site.json').read()
css_old='.dinfo{border-left:3px solid var(--ec);padding:6px 0 6px 12px;min-height:58px}'
css_new='''.dinfo{border:2px solid var(--ec);background:color-mix(in srgb,var(--ec) 9%,transparent);padding:10px 14px;min-height:58px;box-shadow:0 0 22px -8px var(--ec)}
.dinfo.flash,.explain.flash{animation:mmmflash .7s ease-out}
@keyframes mmmflash{0%{box-shadow:0 0 0 3px var(--ec,#e1b31a),0 0 30px -4px var(--ec,#e1b31a)}100%{box-shadow:0 0 22px -8px var(--ec,#e1b31a)}}
.cb .explain{border:2px solid var(--gold);--ec:var(--gold);background:rgba(225,179,26,.04);margin:10px}
.dside{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between}
.pm{border:1px solid var(--line2);background:var(--panel2);padding:10px 12px;display:grid;gap:8px}
.pm h4{margin:0;font:700 15px/1.2 var(--display);letter-spacing:.06em;text-transform:uppercase;color:var(--gold2)}
.pm ul{margin:0;padding-left:18px;display:grid;gap:5px;color:#d4dae0;line-height:1.5;font-size:15px}
.wk{display:grid;gap:5px}
.wk .bar{display:flex;height:16px;border:1px solid var(--line2)}
.wk .bar i{display:block;height:100%}
.wk .lg{display:flex;flex-wrap:wrap;gap:4px 12px;font:600 12.5px/1.3 var(--mono);color:#c9d0d6}
.wk .lg b{display:inline-block;width:10px;height:10px;margin-right:5px;vertical-align:-1px}
.oddsbtn{font:700 15px/1.2 var(--display);letter-spacing:.07em;text-transform:uppercase;background:var(--gold);color:#0b0b0b;border:0;padding:11px 14px;cursor:pointer;justify-self:start;text-align:left}
.oddsbtn[aria-expanded="true"]{background:transparent;color:var(--gold);outline:1px solid var(--gold)}
.odds{border:1px solid var(--line2);background:#0b0d10;padding:12px;display:grid;gap:9px}
.odds .tfs{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.orow{display:grid;grid-template-columns:minmax(0,1fr) minmax(60px,130px) 46px;gap:10px;align-items:center;font-size:14.5px;color:#d4dae0}
.orow .tr{height:10px;background:#1b1f25;position:relative}
.orow .tr i{position:absolute;left:0;top:0;bottom:0;display:block}
.orow b{font:700 15px/1 var(--mono);text-align:right}
.odds .nt{margin:0;color:var(--mute);font-size:13px;line-height:1.45}'''
assert css_old in s; s=s.replace(css_old,css_new)
o1='<tr><td>MMCB box</td><td>The higher-timeframe candle drawn on your chart as a box: pale green after a bull type, purple after a bear type. Two sets run at once (H1 and H4 by default), so you see the hour and the 4-hour candle while you trade the 1m or 5m.</td></tr>'
assert o1 in s
s=s.replace(o1,'<tr><td>MMCB box</td><td>Only used to see a higher-timeframe candle on a lower chart. Pick H4 while you trade the 15m: the box is the 4-hour candle’s range with your 15m candles inside it, pale green after a bull type, purple after a bear type. Tap “HTF box on your chart” above to see it.</td></tr>')
s=s.replace('font-size="11">MMCB box</text>','font-size="11">H4 MMCB box</text>')
old_c="idea: 'Reads control one candle at a time. Every candle that closes beyond the one before it is a vote. MMM Pro C keeps score of those votes: the last time buyers forced a close, the last time sellers did, and which of those closes the other side failed to take back.',"
new_c="idea: 'Reads control through the body close candles. A body close beyond the candle before it is expansion: price is out of balance and one side is pushing. MMM Pro C keeps score of those body closes: the last time buyers forced one, the last time sellers did, and which of them the other side failed to take back.',"
assert old_c in s; s=s.replace(old_c,new_c)
o2='<span class="lab">Grey = the previous candle</span>'
assert o2 in s; s=s.replace(o2,'<span class="seg" id="cb-view" role="group" aria-label="View"></span><span class="lab">Grey = the previous candle</span>')
a=s.index('  /* ---------------- MMM Candle Bias Pro ---------------- */'); b=s.index('  /* ---------------- engines ---------------- */')
js=open('/home/claude/ten/cb_js.txt').read().replace('__ODDS__',ODDS)
s=s[:a]+js+'\n'+s[b:]
open(p,'w').write(s); print('ok')
