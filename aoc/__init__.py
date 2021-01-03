import io
import runpy
import sys

__version__ = "2020.1"


def plugin(year, day, data):
    mod_name = f"aoc.{year}.day{day:02d}"
    sys.modules.pop(mod_name, None)
    old_stdout = sys.stdout
    sys.stdout = out = io.StringIO()
    try:
        runpy.run_module(mod_name, run_name="__main__")
    except ImportError:
        return None, None
    finally:
        sys.stdout = old_stdout
    lines = [x for x in out.getvalue().splitlines() if x]

    part_a = part_b = None
    for line in lines:
        if line.startswith("Part One"):
            if len(line.split()) > 2:
                part_a = line.split()[-1]
            else:
                part_a = ""
        elif line.startswith("Part Two"):
            if len(line.split()) > 2:
                part_b = line.split()[-1]
            else:
                part_b = ""
    return part_a, part_b
