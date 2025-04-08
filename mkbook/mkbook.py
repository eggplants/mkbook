"""Create a PDF book from images."""

from __future__ import annotations

import importlib.resources
import io
import os
import re
from functools import cmp_to_key
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from PIL import Image as PImage
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
)

if TYPE_CHECKING:
    from reportlab.platypus.flowables import Flowable


class MakeBook:
    """Create a PDF book from images."""

    default_font = Path(str(importlib.resources.files("mkbook"))) / "fonts" / "RampartOne-Regular.ttf"
    img_extensions = PImage.registered_extensions()

    def __init__(self, font_path: str | Path | None = None) -> None:
        """Initialize the MakeBook class.

        Args:
            font_path (str | Path | None): Path to the font file. If None, use the default font.
        """
        self.set_font(font_path)

    def set_font(self, font_path: str | Path | None = None) -> None:
        """Set the font for the PDF.

        Args:
            font_path (str | Path | None): Path to the font file. If None, use the default font.
        """
        font_path = self.default_font if font_path is None else font_path
        font_name = Path(font_path).name.split(".")[0]
        pdfmetrics.registerFont(TTFont(font_name, font_path, asciiReadable=True))
        self.font_path, self.font_name = font_path, font_name

    def make(self, save_path: Path | str, target_path: str, font_size: int = 20) -> None:
        """Create a PDF book from images.

        Args:
            save_path (Path | str): Path to save the PDF file.
            target_path (str): Path to the target directory containing images.
            font_size (int): Font size for the text in the PDF.
        """
        text_style = ParagraphStyle(
            name="Normal",
            fontName=self.font_name,
            alignment=TA_CENTER,
            fontSize=font_size,
            textColor=black,
            wordWrap="CJK",
        )
        door_text_style = ParagraphStyle(
            name="Normal",
            fontName=self.font_name,
            alignment=TA_CENTER,
            fontSize=font_size * 3,
            textColor=black,
            wordWrap="CJK",
        )
        br = "<br />\n<br />\n"
        stories: list[Literal[0, 1] | Flowable] = [
            0,
            Paragraph(Path(target_path).name, door_text_style),
            PageBreak(),
        ]
        sizes = [A4, A4]
        cnt = 1
        tree = list(os.walk(target_path))
        tree = self.sort_v(tree)
        tree_size = len(tree)
        for idx, (root, _dirs, files) in enumerate(tree):
            print(root)
            root_filename = Path(root).name
            files = sorted(f for f in files if Path(f).suffix in self.img_extensions)  # noqa: PLW2901
            w, h = self.get_size(root, files)
            sizes.append((w, h))
            if len(files) > 0:
                stories.extend(
                    (
                        0,
                        Paragraph(
                            root_filename.replace("　", br * 2).replace("]", "]" + br * 2),
                            door_text_style,
                        ),
                        1,
                        Paragraph(f"{cnt}", text_style),
                        PageBreak(),
                    ),
                )
                cnt += 1
            files_size = len(files)
            f_idx = 0
            for f_idx, img in enumerate(files):
                print(
                    f"\033[2K{idx + 1}/{tree_size} ({f_idx + 1}/{files_size})",
                    end="\n\033[A",
                )
                border_img = [[Image(Path(root) / img)]]
                stories.append(
                    Paragraph(root_filename, text_style),
                )
                stories.append(Spacer(1, font_size))
                stories.append(Table(border_img, w, h))
                stories.append(Spacer(1, font_size))
                stories.append(Paragraph(f"{cnt}", text_style))
                stories.append(PageBreak())
                cnt += 1
            print(f"\033[2K{idx + 1}/{tree_size} ({f_idx}/{files_size})", end="\n\033[A")
        print("\033[2KSaving...")

        (_min_w, _min_h), *_, (max_w, max_h) = sorted(sizes)
        max_w += 400
        max_h += 400
        doc = SimpleDocTemplate(str(save_path), pagesize=(max_w, max_h))

        doc.build(
            [
                Spacer(1, max_h / 2) if s == 0 else Spacer(1, max_h / 8 + font_size * 9) if s == 1 else s
                for s in stories
            ],
        )

    @staticmethod
    def pil_to_bytes(img: PImage.Image) -> bytes:
        """Convert a PIL image to bytes.

        Args:
            img (PIL.Image.Image): The PIL image to convert.

        Returns:
            bytes: The image in bytes format.
        """
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        return img_bytes.getvalue()

    def get_size(self, root: str, files: list[str]) -> tuple[float, float]:
        """Get the size of the largest image in the directory.

        Args:
            root (str): The root directory.
            files (list[str]): List of image files.

        Returns:
            tuple[float, float]: The width and height of the largest image.
        """
        if len(files) == 0:
            return A4
        w, h = sorted(PImage.open(Path(root) / f).size for f in files)[-1]
        return float(w), float(h)

    @staticmethod
    def sort_v(tree: list[tuple[str, list[str], list[str]]]) -> list[tuple[str, list[str], list[str]]]:
        """Sort the directory tree.

        Args:
            tree (list[tuple[str, list[str], list[str]]]): The directory tree.

        Returns:
            list[tuple[str, list[str], list[str]]]: The sorted directory tree.
        """

        def cmp(a: tuple[str, list[str], list[str]], b: tuple[str, list[str], list[str]]) -> int:
            def norm(s: str) -> str:
                tr = str.maketrans("１２３４５６７８９０", "1234567890")  # noqa: RUF001
                s = s.translate(tr)
                return re.sub(r"(\d+)", lambda m: m.group(1).zfill(30), s)

            sa, sb = norm(a[0]), norm(b[0])
            return -1 if sa < sb else 1 if sa > sb else 0

        return sorted(tree, key=cmp_to_key(cmp))
