import json
import pathlib

from python_editing.args import init_args
from python_editing.edit import edit


def main():
    args = init_args()
    parse_file: pathlib.Path = args.parse_file
    output_file: pathlib.Path = args.output_file

    with open(parse_file, 'r') as f:
        lines = f.read()

    result = edit(lines)

    json_result = json.dumps(result)

    output_file.write_text(json_result)
    print(f"Final results save to {output_file.absolute().as_uri()}")

    return result
