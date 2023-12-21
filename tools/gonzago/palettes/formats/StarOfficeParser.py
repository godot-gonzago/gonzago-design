from pathlib import Path

from ..core import Palette
from ..io import register_reader, register_writer

# http://www.selapa.net/swatches/colors/fileformats.php#ooo_soc

# <?xml version="1.0" encoding="UTF-8"?>
# <office:color-table xmlns:office="http://openoffice.org/2000/office" xmlns:style="http://openoffice.org/2000/style" xmlns:text="http://openoffice.org/2000/text" xmlns:table="http://openoffice.org/2000/table" xmlns:draw="http://openoffice.org/2000/drawing" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:meta="http://openoffice.org/2000/meta" xmlns:number="http://openoffice.org/2000/datastyle" xmlns:svg="http://www.w3.org/2000/svg" xmlns:chart="http://openoffice.org/2000/chart" xmlns:dr3d="http://openoffice.org/2000/dr3d" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:form="http://openoffice.org/2000/form" xmlns:script="http://openoffice.org/2000/script">
#   <!-- vsf 2018-01-09, using dave eddy <bahamas10> implementation of Gossett & Chen algorithm https://bahamas10.github.io/ryb/about.html -->
#   <!-- regenerated a RYB => RGB sequence for the RYB Hues at: 0, tints at 191, 153, 115, 77 and shades at -51, -102, -153, -204 -->
#   <!-- Color naming RYB Hues: primary: Red, Yellow, Blue; secondary: Orange, Green, Purple; tertiary: Magenta, Indigo, Teal, Lime, Gold, Brick as found https://en.wikipedia.org/wiki/Tertiary_color -->
#
#   <!-- Gray palette from black to white -->
#   <draw:color draw:name="Black" draw:color="#000000"/>
#   <draw:color draw:name="Dark Gray 4" draw:color="#111111"/>
#
#   <!-- +191 brightness, 75% tint -->
#   <draw:color draw:name="Light Yellow 4" draw:color="#ffffd7"/>
#   <draw:color draw:name="Light Gold 4" draw:color="#fff5ce"/>
# </office:color-table>


ID: str = "office"
PATTERN: str = "*.soc"
SUFFIX: str = ".soc"
DESCRIPTION = "Color palette for StarOffice/OpenOffice/LibreOffice."


def read(file: Path) -> Palette:
    raise NotImplementedError()


def write(palette: Palette, file: Path) -> None:
    raise NotImplementedError()


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
