from rich.console import Console

from .base_cmd import BaseCmd


class ParabellumCmd(BaseCmd):
    """
    Handle all Parabellum commands.
    """

    def __init__(self) -> None:
        """
        Initializes ParabellumCmd object.
        """
        self.console = Console()
        self.prompt = 'parabellum > '
        super().__init__()
