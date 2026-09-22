import sys
from typing import Protocol, TextIO

from pyrotcrypt.rot import rot


class Reader(Protocol):
    def readline(self) -> str: ...


def run(argv: list[str], stdin: Reader, stdout: TextIO, stderr: TextIO) -> int:
    while line := stdin.readline():
        stdout.write(rot(line, 13))
    return 0


def main() -> None:
    sys.exit(run(sys.argv, sys.stdin, sys.stdout, sys.stderr))
