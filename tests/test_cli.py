import io
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


@pytest.mark.parametrize("arg_name", ["-n", "--num"])
def test_rot_with_num_arg(arg_name: str) -> None:
    """Calling pyrotcrypt -n z<num> reads from stdin and writes to stdout, and
    rotates charactes as many times as given.
    """
    stdin = io.StringIO("foo\nbar\n")
    stdout, stderr = io.StringIO(), io.StringIO()

    code = run([arg_name, "14"], stdin, stdout, stderr)

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
