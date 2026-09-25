def slurp(path: str) -> str:
    with open(path, encoding="utf-8") as w:
        return w.read()
