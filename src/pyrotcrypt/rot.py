def rot(text: str, n: int) -> str:
    return "".join(rotate_char(c, n) for c in text)


def rotate_char(c: str, n: int) -> str:
    """Rotate a single character by n positions, preserving case."""
    if c.isalpha():
        base = ord("a") if c.islower() else ord("A")
        return chr((ord(c) - base + n) % 26 + base)
    return c
