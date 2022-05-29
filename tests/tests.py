import os, sys


def run_test(name):
    ec = os.system(f"python3 pybw/main.py tests/test_{name}.bw")
    if ec:
        sys.exit(ec)

    ec = os.system(f"build/test_{name}")
    if ec:
        sys.exit(ec)


if __name__ == "__main__":
    for test_name in ["lexer"]:
        run_test(test_name)
