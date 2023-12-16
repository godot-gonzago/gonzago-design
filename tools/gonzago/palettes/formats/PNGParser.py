from pathlib import Path
from ..io import Palette, register_reader, register_writer


ID: str = "png"
PATTERN: str = "*.png"
SUFFIX: str = ".png"
DESCRIPTION = "PNG palette image."


def read(file: Path) -> Palette:
    raise NotImplementedError()


def write(id: str, file: Path, palette: Palette) -> None:
    """
    PNG

    PNG palette image with size 1px.
    """
    from PIL import Image, ImageDraw

    size: int = 1
    color_count: int = len(palette.colors)
    image: Image = Image.new("RGB", (color_count, size))

    draw = ImageDraw.Draw(image, "RGB")
    for i in range(color_count):
        color = palette.colors[i].color
        draw.rectangle((i * size, 0, i * size + size, size), color.as_rgb_tuple())

    image.save(file, "PNG")


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
