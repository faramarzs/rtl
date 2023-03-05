import pytest

from rtl.analyzer import Analyzer
from rtl.model import RTLAlgorithm, Direction


def test_render():
    analyzer = Analyzer()
    strs = [
        "امروز ۲۲ امین روز از ماه April یعنی ماه 4 سال میلادی بود؟ شاید!"
    ]
    for s in strs:
        s2 = analyzer.analyze(s, direction=Direction.RTL, algo=RTLAlgorithm.DIR_BASED)
        print(s2)
