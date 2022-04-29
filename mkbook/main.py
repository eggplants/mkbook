from __future__ import annotations

from .mkbook import MakeBook


def main() -> None:
    m = MakeBook()
    m.make("unko.pdf", "/Users/eggplants/prog/mkbook/test_book")


if __name__ == "__main__":
    main()
