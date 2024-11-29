import argparse
import pathlib


def init_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--parse-file', type=pathlib.Path, help='Path to edit file')
    parser.add_argument('-o', '--output-file', type=pathlib.Path, help='Path to write output in json')
    args = parser.parse_args()

    return args
