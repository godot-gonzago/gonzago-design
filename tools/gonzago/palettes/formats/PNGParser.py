from pathlib import Path
from .parser import register_reader, register_writer

from gonzago.palettes.templates import Template


ID: str = "png"
PATTERN: str = "*/*.png"
SUFFIX: str = ".png"
DESCRIPTION = "PNG palette image with size 1px."


def read(file: Path) -> Template:
    raise NotImplementedError()


def write(id: str, file: Path, template: Template, size: int = 1) -> None:
    """
    PNG

    PNG palette image with size 1px.
    """
    # TODO: Parse scale from filename
    from PIL import Image, ImageDraw

    color_count: int = len(template.colors)
    image: Image = Image.new("RGB", (color_count * size, size))

    draw = ImageDraw.Draw(image, "RGB")
    for i in range(color_count):
        color = template.colors[i].color
        draw.rectangle((i * size, 0, i * size + size, size), color.as_rgb_tuple())

    image.save(file, "PNG")


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
register_writer("png-8", ".x8.png", "PNG palette image with size 8px.", write)
register_writer("png-32", ".x32.png", "PNG palette image with size 32px.", write)
