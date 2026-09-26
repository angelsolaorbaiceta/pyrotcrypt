import argparse
import sys
from typing import Protocol, TextIO

from pyrotcrypt.files import slurp
from pyrotcrypt.rot import normalize_rotnum, rot, rotleft_equivalent


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
    dest="num",
    help="the number of positions to rotate each letter",
)
parser.add_argument(
    "-d",
    "--decrypt",
    default=False,
    action="store_true",
    dest="decrypt",
    help="decrypt the ciphertext",
)
parser.add_argument(
    "in_files", nargs="*", help="paths to files to be encrypted/decrypted"
)


def run(argv: list[str], stdin: Reader, stdout: TextIO, stderr: TextIO) -> int:
    args = parser.parse_args(argv)
    num: int = normalize_rotnum(args.num)
    in_files: list[str] = args.in_files
    decrypt: bool = args.decrypt

    if decrypt:
        num = rotleft_equivalent(num)

    if len(in_files) > 0:
        stdout.writelines(rot(slurp(file), num) for file in in_files)
    else:
        while line := stdin.readline():
            stdout.write(rot(line, num))

    return 0


def main() -> None:
    sys.exit(run(sys.argv[1:], sys.stdin, sys.stdout, sys.stderr))
