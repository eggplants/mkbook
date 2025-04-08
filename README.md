# mkbook

[![PyPI version](
  https://badge.fury.io/py/mkbook.svg
  )](
  https://badge.fury.io/py/mkbook
) [![pre-commit.ci status](
  https://results.pre-commit.ci/badge/github/eggplants/mkbook/master.svg
  )](
  https://results.pre-commit.ci/latest/github/eggplants/mkbook/master
) [![Maintainability](
  <https://qlty.sh/badges/1b18ac00-58a2-4a71-902d-76309813b0ab/maintainability.svg>
  )](
  <https://qlty.sh/gh/eggplants/projects/mkbook>
) [![Code Coverage](
  <https://qlty.sh/badges/1b18ac00-58a2-4a71-902d-76309813b0ab/test_coverage.svg>
  )](
  <https://qlty.sh/gh/eggplants/projects/mkbook>
) [![Release Package](
  https://github.com/eggplants/mkbook/actions/workflows/release.yml/badge.svg
  )](
  https://github.com/eggplants/mkbook/actions/workflows/release.yml
)

- Make directory including pictures into a PDF book.
- This package and tool are mainly made for [getjump](https://github.com/eggplants/getjump)
  - FOR PERSONAL USE ONLY. Generated PDF must not be distributed to other people.

## Install

```sh
pip install mkbook
# or:
pip install git+https://github.com/eggplants/mkbook
```

## CLI

```shellsession
$ mkbook ~/Pictures/タコピーの原罪 takop.pdf
Saving...
Done: /Users/eggplants/prog/mkbook/takop.pdf

$ file takop.pdf
takop.pdf: PDF document, version 1.4

$ mkbook ~/Pictures/タコピーの原罪 takop.pdf
'takop.pdf' already exists. Use `-o` to overwrite.
```

```shellsession
$ mkbook -h
usage: mkbook [-h] [-f FONT_SIZE] [-F TT_FONT] [-o] [-V] PATH PATH

Make directory including pictures into a PDF book

positional arguments:
  PATH                                 target dir
  PATH                                 saved pdf file path

optional arguments:
  -h, --help                           show this help message and exit
  -f FONT_SIZE, --font-size FONT_SIZE  overwrite if pdf path exists (default: 20)
  -F TT_FONT, --tt-font TT_FONT        truetype font file
  -o, --overwrite
  -V, --version                        show program's version number and exit

note:
    This package and tool are mainly made for getjump.
    https://github.com/eggplants/getjump
```

## License

MIT

### Licenses of fonts

- [Rampart](https://github.com/fontworks-fonts/Rampart/blob/master/fonts/ttf/RampartOne-Regular.ttf)

[The Open Font License (OFL)](https://github.com/fontworks-fonts/Rampart/blob/master/OFL.txt)
