from pathlib import Path
from .parser import register_reader, register_writer

from gonzago.palettes.templates import Template


ID: str = "png"
SUFFIX: str = ".png"
DESCRIPTION = "PNG palette image with size 1px."


def can_handle_id(id: str) -> bool:
    raise NotImplementedError()


def can_read(file: Path) -> bool:
    raise NotImplementedError()


def read(file: Path) -> Template:
    raise NotImplementedError()


def change_path_from_id(id: str, file: Path) -> Path:
    raise NotImplementedError()


def can_write(file: Path) -> bool:
    raise NotImplementedError()


def write(file: Path, template: Template, size: int = 1) -> None:
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


register_reader(ID, SUFFIX, DESCRIPTION, can_handle_id, can_read, read)
register_writer(
    ID, SUFFIX, DESCRIPTION, can_handle_id, change_path_from_id, can_write, write
)
