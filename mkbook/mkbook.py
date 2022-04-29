from __future__ import annotations

import io
import os
from typing import cast

from PIL import Image as PImage
from pkg_resources import resource_filename
from reportlab.lib.colors import black as BLACK
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


class MakeBook:
    default_font = resource_filename(__name__, "fonts/RampartOne-Regular.ttf")
    img_extensions = PImage.registered_extensions()

    def __init__(self, font_path: str | None = None) -> None:
        self.set_font(font_path)

    def set_font(self, font_path: str | None = None) -> None:
        font_path = self.default_font if font_path is None else font_path
        font_name = os.path.basename(font_path).split(".")[0]
        pdfmetrics.registerFont(TTFont(font_name, font_path, asciiReadable=True))
        self.font_path, self.font_name = font_path, font_name

    def make(self, save_path: str, target_path: str, font_size: int = 20) -> None:
        text_style = ParagraphStyle(
            name="Normal",
            fontName=self.font_name,
            alignment=TA_CENTER,
            fontSize=font_size,
            textColor=BLACK,
            wordWrap="CJK",
        )
        stories = [0, Paragraph(os.path.basename(target_path), text_style), PageBreak()]
        sizes = [A4, A4]
        cnt = 1
        tree = [t for t in os.walk(target_path)]
        tree_size = len(tree)
        for idx, (root, _dirs, files) in enumerate(tree):
            files = sorted(
                f for f in files if os.path.splitext(f)[-1] in self.img_extensions
            )
            w, h = self.get_size(root, files)
            sizes.append((w, h))
            if len(files) > 0:
                stories.extend(
                    (
                        0,
                        Paragraph(
                            os.path.basename(root)
                            .replace("　", "<br />\n<br />\n")
                            .replace("]", "]<br />\n<br />\n"),
                            text_style,
                        ),
                        1,
                        Paragraph(f"{cnt}", text_style),
                        PageBreak(),
                    )
                )
                cnt += 1
            files_size = len(files)
            f_idx = 0
            for f_idx, img in enumerate(files):
                print(
                    f"\033[2K{idx+1}/{tree_size} ({f_idx+1}/{files_size})",
                    end="\n\033[A",
                )
                border_img = [[Image(os.path.join(root, img))]]
                stories.append(
                    Paragraph(os.path.basename(root), text_style),
                )
                stories.append(Spacer(1, font_size))
                stories.append(Table(border_img, w, h))
                stories.append(Spacer(1, font_size))
                stories.append(Paragraph(f"{cnt}", text_style))
                stories.append(PageBreak())
                cnt += 1
            print(f"\033[2K{idx+1}/{tree_size} ({f_idx}/{files_size})", end="\n\033[A")
        print("\033[2KSaving...")

        (min_w, min_h), *_, (max_w, max_h) = sorted(sizes)
        max_w += 400
        max_h += 400
        doc = SimpleDocTemplate(save_path, pagesize=(max_w, max_h))

        doc.build(
            [
                Spacer(1, max_h / 2)
                if s == 0
                else Spacer(1, max_h / 4 + font_size + 10)
                if s == 1
                else s
                for s in stories
            ]
        )

    @staticmethod
    def pil_to_bytes(img: PImage.Image) -> bytes:
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        return img_bytes.getvalue()

    def get_size(self, root: str, files: list[str]) -> tuple[float, float]:
        if len(files) == 0:
            return cast(tuple[float, float], A4)
        w, h = sorted(PImage.open(os.path.join(root, f)).size for f in files)[-1]
        return float(w), float(h)
