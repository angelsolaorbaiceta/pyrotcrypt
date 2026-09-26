def slurp(path: str) -> str:
    with open(path, encoding="utf-8") as w:
        return w.read()


def write_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as w:
        w.write(content)
