import argparse
import sys
from typing import Protocol, TextIO

from pyrotcrypt.rot import rot


class Reader(Protocol):
    def readline(self) -> str: ...


parser = argparse.ArgumentParser(
    prog="pyrotcrypt",
    description="Encrypt/Decrypt text by rotating the letters of the alphabet",
)
parser.add_argument(
    "-n",
    "--num",
    type=int,
    default=13,
    help="the number of positions to rotate each letter",
)


def run(argv: list[str], stdin: Reader, stdout: TextIO, stderr: TextIO) -> int:
    args = parser.parse_args(argv)
    while line := stdin.readline():
        stdout.write(rot(line, args.n))
    return 0


def main() -> None:
    sys.exit(run(sys.argv, sys.stdin, sys.stdout, sys.stderr))
