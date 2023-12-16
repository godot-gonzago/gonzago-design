from .parser import register_reader, register_writer
import TemplateParser
import PNGParser
import GIMPParser
import HexParser
import AdobeParser
import KritaParser
import PaintNetParser
import PaintShopProParser
import ScribusParser
import StarOfficeParser

__all__ = [
    "register_reader",
    "register_writer",
    "TemplateParser",
    "PNGParser",
    "GIMPParser",
    "HexParser",
    "AdobeParser",
    "KritaParser",
    "PaintNetParser",
    "PaintShopProParser",
    "ScribusParser",
    "StarOfficeParser"
]
