from __future__ import annotations

from mkbook import __version__


def test_check_version() -> None:
    assert __version__ is not None
