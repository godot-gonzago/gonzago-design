import typer

from .check import check
from .reload import reload
from .save import save
from .setup import setup

config_app = typer.Typer()

config_app.command("check")(check)
config_app.command("reload")(reload)
config_app.command("save")(save)
config_app.command("setup")(setup)


@config_app.callback(no_args_is_help=True)
def config_callback() -> None:
    """
    Gonzago Desing Tools config functionality.
    """
