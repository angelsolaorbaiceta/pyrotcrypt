import io
from collections.abc import Iterable
from unittest.mock import MagicMock, patch

import pytest

from pyrotcrypt import run


def test_rot_without_args() -> None:
    """Calling pyrotcrypt without options reads from stdin and writes to stdout.
    By default rotates characters by 13 positions.
    """
    stdin = io.StringIO("foo\nbar\n")
    stdout, stderr = io.StringIO(), io.StringIO()

    code = run([], stdin, stdout, stderr)

    assert code == 0
    assert stdout.getvalue() == "sbb\none\n"
    assert stderr.getvalue() == ""


@pytest.mark.parametrize(
    "args", [("-n", "14"), ("-n14",), ("--num", "14"), ("--num=14",)]
)
def test_rot_with_num_arg(args: Iterable[str]) -> None:
    """Calling pyrotcrypt -n z<num> reads from stdin and writes to stdout, and
    rotates charactes as many times as given.
    """
    stdin = io.StringIO("foo\nbar\n")
    stdout, stderr = io.StringIO(), io.StringIO()

    code = run([*args], stdin, stdout, stderr)

    assert code == 0
    assert stdout.getvalue() == "tcc\npof\n"
    assert stderr.getvalue() == ""


@patch("pyrotcrypt.slurp")
def test_encrypt_files(slurp_stub: MagicMock) -> None:
    """Calling pyrotcrypt <arg1> <arg2> expects the arguments to be file paths.
    It reads their contents and encrypts their contenst.
    """
    contents = {"one.txt": "foo", "two.txt": "bar"}
    slurp_stub.side_effect = lambda path: contents[path]

    stdin, stdout, stderr = io.StringIO(), io.StringIO(), io.StringIO()

    code = run(["one.txt", "two.txt"], stdin, stdout, stderr)

    assert code == 0
    assert stdout.getvalue() == "sbbone"
    assert stderr.getvalue() == ""


@pytest.mark.parametrize("arg_name", ["-d", "--decrypt"])
def test_decrypt_stdin(arg_name: str) -> None:
    """Calling pyrotcrypt -d|--decrypt rotates characters in the opposite
    direction to decrypt cyphertexts.
    """
    stdin = io.StringIO("tcc\npof\n")
    stdout, stderr = io.StringIO(), io.StringIO()

    code = run([arg_name, "-n14"], stdin, stdout, stderr)

    assert code == 0
    assert stdout.getvalue() == "foo\nbar\n"
    assert stderr.getvalue() == ""
