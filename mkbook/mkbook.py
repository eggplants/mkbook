from __future__ import annotations

import os
from typing import cast

from PIL import Image as PImage
from pkg_resources import resource_filename
from reportlab.lib.colors import black as BLACK  # type: ignore[import]
from reportlab.lib.enums import TA_CENTER  # type: ignore[import]
from reportlab.lib.pagesizes import A4  # type: ignore[import]
from reportlab.lib.styles import ParagraphStyle  # type: ignore[import]
from reportlab.pdfbase import pdfmetrics  # type: ignore[import]
from reportlab.pdfbase.ttfonts import TTFont  # type: ignore[import]
from reportlab.platypus import (  # type: ignore[import]
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


class MakeBook:
    default_font = resource_filename(__name__, "fonts/RampartOne-Regular.ttf")
    img_extensions = PImage.registered_extensions().keys()

    def __init__(self, font_path: str | None = None) -> None:
        self.set_font(font_path)

    def set_font(self, font_path: str | None = None) -> None:
        font_path = self.default_font if font_path is None else font_path
        font_name = os.path.basename(font_path).split(".")[0]
        pdfmetrics.registerFont(TTFont(font_name, font_path))
        self.font_path, self.font_name = font_path, font_name

    def make(self, save_path: str, target_path: str, font_size: int = 20) -> None:
        text_style = ParagraphStyle(
            name="Normal",
            fontName=self.font_name,
            alignment=TA_CENTER,
            fontSize=font_size,
            textColor=BLACK,
            splitLongWords=True,
        )
        stories = []
        doc = SimpleDocTemplate(save_path, pagesize=A4)
        for root, _dirs, files in os.walk(target_path):
            files = sorted(
                f for f in files if f".{'.'.split(f)[-1]}" in self.img_extensions
            )
            _w, h = self.get_size(files)
            stories.append(Spacer(1, h / 2))
            stories.append(Paragraph(root, text_style))
            for img in files:
                stories.append(Image(img, _w, h))
        doc.build(stories)

    def get_size(self, files: list[str]) -> tuple[float, float]:
        if len(files) == 0:
            return cast(tuple[float, float], A4)
        sizes = [PImage.open(f).size for f in files]
        w, h = sorted(sizes)[-1]
        return float(w), float(h)
