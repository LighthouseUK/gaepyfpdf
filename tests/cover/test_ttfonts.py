# -*- coding: utf-8 -*-

"Basic test of TrueType Unicode font handling"

from __future__ import with_statement

#PyFPDF-cover-test:res=font/DejaVuSansCondensed.ttf
#PyFPDF-cover-test:res=dejavusanscondensed.cw.dat

import common
from gaefpdf.ttfonts import TTFontFile

import os, struct

@common.add_unittest
def dotest(outputname, nostamp):
    ttf = TTFontFile()
    ttffile = os.path.join(common.basepath, "font", "DejaVuSansCondensed.ttf");
    ttf.getMetrics(ttffile)
    # test basic metrics:
    assert round(ttf.descent, 0) == -236, "Check descent"
    assert round(ttf.capHeight, 0) == 928, "Chech capHeight"
    assert ttf.flags == 4, "Check flags"
    assert [round(i, 0) for i in ttf.bbox] == [-918, -415, 1513, 1167], "Check bbox"
    assert ttf.italicAngle == 0, "Check italicAngle==0"
    assert ttf.stemV == 87, "Check stemV"
    assert round(ttf.defaultWidth, 0) == 540, "Check defaultWidth"
    assert round(ttf.underlinePosition, 0) == -63, "Check underlinePosition"
    assert round(ttf.underlineThickness, 0) == 44, "Check underlineThickness"
    # test char widths (against binary file generated by tfpdf.php):
    # note: after fixing issue 82 this raw data started to be wrong
    #  1. total length - 65536, DejaVuSansCondensed.ttf maximal char is 65533, round to nearest 1024 size
    #  2. missing char width should be 540 instead of zero
    with open(os.path.join(common.basepath, "dejavusanscondensed.cw.dat"),\
            "rb") as file:
        data = file.read()
    char_widths = struct.unpack(">%dH" % (len(data) // 2), data)
    assert len(char_widths) == 65536, "Check cw.dat char_widths 65536"
    assert len(ttf.charWidths) == 65536, "Check ttf char_widths 65536"
    diff = []
    for i, (x, y) in enumerate(zip(char_widths, ttf.charWidths)):
        if x == 0 and y == ttf.defaultWidth: continue
        if x != y:# compare each char width, but not 0
            diff.append(i)
    assert not diff, "Check char widths"
    # for checking assertion works ttf.charWidths[1] = 600
    ## assert tuple(ttf.charWidths) == tuple(char_widths)
    
if __name__ == "__main__":
    common.testmain(__file__, dotest)

