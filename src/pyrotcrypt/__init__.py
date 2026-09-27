import argparse
import sys
from importlib.metadata import version
from typing import Protocol, TextIO

from pyrotcrypt.files import slurp, write_file
from pyrotcrypt.rot import normalize_rotnum, rot, rotleft_equivalent

__version__ = version("pyrotcrypt")


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
    help="decrypt the ciphertext (instead of encrypting the plaintext)",
)
parser.add_argument(
    "-w",
    "--write",
    default=False,
    action="store_true",
    dest="write_files",
    help="write cyperthext to files (instead of stdout)",
)
parser.add_argument(
    "-v", "--version", action="version", version=f"%(prog)s {__version__}"
)
parser.add_argument(
    "in_files", nargs="*", help="paths to files to be encrypted/decrypted"
)


def run(argv: list[str], stdin: Reader, stdout: TextIO, stderr: TextIO) -> int:
    args = parser.parse_args(argv)
    num: int = normalize_rotnum(args.num)
    in_files: list[str] = args.in_files
    decrypt: bool = args.decrypt
    write_files: bool = args.write_files

    if decrypt:
        num = rotleft_equivalent(num)

    if len(in_files) > 0:
        if write_files:
            for file in in_files:
                filename = f"{file.removesuffix('.txt')}.{'plain' if decrypt else 'cipher'}.rot{args.num}.txt"
                content = rot(slurp(file), num)
                write_file(filename, content)
        else:
            stdout.writelines(rot(slurp(file), num) for file in in_files)
    else:
        if write_files:
            filename = f"{'plain' if decrypt else 'cipher'}.rot{args.num}.txt"
            content = rot("".join(list(iter(stdin.readline, ""))), num)
            write_file(filename, content)
        else:
            while line := stdin.readline():
                stdout.write(rot(line, num))

    return 0


def main() -> None:
    sys.exit(run(sys.argv[1:], sys.stdin, sys.stdout, sys.stderr))
