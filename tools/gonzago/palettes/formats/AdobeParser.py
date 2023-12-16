from pathlib import Path

from ..core import Palette
from ..io import register_reader, register_writer

ID: str = "ase"
PATTERN: str = "*.ase"
SUFFIX: str = ".ase"
DESCRIPTION = "Color palette for Adobe products (Adobe Swatch Exchange)."


def read(file: Path) -> Palette:
    raise NotImplementedError()


def write(id: str, file: Path, palette: Palette) -> None:
    #    # https://medium.com/swlh/mastering-adobe-color-file-formats-d29e43fde8eb
    #    # http://www.selapa.net/swatches/colors/fileformats.php#adobe_ase
    #    with out_file.open("wb") as file:
    #        # Write header
    #        file.write(b"\x41\x53\x45\x46")  # Signature (Constant: ASEF)
    #        file.write(b"\x00\x01\x00\x00")  # Version (Constant: 1.0)
    #        file.write(b"\x00\x00\x00\x03")  # Number of blocks
    #
    #        # Group start
    #        file.write(b"\xC0\x01")  # Block type (Group start)
    #        file.write(b"\x00\x00\x00\x00")  # Block length
    #        file.write(b"\x00\x00")  # Name length
    #        file.write(b"\x00")  # 0-terminated group name encoded in UTF-16
    #
    #        # Color entry
    #        file.write(b"\x00\x01")  # Block type (Color entry)
    #        file.write(b"\x00\x00\x00\x00")  # Block length
    #        file.write(b"\x00\x00")  # Name length
    #        file.write(b"\x00")  # 0-terminated color name encoded in UTF-16
    #        file.write(b"\x52\x47\x42\x20")  # Color space (Constant: RGB)
    #        file.write(b"\x00\x00\x00\x00")  # Red
    #        file.write(b"\x00\x00\x00\x00")  # Green
    #        file.write(b"\x00\x00\x00\x00")  # Blue
    #        file.write(b"\x00\x02")  # Color mode (Constant: Normal)
    #
    #        # Group end
    #        file.write(b"\xC0\x02")  # Block type (Group end)
    #        file.write(b"\x00\x00\x00\x00")  # Block length (Constant for Group end)
    raise NotImplementedError()


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
