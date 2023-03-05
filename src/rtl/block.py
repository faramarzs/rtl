from dataclasses import dataclass, field
from enum import Enum
from typing import List, Union

from rtl.render import contextual_analyze

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
        return contextual_analyze(self.text)


@dataclass
class Line:
    blocks: List = field(default_factory=list)

    def render(self, direction=Direction.LTR):
        self._set_block_directions(direction)

        if direction == Direction.LTR:
            self._render_ltr()
        self._render_rtl()

    def _set_block_directions(self, dir: Direction):
        for idx, block in enumerate(self.blocks):
            prev_dir = dir if idx == 0 else self.blocks[idx - 1].dir
            next_dir = dir if idx == len(self.blocks) - 1 else self.blocks[idx + 1].dir

            self._set_block_direction(block, master_dir=dir, prev_dir=prev_dir, next_dir=next_dir)

    @staticmethod
    def _set_block_direction(block: Block, master_dir: Direction, prev_dir: Union[Direction, None],
                             next_dir: Union[Direction, None]) -> None:
        if block.dir != Direction.NEUTRAL:
            return

        if prev_dir == next_dir:
            block.dir = prev_dir
            return

        if prev_dir == Direction.NEUTRAL:
            block.dir = next_dir
            return

        if next_dir == Direction.NEUTRAL:
            block.dir = prev_dir
            return

        block.dir = dir

    def _render_ltr(self):
        pass

    def _render_rtl(self):
        pass
