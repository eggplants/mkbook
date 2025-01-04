from __future__ import annotations

import argparse
import shutil
import sys
import textwrap
from pathlib import Path

from . import MakeBook, __version__


class MBHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter,
):
    pass


def check_dir(s: str) -> str:
    if Path(s).is_dir():
        return s
    raise argparse.ArgumentTypeError(f"{s!r} is not a dir.")


def check_file(s: str) -> str:
    path = Path(s)
    if path.is_file() or not path.exists():
        return s
    if not path.parent.is_dir():
        raise argparse.ArgumentTypeError(f"Base dir of {s!r} does not exist.")
    raise argparse.ArgumentTypeError(f"{s!r} is not a file.")


def check_positive(s: str) -> int:
    v = int(s)
    if v >= 1:
        return v
    raise argparse.ArgumentTypeError(f"{s!r} is not a positive integer.")


def parse_args() -> argparse.Namespace:
    usage = textwrap.dedent(
        """
    note:
        This package and tool are mainly made for getjump.
        https://github.com/eggplants/getjump
    """,
    )

    parser = argparse.ArgumentParser(
        prog="mkbook",
        description="Make directory including pictures into a PDF book",
        formatter_class=(
            lambda prog: MBHelpFormatter(
                prog,
                width=shutil.get_terminal_size(fallback=(120, 50)).columns,
                max_help_position=40,
            )
        ),
        epilog=usage,
    )
    parser.add_argument(
        "target_dir",
        type=check_dir,
        help="target dir",
        metavar="PATH",
    )
    parser.add_argument(
        "save_path",
        type=check_file,
        help="saved pdf file path",
        metavar="PATH",
    )
    parser.add_argument(
        "-f",
        "--font-size",
        type=check_positive,
        help="overwrite if pdf path exists",
        default=20,
    )
    parser.add_argument("-F", "--tt-font", type=check_file, help="truetype font file")
    parser.add_argument("-o", "--overwrite", action="store_true")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    status = 0
    save_path = Path(args.save_path)
    if save_path.exists() and not args.overwrite:
        print(
            f"{save_path.resolve()} already exists. Use `-o` to overwrite.",
            file=sys.stderr,
        )
        status = 2
    else:
        font_path = None if args.tt_font == argparse.SUPPRESS else args.tt_font
        m = MakeBook(font_path=font_path)
        m.make(args.save_path, args.target_dir, font_size=args.font_size)
        print(f"Done: {save_path.resolve()}")
    sys.exit(status)


if __name__ == "__main__":
    main()
