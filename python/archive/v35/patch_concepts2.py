import sys
p='MMM_Concepts_Pro_Plus_3.5.pine'; src=open(p).read()
def rep(old,new,count=1):
    global src
    c=src.count(old)
    if c!=count: print("FAIL",c,old[:200]); sys.exit(1)
    src=src.replace(old,new)
rep('''var float  lastRevBoxLow    = na
''','''var float  lastRevBoxLow    = na
var int    lastRevHT        = na   // when the live LDx level was set
var int    lastRevLT        = na   // when the live SDx level was set
''')
rep('''var int   revHT    = na
var int   revLT    = na
''','')
rep('''        revHT    := int(nz(htf_time, time))''','''        lastRevHT := int(nz(htf_time, time))''')
rep('''        revLT    := int(nz(htf_time, time))''','''        lastRevLT := int(nz(htf_time, time))''')
rep('''        int    nT   = nUp ? revHT : revLT''','''        int    nT   = nUp ? lastRevHT : lastRevLT''')
# CDLx above / CDSx below the middle of the box
rep('''CDLabel := label.new(x=f_future_time(offsetGap), y=cdexY, text=revPass ? cdexText : str.lower(cdexText), style=label.style_label_left,''',
    '''CDLabel := label.new(x=int(math.avg(currentLiveBox.startTime, htf_time)), y=cdexY, text=revPass ? cdexText : str.lower(cdexText), style=cdexText == "CDLx" ? label.style_label_down : label.style_label_up,''')
# LDx above / SDx below the middle of the level span
rep('''sharedLDLabel := label.new(x=f_future_time(offsetGap), y=lastRevBoxHigh, text=contPass ? ldLabelText : str.lower(ldLabelText), style=label.style_label_left,''',
    '''sharedLDLabel := label.new(x=int(math.avg(nz(lastRevHT, htf_time), htf_time)), y=lastRevBoxHigh, text=contPass ? ldLabelText : str.lower(ldLabelText), style=label.style_label_down,''')
rep('''sharedSDLabel := label.new(x=f_future_time(offsetGap), y=lastRevBoxLow, text=contPass ? sdLabelText : str.lower(sdLabelText), style=label.style_label_left,''',
    '''sharedSDLabel := label.new(x=int(math.avg(nz(lastRevLT, htf_time), htf_time)), y=lastRevBoxLow, text=contPass ? sdLabelText : str.lower(sdLabelText), style=label.style_label_up,''')
rep('''sharedLDLabel := label.new(x=f_future_time(offsetGap), y=lastRevBoxHigh, text=plusPass ? ldLabelText : str.lower(ldLabelText), style=label.style_label_left,''',
    '''sharedLDLabel := label.new(x=int(math.avg(nz(lastRevHT, htf_time), htf_time)), y=lastRevBoxHigh, text=plusPass ? ldLabelText : str.lower(ldLabelText), style=label.style_label_down,''')
rep('''sharedSDLabel := label.new(x=f_future_time(offsetGap), y=lastRevBoxLow, text=plusPass ? sdLabelText : str.lower(sdLabelText), style=label.style_label_left,''',
    '''sharedSDLabel := label.new(x=int(math.avg(nz(lastRevLT, htf_time), htf_time)), y=lastRevBoxLow, text=plusPass ? sdLabelText : str.lower(sdLabelText), style=label.style_label_up,''')
rep('''        if not boxGrow
            na
        else if currentLiveBox.boxType == "Demand" and isCurrentBullishAffinity''', '''        if boxGrow and currentLiveBox.boxType == "Demand" and isCurrentBullishAffinity''')
rep('''        else if currentLiveBox.boxType == "Supply" and isCurrentBearishAffinity
            if htf_high > affinityTrackedBoundary''', '''        else if boxGrow and currentLiveBox.boxType == "Supply" and isCurrentBearishAffinity
            if htf_high > affinityTrackedBoundary''')
open(p,'w').write(src); print("ok")
