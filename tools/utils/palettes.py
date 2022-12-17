import csv
from io import TextIOWrapper
from pathlib import PurePath
from tokenize import String

import yaml
from PIL import ImageColor


class Palette:
    name: str
    description: str
    category: str
    colors: list[str]
    #  - name:  White
    #    dark:  0xffffff
    #    light: 0x414141
