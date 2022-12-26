import csv
from io import TextIOWrapper
from pathlib import PurePath
from tokenize import String

import yaml
from PIL import ImageColor


class Color:
    r: int
    g: int
    b: int
    # https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    # https://stackoverflow.com/questions/5661725/format-ints-into-string-of-hex
    # https://pillow.readthedocs.io/en/stable/reference/ImageColor.html
    # https://stackoverflow.com/questions/18666816/using-python-to-dump-hexadecimals-into-yaml
    # https://docs.python.org/3/library/dataclasses.html#module-dataclasses
    # https://docs.python.org/3/reference/datamodel.html#specialnames
    # https://stackoverflow.com/questions/9100662/how-to-print-integers-as-hex-strings-using-json-dumps-in-python/9101562#9101562
    # https://pynative.com/python-yaml/#h-make-custom-python-class-yaml-serializable

    def load(color: str):
        a: ImageColor._RGB = ImageColor.getrgb(color)


class PaletteEntry:
    name: str
    dark: int
    light: int


class Palette:
    name: str
    description: str
    category: str
    colors: list[PaletteEntry]
    #  - name:  White
    #    dark:  0xffffff
    #    light: 0x414141
