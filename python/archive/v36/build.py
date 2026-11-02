import sys
sys.path.insert(0, '/home/claude/v36')
import modules as M

def fill(tpl, subs):
    for k, v in subs.items():
        tag = '//@@' + k + '@@'
        assert tag in tpl, k
        tpl = tpl.replace(tag, v.rstrip('\n'))
    assert '//@@' not in tpl, 'unfilled tag'
    return tpl

def fmt(s, **kw):
    for k, v in kw.items():
        s = s.replace('{' + k + '}', v)
    return s

def build(name, tpl_path, out_path, grp, eng_default, pos_default, bull, bear, gate_tf, htf_grow, extra=None):
    tpl = open(tpl_path).read()
    subs = {
        'GATE_INPUTS': fmt(M.GATE_INPUTS, grp=grp['gate'], gate_tf=gate_tf),
        'ZONE_INPUTS': fmt(M.ZONE_INPUTS, grp=grp['zone']),
        'HTF_INPUTS':  fmt(M.HTF_INPUTS, grp=grp['htf'], eng_default=eng_default, pos_default=pos_default),
        'NEWS_INPUTS': fmt(M.NEWS_INPUTS, grp=grp['news']),
        'GATE_ENGINE': M.GATE_ENGINE,
        'ZONE_HELPERS': M.ZONE_HELPERS,
        'LEVELS': M.LEVELS,
        'ZONE_ENGINE': M.ZONE_ENGINE,
        'HTF_ENGINE': fmt(M.HTF_ENGINE, htf_grow=htf_grow),
        'NEWS_ENGINE': M.NEWS_ENGINE,
        'HTF_TABLE': fmt(M.HTF_TABLE, bull_col=bull, bear_col=bear),
    }
    if extra:
        subs.update(extra)
    # only fill tags present
    subs = {k: v for k, v in subs.items() if ('//@@' + k + '@@') in tpl}
    out = fill(tpl, subs)
    open(out_path, 'w').write(out)
    print(name, 'ok', out.count('\n'), 'lines')

if __name__ == '__main__':
    which = sys.argv[1:] or ['ofs', 'concepts']
    if 'ofs' in which:
        build('OFS', '/home/claude/v36/ofs_template.pine', '/home/claude/v36/MMM_Order_Flow_Suite_3.6.pine',
              {'gate': '5. Gate · Premium / Discount', 'zone': '6. eBlock / iBlock', 'htf': '7. HTF Bias (HTF in LTF)', 'news': '8. News'},
              'Swing s (swings)', 'Top Right', 'LINE_BULL', 'LINE_BEAR', '', 'true')
    if 'concepts' in which:
        build('Concepts', '/home/claude/v36/concepts_template.pine', '/home/claude/v36/MMM_Concepts_Pro_Plus_3.6.pine',
              {'gate': '4. Gate · Premium / Discount', 'zone': '5. eBlock / iBlock', 'htf': '6. HTF Bias (HTF in LTF)', 'news': '7. News'},
              'Zone x (boxes)', 'Top Right', 'c_bull_bc', 'c_bear_bc', ', read on the BLOCK timeframe', 'boxGrow')

def build37(name, tpl_path, out_path, grp, eng_default, pos_default, bull, bear, gate_tf, htf_grow):
    extra = {
        'TF_INPUTS': fmt(M.TF_INPUTS, grp=grp['tf']),
        'TF_ENGINE': M.TF_ENGINE,
        'RANGE_INPUTS': fmt(M.RANGE_INPUTS, grp=grp['rng']),
        'RANGE_HELPERS': M.RANGE_HELPERS,
        'TN_INPUT': M.TN_INPUT,
        'STATS_INPUTS': fmt(M.STATS_INPUTS, grp=grp['st']),
        'STATS_ENGINE': M.STATS_ENGINE,
        'XDXP_ENGINE': fmt(M.XDXP_ENGINE, bull=bull, bear=bear),
    }
    build(name, tpl_path, out_path, grp, eng_default, pos_default, bull, bear, gate_tf, htf_grow, extra)
