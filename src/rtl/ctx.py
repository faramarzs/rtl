from rtl.chars import char_data, CASE_MIDDLE, CASE_BEGINNING, CASE_END, CASE_ISOLATED, ATTR_NEXT_ATTACH, \
    ATTR_PREV_ATTACH

char_cases = {chr(d['code']): d for d in char_data["chars"]}


def _right_attached(text, idx) -> bool:
    if idx > 0 and (text[idx] not in char_cases or text[idx - 1] not in char_cases):
        return False
    return idx > 0 and char_cases[text[idx - 1]][ATTR_NEXT_ATTACH] and char_cases[text[idx]][ATTR_PREV_ATTACH]


def _left_attached(text, idx) -> bool:
    if (idx + 1) < len(text) and (text[idx] not in char_cases or text[idx + 1] not in char_cases):
        return False
    return (idx + 1) < len(text) and char_cases[text[idx + 1]][ATTR_PREV_ATTACH] and char_cases[text[idx]][
        ATTR_NEXT_ATTACH]


def ctx_analysis(text: str, debug: int = 0) -> str:
    new_text = ""
    for idx, ch in enumerate(text):
        r_attached = _right_attached(text, idx)
        l_attached = _left_attached(text, idx)

        if r_attached:
            ch_case = CASE_MIDDLE if l_attached else CASE_END
        else:
            ch_case = CASE_BEGINNING if l_attached else CASE_ISOLATED

        if ch in char_cases:
            chi = char_cases[ch][ch_case]
            updated_ch = chr(chi) if chi > 0 else ch
        else:
            chi = ord(ch)
            updated_ch = ch
        if debug:
            print(f"DEBUG: ch={ch}({ord(ch)}) {r_attached=} {l_attached=} {chi=} {updated_ch=}")
        new_text += updated_ch
    return new_text
