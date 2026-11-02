import json, re, sys, os
SP='/tmp/claude-0/-home-claude/2f55ff78-2cd0-5f42-a374-6a674bbb5d06/scratchpad/site'
M=json.load(open(SP+'/missing.json'))
def ph(s): return sorted(re.findall(r'\{\d+\}', s))
def tags(s): return sorted(re.findall(r'<[^>]+>', s))
for lang in sys.argv[1:]:
    T=json.load(open(f'{SP}/tr_{lang}.json'))
    bad=0
    for page,keys in M.items():
        p=f'/home/claude/mmmpro-journal/i18n/{lang}/{page}.json'; D=json.load(open(p))
        tp=T.get(page,{})
        for k in keys:
            v=tp.get(k)
            if not v or ph(v)!=ph(k) or tags(v)!=tags(k): bad+=1; continue
            D[k]=v
        json.dump(D,open(p,'w'),ensure_ascii=False,separators=(',',':'))
    print(lang,'bad',bad)
