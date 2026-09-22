import io

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


def test_rot_with_num_arg() -> None:
    """Calling pyrotcrypt -n z<num> reads from stdin and writes to stdout, and
    rotates charactes as many times as given.
    """
    stdin = io.StringIO("foo\nbar\n")
    stdout, stderr = io.StringIO(), io.StringIO()

    code = run(["-n", "14"], stdin, stdout, stderr)

    assert code == 0
    assert stdout.getvalue() == "tcc\npof\n"
    assert stderr.getvalue() == ""
