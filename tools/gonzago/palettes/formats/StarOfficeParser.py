from pathlib import Path

from ..core import Palette
from ..io import register_reader, register_writer

# http://www.selapa.net/swatches/colors/fileformats.php#ooo_soc

ID: str = "office"
PATTERN: str = "*.soc"
SUFFIX: str = ".soc"
DESCRIPTION = "Color palette for StarOffice/OpenOffice/LibreOffice."


def read(file: Path) -> Palette:
    raise NotImplementedError()


def write(id: str, file: Path, palette: Palette) -> None:
    raise NotImplementedError()


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
