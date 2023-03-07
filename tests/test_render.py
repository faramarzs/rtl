import pytest

from rtl.analyzer import Analyzer
from rtl.model import RTLAlgorithm, Direction

RTL_TEXT = "روباه"
RTL_WITH_SPACE_TEXT = "شیر قهوه‌ای"
RTL_WITH_SPACE_TEXT2 = "ه‌ا"
RTL_NUMBER = "۴۹۶"
RTL_MARKS1 = "؟"
RTL_MARKS2 = "،"

NEUTRAL_TEXT = "593+327=920!"

LTR_TEXT = "bitter"
LTR_WITH_SPACE_TEXT = "bitter taste"
LTR_MARKS1 = "@$"
LTR_MARKS2 = "&~"


def test_render():
    analyzer = Analyzer(debug=1)
    strs = [
        #RTL_TEXT + RTL_NUMBER + RTL_WITH_SPACE_TEXT + RTL_MARKS1,
        #LTR_TEXT + NEUTRAL_TEXT + LTR_WITH_SPACE_TEXT + LTR_MARKS1,
        #LTR_TEXT + NEUTRAL_TEXT + RTL_WITH_SPACE_TEXT + NEUTRAL_TEXT + LTR_WITH_SPACE_TEXT + LTR_MARKS2,
        #RTL_TEXT,
        #RTL_WITH_SPACE_TEXT,
        "۱۲ عید نوروز"
    ]
    with open("/tmp/x.txt", "w") as f:
        for s in strs:
            print(s, file=f)
            print('', file=f)
            s2 = analyzer.analyze(s, direction=Direction.RTL, algo=RTLAlgorithm.DIR_BASED)
            print(s2, file=f)
            sl = list(s)
            sl2 = list(s2)
            print('-----------------------------------------------------------------------', file=f)
