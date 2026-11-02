"""Builds MMM_PRO_U_4.0.pine from the template, the shared 3.7/3.8 modules and the new 4.0 parts."""
import sys
sys.path.insert(0, '/home/claude/v36')
import modules as m

D = '/home/claude/v40'
t = open(f'{D}/u40_template.pine').read()
rd = lambda f: open(f'{D}/{f}').read().rstrip('\n')

fill = {
    'TF_INPUTS': m.TF_INPUTS.replace('{grp}', '0. Structure Timeframe (HTF in LTF)'),
    'RANGE_INPUTS': m.RANGE_INPUTS.replace('{grp}', '7. Lines · Max Outside the Range'),
    'TN_INPUT': m.TN_INPUT,
    'GATE_INPUTS': m.GATE_INPUTS.replace('{grp}', '8. Gate · Premium / Discount').replace('{gate_tf}', ', read on the STRUCTURE timeframe'),
    'ZONE_INPUTS': m.ZONE_INPUTS.replace('{grp}', '9. eBlock / iBlock'),
    'HTF_INPUTS': m.HTF_INPUTS.replace('{grp}', '11. HTF Bias (HTF in LTF)').replace('{eng_default}', 'Zone x (boxes)').replace('{pos_default}', 'Top Center'),
    'NEWS_INPUTS': m.NEWS_INPUTS.replace('{grp}', '13. News'),
    'STATS_INPUTS': m.STATS_INPUTS.replace('{grp}', '14. BC Flow & Volatility Stop').replace('st_on   = input.bool(true,', 'st_on   = input.bool(false,'),
    'PALETTE': rd('palette.pine'),
    'GATE_ENGINE': m.GATE_ENGINE,
    'TF_ENGINE': m.TF_ENGINE,
    'ZONE_HELPERS': m.ZONE_HELPERS,
    'LEVELS': m.LEVELS,
    'RANGE_HELPERS': m.RANGE_HELPERS,
    'ZONE_ENGINE': m.ZONE_ENGINE,
    'HTF_ENGINE': m.HTF_ENGINE.replace('{htf_grow}', 'boxGrow'),
    'NEWS_ENGINE': m.NEWS_ENGINE.replace('size=size.tiny', 'size=f_lsz(news_size)'),
    'STATS_ENGINE': rd('stats38.pine'),
    'XDXP_ENGINE': m.XDXP_ENGINE.replace('{bull}', 'c_bull_bc').replace('{bear}', 'c_bear_bc').replace('size=xdxp_size == "normal" ? size.normal : xdxp_size == "tiny" ? size.tiny : size.small', 'size=f_lsz(xdxp_size)'),
    'BODY': rd('body_a.pine').replace('//@@GMTAB@@', rd('gmtab.pine')) + '\n\n' + rd('body_b.pine') + '\n\n' + rd('body_c.pine'),
}
for k, v in fill.items():
    tag = f'//@@{k}@@'
    assert tag in t, tag
    t = t.replace(tag, v.rstrip('\n'))
assert '//@@' not in t
assert 'f_lsz(news_size)' in t and 'f_lsz(xdxp_size)' in t
import re
left = re.findall(r'\{(grp|bull|bear|eng_default|pos_default|htf_grow|gate_tf)\}', t)
assert not left, left
out = '/home/claude/v40/MMM_Pro_XCS_One.pine'
open(out, 'w').write(t)
print(out, len(t.splitlines()), 'lines', len(t), 'chars')
