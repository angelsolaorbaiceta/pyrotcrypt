.PHONY: test
test:
	uv run pytest -v

.PHONY: show_help
show_help:
	uv run pyrotcrypt --help
