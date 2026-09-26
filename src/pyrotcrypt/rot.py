_alpha_size = ord("z") - ord("a") + 1
"""The number of characters in the english alphabet."""


def normalize_rotnum(num: int) -> int:
    """Rotating _alpha_size times is equivalent to not rotating at all.
    This function ensures the rotation count stays in the [0, _alpha_size) interval.
    """
    return num % _alpha_size


def rotleft_equivalent(num: int) -> int:
    """If the text is going to be decrypted, this function calculates the number
    of rotations equivalent to rotating num times to the left.
    """
    return _alpha_size - normalize_rotnum(num)


def rot(text: str, n: int) -> str:
    return "".join(rotate_char(c, n) for c in text)


def rotate_char(c: str, n: int) -> str:
    """Rotate a single character by n positions, preserving case."""
    if c.isalpha():
        base = ord("a") if c.islower() else ord("A")
        return chr((ord(c) - base + n) % 26 + base)
    return c
