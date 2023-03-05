from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Direction(Enum):
    LTR = 0
    RTL = 1
    NEUTRAL = 2


@dataclass
class Block:
    dir: int = Direction.LTR
    text: str = ''

    def append(self, ch: str) -> str:
        self.text += ch
        return self.text

    def render(self) -> str:
        if self.dir == Direction.LTR:
            return str(self.text)
        return self.text[::-1]


@dataclass
class Line:
    blocks: List = field(default_factory=list)

    def render(self, direction=Direction.LTR):
        if direction == Direction.LTR:
            self._render_ltr()
        self._render_rtl()

    def _render_ltr(self):
        pass

    def _render_rtl(self):
        pass
