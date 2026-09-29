.PHONY: test
test:
	uv run pytest -v

.PHONY: sync
sync:
	uv sync

.PHONY: build
build:
	uv build

.PHONY: publish
	uv publish

.PHONY: show_help
show_help:
	uv run pyrotcrypt --help
