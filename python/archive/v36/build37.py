import sys
sys.path.insert(0, '/home/claude/v36')
from build import build37
which = sys.argv[1:] or ['ofs', 'concepts']
if 'ofs' in which:
    build37('OFS', '/home/claude/v36/ofs37_template.pine', '/home/claude/v36/MMM_Order_Flow_Suite_3.7.pine',
          {'tf': '0. Structure Timeframe (HTF in LTF)', 'rng': '4. Market Structure (Swing Engine s)', 'st': '11. BC Flow & Volatility Stop',
           'gate': '5. Gate · Premium / Discount', 'zone': '6. eBlock / iBlock', 'htf': '7. HTF Bias (HTF in LTF)', 'news': '8. News'},
          'Swing s (swings)', 'Top Right', 'LINE_BULL', 'LINE_BEAR', ', read on the STRUCTURE timeframe', 'true')
if 'concepts' in which:
    build37('Concepts', '/home/claude/v36/concepts37_template.pine', '/home/claude/v36/MMM_Concepts_Pro_Plus_3.7.pine',
          {'tf': '0. Structure Timeframe (HTF in LTF)', 'rng': '3. Lines · Max Outside the Range', 'st': '8. BC Flow & Volatility Stop',
           'gate': '4. Gate · Premium / Discount', 'zone': '5. eBlock / iBlock', 'htf': '6. HTF Bias (HTF in LTF)', 'news': '7. News'},
          'Zone x (boxes)', 'Top Right', 'c_bull_bc', 'c_bear_bc', ', read on the STRUCTURE timeframe', 'boxGrow')
