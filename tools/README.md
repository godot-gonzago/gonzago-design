# Gonzago Framework Design Tools

Tools for Gonzago design assets.

## Gettings started

TODO: Write better instructions

### Setup dependancies

TODO: Write better instructions

Windows User download <https://www.msys2.org/> and prepend System Variable Path with C:\msys64\usr\bin and C:\msys64\mingw64\bin.
Install <https://packages.msys2.org/package/mingw-w64-x86_64-cairo>. Restart System and enjoy a working CairoSVG.

### Setup Poetry

Install Poetry globally.
<https://python-poetry.org/docs/#installation>

1. Install pipx: `python -m pip install pipx`
2. Install Poetry: `pipx install poetry`
3. Poetry needs its paths registered: `pipx ensurepath`

Navigate to your terminal to this folder (if not aleady there) and setup the project locally.

1. Create virtual environment for project: `python -m venv .venv --prompt Gonzago`
2. Activate virtual environment: `.venv/Scripts/Activate.ps1`
3. Install dependancies via poetry: `poetry install`

## Usage

### Usage of automated tools

1. Activate virtual environment: `.venv/Scripts/Activate.ps1`
2. Run gonzago tools: `gonzago`
3. You should see a list of all commands. Use the commands: `gonzago [command]`

#### Config

TODO: Describe better.

### Available tools

#### Application

Application assets.
TODO: Describe better. Location, import settings etc.

#### Icons

Editor icons for use with Godot Engine.
TODO: Describe better. Location, import settings etc.

#### Palettes

Color palletes.
TODO: Describe better. Location, import settings etc.

#### Assets

Tool and demo assets.
TODO: Describe better. Location, import settings etc.

#### Presskit

Presskit assets.
TODO: Describe better. Location, use etc.

## Creating assets

This is a list of the software used to create design assets.
The contained automation tools might rely on an installation of certain software.

- <https://www.blender.org/>
- <https://inkscape.org/>
- <https://www.gimp.org/>
- <https://lmms.io/>
- <https://godotengine.org/>
