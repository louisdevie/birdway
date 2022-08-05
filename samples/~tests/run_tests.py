import os, sys
from pathlib import Path as P
from pprint import pprint

from printer import *
from test import Tests

ROOT = P(__file__).parent.parent

PRINTER = Printer(sys.stdout)


def main():
    PRINTER.print("Loading tests ... ")
    PRINTER.indent()

    tests = load_tests()

    PRINTER.println("done")
    PRINTER.unindent()

    PRINTER.println("Ready to execute", tests.count_total, "tests", style=GREEN & BOLD)
    input()

    ok, used = tests.run(PRINTER, ROOT)

    if ok == tests.count_total:
        color = GREEN
    elif (ok / tests.count_total) > (9 / 10):  # more than 1 out of 10 failed
        color = YELLOW
    else:
        color = RED

    PRINTER.println()
    PRINTER.println(
        f"{ok} tests successful out of {tests.count_total}", style=color & BOLD
    )

    implemented = []
    for root, dirs, files in os.walk(ROOT):
        for file in files:
            file = P(root) / P(file)
            if file.suffix == ".bw":
                with open(file, "rt") as f:
                    content = f.read()
                if not content.rstrip().endswith("---"):
                    implemented.append(str(file.relative_to(ROOT)))
    not_tested = [f for f in implemented if f not in used]

    if len(not_tested) == 0:
        PRINTER.println(f"All scripts were tested !", style=GREEN & BOLD)
    else:
        if (len(not_tested) / len(implemented)) < (
            1 / 10
        ):  # less than 1 out of 10 weren't tested
            color = YELLOW
        else:
            color = RED

        PRINTER.println(
            f"{len(not_tested)} scripts were not tested :", style=color & BOLD
        )
        PRINTER.indent(" → ")
        for f in sorted(not_tested):
            PRINTER.println(f)


def load_tests():
    tests = Tests()

    for root, dirs, files in os.walk(ROOT):
        root = P(root)

        for file in files:
            path = root / file

            if path.suffixes == [".test", ".yaml"]:
                if path.stem[:-5] != root.name:
                    PRINTER.newline()
                    PRINTER.println(
                        f"WARNING : test file {path.relative_to(ROOT)} doesn't have the same name as the directory",
                        style=YELLOW,
                    )

                with open(path, "rt", encoding="utf-8") as f:
                    tests.load(f.read(), path.parent.relative_to(ROOT))

    return tests


if __name__ == "__main__":
    main()
