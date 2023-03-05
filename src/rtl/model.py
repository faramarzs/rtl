from dataclasses import dataclass, field
from enum import Enum
from typing import List, Union


class Language(Enum):
    NONE = -1
    LTR = 0
    RTL = 1
    NEUTRAL = 2


class Direction(Enum):
    NONE = -1
    LTR = 0
    RTL = 1


class RTLAlgorithm(Enum):
    LTR_NEUTRAL = 1
    RTL_NEUTRAL = 2
    PREV = 3
    DIR_BASED = 4


@dataclass
class Block:
    lang: int = Language.LTR
    text: str = ''
    orig_text: str = None
    orig_lang: int = Language.NONE

    def append(self, ch: str) -> str:
        self.text += ch
        return self.text

    def coalesce(self, other: 'Block'):
        assert self.lang == other.lang
        self.text += other.text

    def lang_text(self):
        if self.lang == Direction.RTL:
            return self.text[::-1]
        return str(self.text)


@dataclass
class Line:
    blocks: List = field(default_factory=list)
