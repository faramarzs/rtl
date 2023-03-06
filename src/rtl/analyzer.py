from typing import Callable

from rtl.chars import char_data
from rtl.model import RTLAlgorithm, Direction, Line, Block, Language


class Analyzer:
    _rtl_chars = set()

    def __init__(self, debug: bool = False):
        self._debug = debug

        self._chars = {chr(d['code']): d for d in char_data['chars']}

        self._neutrals = char_data['neutrals']
        self._digit_data = char_data['digits']
        self._rtl_non_alphas = char_data['rtl-non-alphas']
        self._ltr_non_alphas = char_data['ltr-non-alphas']

        self._init_rtl_set()

    def analyze(self, text: str, direction: Direction, algo: RTLAlgorithm) -> str:
        line = self._parse(text)
        self._resolve_neutrals(line, direction, algo)
        _coalesce_line(line)

        if self._debug:
            for idx, block in enumerate(line.blocks):
                print(f"block #{idx}:")
                print(f"\t{block.lang}")
                print(f"\t|{block.text}|")
            print(".")

        return self._render(line, direction)

    def _init_rtl_set(self):
        for c in self._chars:
            self._rtl_chars.add(c)
            d = self._chars[c]
            self._rtl_chars.add(chr(d['isolated']))
            self._rtl_chars.add(chr(d['beginning']))
            self._rtl_chars.add(chr(d['end']))
            self._rtl_chars.add(chr(d['middle']))
        self._rtl_chars.remove(chr(0))
        for c in self._digit_data['arabic']:
            self._rtl_chars.add(c)
        for c in self._digit_data['persian']:
            self._rtl_chars.add(c)
        for c in self._rtl_non_alphas:
            self._rtl_chars.add(c)
        self._rtl_chars.add('\u200c')

    def _is_rtl(self, ch: str) -> bool:
        return ch in self._rtl_chars

    def _is_neutral(self, ch: str) -> bool:
        return ch in self._neutrals

    def _is_ltr(self, ch: str) -> bool:
        return 'A' <= ch <= 'Z' or 'a' <= ch <= 'z' or ch in self._ltr_non_alphas

    def _render(self, line: Line, direction: Direction) -> str:
        blocks = line.blocks if direction == Direction.LTR else line.blocks[::-1]
        return ''.join([block.lang_text() for block in blocks])

    def _parse(self, text: str) -> Line:
        line = Line()

        block = None
        for ch in text:

            if self._is_rtl(ch):
                lang = Language.RTL
            elif self._is_neutral(ch):
                lang = Language.NEUTRAL
            else:
                lang = Language.LTR

            if not block:
                block = Block()
                line.blocks.append(block)
                block.lang = lang
            else:
                if block.lang != lang:
                    block = Block()
                    line.blocks.append(block)
                    block.lang = lang

            block.append(ch)

        return line

    def _translate_neutrals(self, text):
        return ''.join([self._neutrals.get(ch, ch) for ch in text])

    def _resolve_neutrals(self, line: Line, line_dir: Direction, algo: RTLAlgorithm) -> None:
        """ Resolves all blocks which have NEUTRAL as their language, based on the given algorithm,
            their neighbouring blocks and direction specified for the line.
            After this call, all blocks in the line would be either RTL or LTR as their language;
            although there might be neighbour blocks with same language. That's why next phase in processing
            the line would be coalescing such blocks so no two adjacent block share langauge.

            """

        resolver = _get_resolver(algo)
        for idx, block in enumerate(line.blocks):
            if block.lang != Language.NEUTRAL:
                continue

            prev_lang = Language.NONE if idx == 0 else line.blocks[idx - 1].lang
            next_lang = Language.NONE if idx == len(line.blocks) - 1 else line.blocks[idx + 1].lang

            new_lang = resolver(block, prev_lang, next_lang, line_dir)
            block.orig_lang = block.lang
            block.lang = new_lang

            if block.lang == Language.RTL:
                block.orig_text = block.text
                block.text = self._translate_neutrals(block.text)


def _coalesce_line(line: Line) -> None:
    i = 0
    while i < len(line.blocks):
        block = line.blocks[i]
        next_block = None if (i + 1) >= len(line.blocks) else line.blocks[i + 1]
        if not next_block:
            return

        if block.lang != next_block.lang:
            i += 1
            continue

        block.coalesce(next_block)
        del line.blocks[i + 1]


def _get_resolver(algo: RTLAlgorithm) -> Callable:
    resolvers = {
        RTLAlgorithm.LTR_NEUTRAL: _resolve_ltr_neutral,
        RTLAlgorithm.RTL_NEUTRAL: _resolve_rtl_neutral,
        RTLAlgorithm.PREV: _resolve_prev,
        RTLAlgorithm.DIR_BASED: _resolve_dir_based,
    }
    return resolvers.get(algo)


def _resolve_ltr_neutral(b: Block, prev_lang: Language, next_lang: Language, line_dir: Direction) -> Language:
    """ Resolve NEUTRAL blocks by checking their adjacent blocks; if they are of the same language or one of
        them has NONE (i.e. current block is either first of last block of line), absort language of non-NONE language
        of its neighbour.
        If they're not the same, i.e. one of them is either RTL or another is LTR, LTR is chosen.

    """
    if prev_lang == Language.NONE:
        return next_lang
    if next_lang == Language.NONE:
        return prev_lang
    if next_lang == prev_lang:
        return next_lang
    return Language.LTR


def _resolve_rtl_neutral(b: Block, prev_lang: Language, next_lang: Language, line_dir: Direction) -> Language:
    """ Resolve NEUTRAL blocks by checking their adjacent blocks; if they are of the same language or one of
        them has NONE (i.e. current block is either first of last block of line), absort language of non-NONE language
        of its neighbour.
        If they're not the same, i.e. one of them is either RTL or another is LTR, RTL is chosen.

    """
    if prev_lang == Language.NONE:
        return next_lang
    if next_lang == Language.NONE:
        return prev_lang
    if next_lang == prev_lang:
        return next_lang
    return Language.RTL


def _resolve_prev(b: Block, prev_lang: Language, next_lang: Language, line_dir: Direction) -> Language:
    """ Resolve NEUTRAL blocks by checking their adjacent blocks; if they are of the same language or one of
        them has NONE (i.e. current block is either first of last block of line), absort language of non-NONE language
        of its neighbour.
        If they're not the same, i.e. one of them is either RTL or another is LTR, language of previous block is chosen.

    """

    if prev_lang == Language.NONE:
        return next_lang
    if next_lang == Language.NONE:
        return prev_lang
    if next_lang == prev_lang:
        return next_lang
    return prev_lang


def _resolve_dir_based(b: Block, prev_lang: Language, next_lang: Language, line_dir: Direction) -> Language:
    """ Resolve NEUTRAL blocks by checking their adjacent blocks; if they are of the same language or one of
        them has NONE (i.e. current block is either first of last block of line), absort language of non-NONE language
        of its neighbour.
        If they're not the same, i.e. one of them is either RTL or another is LTR, language which matches the direction
        (i.e. Language.RTL for Direction.RTL or Language.LTR for Direction.LTR) is chosen.

    """

    if prev_lang == Language.NONE:
        return next_lang
    if next_lang == Language.NONE:
        return prev_lang
    if next_lang == prev_lang:
        return next_lang
    return Language.LTR if line_dir == Direction.LTR else Language.RTL
