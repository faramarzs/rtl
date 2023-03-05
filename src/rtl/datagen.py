import json


def datagen(lines: list[str]) -> dict:
    char_data = []
    arabic_numbers = [chr(x) for x in range(0x660, 0x66a)]
    persian_numbers = [chr(x) for x in range(0x6f0, 0x6fa)]
    data = {
        'chars': char_data,
        'numbers': {
            'arabic': arabic_numbers,
            'persian': persian_numbers
        }
    }

    for line in lines:
        parts = [s.strip().replace('"', '') for s in line.split(",")]
        assert len(parts) == 11, f"There is no enough items in line (line='{line}', parts={len(parts)}"
        char_data.append({
            'name': parts[10],
            'code': int(parts[0], 16),
            'isolated': int(parts[2], 16),
            'end': int(parts[4], 16),
            'middle': int(parts[6], 16) if parts[6] != '' else 0,
            'beginning': int(parts[8], 16) if parts[8] != '' else 0,
        })

    return data


def generate(input_file: str, output_file: str, compressed_json: bool = False) -> None:
    with open(input_file, "r") as fi:
        lines = [line.strip() for line in fi.readlines() if not line.startswith("#") and not line.startswith("\n")]
        data = datagen(lines)
        with open(output_file, "w") as fo:
            s = json.dumps(data, indent=None if compressed_json else 4)
            fo.write(s)
            fo.write('\n')


if __name__ == '__main__':
    generate("../../docs/data.txt", "../../docs/rtl-data.json", compressed_json=False)
