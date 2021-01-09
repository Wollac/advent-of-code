import pathlib

import pytest

from aoc import plugin

here = pathlib.Path(__file__).parent
input_files = sorted(here.glob("20*/*/*.txt"))


def path2id(input_file):
    return str(input_file.relative_to(here))


@pytest.mark.parametrize("input_file", input_files, ids=path2id)
def test_example(input_file, monkeypatch):
    # example input files are in ./YYYY/DD/*.txt
    *_, year, day, _ = input_file.parts
    year = int(year)
    day = int(day)

    # the last two lines are the expected answers for part a and part b
    *input_lines, expected_part_a, expected_part_b = input_file.read_text().splitlines()
    input_data = "\n".join(input_lines)

    # replace aocd.data with the test data
    monkeypatch.delattr("__main__.__file__")
    monkeypatch.setattr("aocd.data", input_data)

    part_a, part_b = plugin(year, day, input_data)

    # verify expected answers
    if expected_part_a != "-":
        assert part_a == expected_part_a
    if expected_part_b != "-":
        assert part_b == expected_part_b
