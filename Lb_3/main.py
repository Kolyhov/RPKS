"""Command-line interface entry point."""

from __future__ import annotations

from . import benchmark


def main() -> None:
    benchmark.main()


if __name__ == "__main__":
    main()
