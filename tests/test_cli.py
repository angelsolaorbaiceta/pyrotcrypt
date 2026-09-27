import io
import re
from collections.abc import Iterable
from unittest.mock import ANY, MagicMock, patch

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


@pytest.mark.parametrize(
    ("args", "expected_filename", "expected_content"),
    [
        (["-w"], "cipher.rot13.txt", "sbb\none\n"),
        (["--write"], "cipher.rot13.txt", "sbb\none\n"),
        (["-w", "-n7"], "cipher.rot7.txt", "mvv\nihy\n"),
        (["-w", "-d"], "plain.rot13.txt", "sbb\none\n"),
        (["-w", "-d", "-n7"], "plain.rot7.txt", "yhh\nutk\n"),
    ],
)
@patch("pyrotcrypt.write_file")
def test_save_to_file_from_stdin(
    write_file_mock: MagicMock,
    args: list[str],
    expected_filename: str,
    expected_content: str,
) -> None:
    """When pyrotcrypt encrypts from stdin and it's passed the -w|--write flag,
    it writes the output to a "cipher.rot<num>.txt" file. If the -d|--decrypt flag
    is also passed, the output is written to "plain.rot<num>.txt".
    """
    stdin = io.StringIO("foo\nbar\n")
    stdout, stderr = io.StringIO(), io.StringIO()

    code = run(args, stdin, stdout, stderr)

    assert code == 0
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == ""

    write_file_mock.assert_called_once_with(expected_filename, expected_content)


@pytest.mark.parametrize(
    ("args", "expected_filename", "expected_content"),
    [
        (["-w", "one.txt"], "one.cipher.rot13.txt", "sbb\none\n"),
        (["--write", "one.txt"], "one.cipher.rot13.txt", "sbb\none\n"),
        (["-w", "-n7", "one.txt"], "one.cipher.rot7.txt", "mvv\nihy\n"),
        (["-w", "-d", "one.txt"], "one.plain.rot13.txt", "sbb\none\n"),
        (["-w", "-d", "-n7", "one.txt"], "one.plain.rot7.txt", "yhh\nutk\n"),
    ],
)
@patch("pyrotcrypt.write_file")
@patch("pyrotcrypt.slurp")
def test_save_to_files(
    slurp_stub: MagicMock,
    write_file_mock: MagicMock,
    args: list[str],
    expected_filename: str,
    expected_content: str,
) -> None:
    """When pyrotcrypt encrypts from files and it's passed the -w|--write flag,
    it writes the output of each file to <filename>.encrypted.rot<num>. If the
    -d|--decrypt flag is passed, the output is written to <filename>.plantext.rot<num>.
    """
    slurp_stub.side_effect = lambda _: "foo\nbar\n"

    stdin, stdout, stderr = io.StringIO(), io.StringIO(), io.StringIO()

    code = run(args, stdin, stdout, stderr)

    assert code == 0
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == ""

    slurp_stub.assert_called_once_with("one.txt")
    write_file_mock.assert_called_once_with(expected_filename, expected_content)
