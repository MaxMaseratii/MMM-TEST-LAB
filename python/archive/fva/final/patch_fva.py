import re,sys
src,dst=sys.argv[1],sys.argv[2]
h=open(src).read()
assert 'data-tab="fva"' not in h
def sub1(pat,repl):
    global h
    m=list(re.finditer(pat,h)); assert len(m)==1,(pat,len(m)); m=m[0]
    h=h[:m.start()]+repl(m)+h[m.end():]
# tab button after the last tab button
btns=list(re.finditer(r'<button role="tab" aria-selected="false" data-tab="[^"]+">(\d+) · [^<]*</button>',h))
last=btns[-1]; num=max(int(b.group(1)) for b in btns)+1
h=h[:last.end()]+f'\n<button role="tab" aria-selected="false" data-tab="fva">{num} · FVA Break · 2 best edges</button>'+h[last.end():]
meta=open('meta_fva.js').read(); play=open('play_fva.js').read()
sub1(r'\nconst ROWS = \{[^\n]*?\};', lambda m: '\n'+meta+'\n'+m.group(0)[1:].replace(' };',', fva: [] };'))
sub1(r'\nfunction showPlay\(', lambda m: '\nPLAY.fva = '+play+m.group(0))
a="  if (r.exitrule && k === 'abbr') return `LR.${r.level}.${r.side[0]}`;"
assert h.count(a)==1
h=h.replace(a,"  if (r.fva && k === 'abbr') return r.code;\n  if (r.fva && k === 'name') return `${r.setup} · ${r.side} · ${r.session} · ${r.filter} · stop ${r.stop} · ${r.target} · ${r.exitrule}`;\n"+a)
a="  else if (state.show[t] === 'star') rs = [...rs].sort((a, b) => a.star - b.star);"
assert h.count(a)==1
h=h.replace(a,a+"\n  else if (t === 'fva' && state.show[t] !== 'worst') rs = [...rs].sort((a, b) => ((a.star || 99) - (b.star || 99)) || (b.av * b.tpm - a.av * a.tpm));")
sub1(r"const LAZY = \{[^\n]*?\};", lambda m: m.group(0).replace(' };',", fva: 'fva.json' };"))
sub1(r"\n  ocf: r => \(\{\}\)", lambda m: m.group(0)+", fva: r => ({ etf: '1h' })")
open(dst,'w').write(h); print('tab',num)
