from rtl.chars import char_data

class Renderer:

    def __init__(self):
        self._char_data = {d['code']: d for d in char_data['chars']}
        self._digit_data = char_data['digits']

    def reder(self, text: str) -> str:
        pass
