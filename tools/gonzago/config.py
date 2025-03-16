from __future__ import annotations

import sys
from pathlib import Path
from shutil import rmtree
from typing import Optional, Tuple, Type

import tomlkit
import tomlkit.toml_file
import typer
import yaml
from pydantic import DirectoryPath
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

from gonzago import __app_name__

APP_DIR: Path = Path(typer.get_app_dir(__app_name__)).resolve()
CONFIG_FILE: Path = APP_DIR.joinpath("config.toml").resolve()


# https://docs.pydantic.dev/latest/concepts/pydantic_settings/
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", yaml_file=APP_DIR.joinpath("config.yaml").resolve()
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
        )

    dst: DirectoryPath = Path(__file__).joinpath("../../..").resolve()
    src: DirectoryPath = dst.joinpath("source").resolve()

    max_depth: int = 8

    inkscape: Optional[Path] = None
    blender: Optional[Path] = None

    def src_path(self, rel: Path | str) -> Path:
        return self.src.joinpath(rel).resolve()

    def dst_path(self, rel: Path | str) -> Path:
        return self.dst.joinpath(rel).resolve()

    def get_yaml_file_location(self) -> Path:
        return self.model_config.get(
            "yaml_file"  # , APP_DIR.joinpath("config.yaml").resolve()
        )

    def save_to_yaml(self) -> None:
        data: dict = self.model_dump(mode="json", exclude_unset=False)
        file = self.get_yaml_file_location()
        file.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
        with file.open("w") as stream:
            yaml.safe_dump(data, stream, sort_keys=False)


SETTINGS: Settings = Settings()


def get_default() -> tomlkit.TOMLDocument:
    doc = tomlkit.document()
    doc.add(tomlkit.comment(__app_name__))
    doc.add(tomlkit.nl())

    dst = Path(__file__).joinpath("../../..").resolve()
    src = dst.joinpath("source").resolve()

    paths = tomlkit.table()
    paths.add("dst", dst.as_posix())
    paths.add("src", src.as_posix())
    doc.add("paths", paths)
    doc.add(tomlkit.nl())

    io = tomlkit.table()
    io.add("max_depth", 8)
    doc.add("io", io)
    doc.add(tomlkit.nl())

    inkscape_path = "inkscape"
    if sys.platform.startswith("linux"):
        inkscape_path = "/usr/lib/inkscape"
    elif sys.platform.startswith("win32"):
        inkscape_path = "%ProgramFiles%/Inkscape/bin/inkscape.exe"
    elif sys.platform.startswith("darwin"):
        inkscape_path = "/Applications/Inkscape.app/Contents/MacOS/inkscape"

    inkscape = tomlkit.table()
    inkscape.add("path", inkscape_path)
    doc.add("inkscape", inkscape)
    doc.add(tomlkit.nl())

    blender_path = "blender"
    if sys.platform.startswith("linux"):
        blender_path = "/usr/lib/blender"
    elif sys.platform.startswith("win32"):
        blender_path = "%ProgramFiles%/Blender Foundation/Blender 4.0/blender.exe"
    elif sys.platform.startswith("darwin"):
        blender_path = "/Applications/Blender/blender.app/Contents/MacOS/blender"

    blender = tomlkit.table()
    blender.add("path", blender_path)
    doc.add("blender", blender)
    doc.add(tomlkit.nl())

    return doc


def exists() -> bool:
    return CONFIG_FILE.is_file()


def load(use_fallback: bool = True) -> tomlkit.TOMLDocument:
    if use_fallback:
        default = get_default()
        if exists():
            persistent = tomlkit.parse(CONFIG_FILE.read_text())
            default.update(persistent)
        return default

    if exists():
        return tomlkit.parse(CONFIG_FILE.read_text())

    return tomlkit.document()


def save(config: tomlkit.TOMLDocument) -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
    CONFIG_FILE.write_text(tomlkit.dumps(config))


def clear() -> None:
    if APP_DIR.exists():
        rmtree(APP_DIR)


CONFIG = load()


def src_path(rel: Path | str) -> Path:
    return Path(CONFIG["paths"]["src"]).joinpath(rel).resolve()


def dst_path(rel: Path | str) -> Path:
    return Path(CONFIG["paths"]["dst"]).joinpath(rel).resolve()
