from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, Type

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
CONFIG_FILE: Path = APP_DIR.joinpath("config.yaml").resolve()

# TODO: Look at https://github.com/lincolnloop/goodconf/tree/main
# https://maxb2.github.io/typer-config/latest/
# https://github.com/pypae/pydantic-typer#readme


# https://docs.pydantic.dev/latest/concepts/pydantic_settings/
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", yaml_file=CONFIG_FILE)

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

    dst: DirectoryPath = Path(__file__).joinpath("../../../..").resolve()
    src: DirectoryPath = dst.joinpath("source").resolve()

    max_depth: int = 8

    inkscape: Optional[Path] = None
    blender: Optional[Path] = None

    def src_path(self, rel: Path | str) -> Path:
        return self.src.joinpath(rel).resolve()

    def dst_path(self, rel: Path | str) -> Path:
        return self.dst.joinpath(rel).resolve()

    def get_yaml_file_location(self) -> Path:
        return self.model_config.get("yaml_file", CONFIG_FILE)

    def save_to_yaml(self) -> None:
        data: dict = self.model_dump(mode="json", exclude_unset=False)
        file = self.get_yaml_file_location()
        file.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
        with file.open("w") as stream:
            yaml.safe_dump(data, stream, sort_keys=False)

    def clear_yaml(self) -> None:
        file = self.get_yaml_file_location()
        if file.is_file():
            file.unlink()
        else:
            return

        folder = file.parent
        if folder.is_dir() and not any(folder.iterdir()):  # check if folder is empty
            folder.rmdir()


CONFIG: Settings = Settings()
