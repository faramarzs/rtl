import json


def datagen(lines: list[str]) -> dict:
    char_data = []
    arabic_numbers = [chr(x) for x in range(0x660, 0x66a)]
    persian_numbers = [chr(x) for x in range(0x6f0, 0x6fa)]
    data = {
        'chars': char_data,
        'digits': {
            'arabic': arabic_numbers,
            'persian': persian_numbers
        },
        'neutrals': {
            ',': '،',
            ';': '؛',
            '?': '؟',
            '*': '×',
            '%': '٪',
            '(': ')',
            ')': '(',
            '{': '}',
            '}': '{',
            '-': '-',
            '+': '+',
            '=': '=',
            '_': '_',
            ' ': ' ',
            '0': '\u06f0',
            '1': '\u06f1',
            '2': '\u06f2',
            '3': '\u06f3',
            '4': '\u06f4',
            '5': '\u06f5',
            '6': '\u06f6',
            '7': '\u06f7',
            '8': '\u06f8',
            '9': '\u06f9',
        },
        'rtl-non-alphas': list('«»٫﷼٪٬ـ؟'),
        'ltr-non-alphas': list('@#$^&/><`\'"~')
    }

    # for na in data['nonalphas']:
    #    print(f"0x{ord(na):04x}: {na}")

    for line in lines:
        parts = [s.strip().replace('"', '') for s in line.split(",")]
        assert len(parts) == 13, f"There is no enough items in line (line='{line}', parts={len(parts)}"
        char_data.append({
            'name': parts[10],
            'code': int(parts[0], 16),
            'isolated': int(parts[2], 16),
            'end': int(parts[4], 16),
            'middle': int(parts[6], 16) if parts[6] != '' else 0,
            'beginning': int(parts[8], 16) if parts[8] != '' else 0,
            'next_attach': int(parts[11]),
            'prev_attach': int(parts[12]),
            'glyphs': [parts[3], parts[5], parts[7], parts[9]]
        })

    return data


def generate(input_file: str, output_file: str, compressed_json: bool = False) -> None:
    with open(input_file, "r") as fi:
        lines = [line.strip() for line in fi.readlines() if not line.startswith("#") and not line.startswith("\n")]
        data = datagen(lines)
        with open(output_file, "w") as fo:
            fo.write('CASE_ISOLATED = "isolated"\n')
            fo.write('CASE_END = "end"\n')
            fo.write('CASE_MIDDLE = "middle"\n')
            fo.write('CASE_BEGINNING = "beginning"\n')
            fo.write('ATTR_NEXT_ATTACH = "next_attach"\n')
            fo.write('ATTR_PREV_ATTACH = "prev_attach"\n')
            fo.write('\n')
            s = json.dumps(data, indent=None if compressed_json else 4)
            fo.write('char_data = ' + s)
            fo.write('\n')


if __name__ == '__main__':
    generate("../../docs/data.txt", "chars.py", compressed_json=False)
