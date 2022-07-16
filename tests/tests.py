import os, sys


def run_test(name):
    if ec := os.system(f"python3 pybw/main.py tests/test_{name}.bw")
        sys.exit(ec)

    if ec := os.system(f"build/test_{name}")
        sys.exit(ec)


if __name__ == "__main__":
    for test_name in ["lexer"]:
        run_test(test_name)
