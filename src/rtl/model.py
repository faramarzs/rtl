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
    orig_lang: Language = Language.NONE

    def append(self, ch: str) -> str:
        self.text += ch
        return self.text

    def coalesce(self, other: 'Block'):
        assert self.lang == other.lang
        if other.lang == Language.RTL and other.orig_lang != Language.NONE:
            other.text = other.text[::-1]
        self.text += other.text

    def lang_text(self):
        if self.lang == Language.RTL:
            return self.text[::-1]
        return str(self.text)

    def replace_text(self, new_text: str):
        self.orig_text = self.text
        self.text = new_text


@dataclass
class Line:
    blocks: List = field(default_factory=list)
