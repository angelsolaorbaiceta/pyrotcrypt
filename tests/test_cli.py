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
