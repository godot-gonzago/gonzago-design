import csv
import yaml
from io import TextIOWrapper
from tokenize import String
from PIL import ImageColor
from pathlib import PurePath

path = PurePath(__file__).parent

def read_yaml():
    with open(path.joinpath('./colors/godot.map')) as f:
        config = yaml.safe_load(f)
    return config


def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)
    return tuple(rgb)


def write_palette_header(file: TextIOWrapper, name: String):
    file.write('GIMP Palette\n')
    file.write('Name: Godot Editor Icons ({} Theme)\n'.format(name))
    file.write('# Icon colors based on {} editor theme\n'.format(name.lower()))
    file.write(
        '# <https://docs.godotengine.org/en/stable/development/editor/creating_icons.html>\n')
    file.write('\n\n')


def write_palette_entry(file: TextIOWrapper, hex: String, name: String):
    c = ImageColor.getrgb(hex)
    file.write('{}\t{}\t{}\t{} ({})\n'.format(c[0], c[1], c[2], name, hex))


def write_palette_space(file: TextIOWrapper):
    file.write('\n\n')


def write_palette_footer(file: TextIOWrapper):
    file.write('\n\n')

# TODO: Handle non existent palettes folder
dark_palette = open(path.joinpath('./palettes/godot-dark.gpl'), "w")
light_palette = open(path.joinpath('./palettes/godot-light.gpl'), "w")

write_palette_header(dark_palette, "Dark")
write_palette_header(light_palette, "Light")

with open(path.joinpath('color_map.csv')) as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) == 3:
            write_palette_entry(dark_palette, row[0], row[2])
            write_palette_entry(light_palette, row[1], row[2])
        else:
            write_palette_space(dark_palette)
            write_palette_space(light_palette)

write_palette_footer(dark_palette)
write_palette_footer(light_palette)

dark_palette.close()
light_palette.close()
