import textwrap

from rich.console import Console

from parabellum.commons import Printer

from .base_cmd import BaseCmd
from .htb_cmd import HtbCmd
from .notion_cmd import NotionCmd


class ParabellumCmd(BaseCmd):
    """
    Handle all Parabellum commands.
    """

    def __init__(self) -> None:
        """
        Initializes ParabellumCmd object.
        """
        self.console: Console = Console()
        self.prompt: str = 'parabellum > '
        self.notion_cmd: NotionCmd = NotionCmd(self.prompt)
        super().__init__()

    def do_htb(self, line: str | None = None) -> None:
        try:
            htb_cmd: HtbCmd = HtbCmd(self.prompt)
            htb_cmd.cmdloop()
        except Exception as ex:
            Printer.err(str(ex))

    def do_notion(self, line: str | None = None) -> None:
        try:
            self.notion_cmd.cmdloop()
        except Exception as ex:
            Printer.err(str(ex))

    def help_htb(self) -> None:
        """
        Prints help menu for the htb command.
        """
        help_text = """
        [bold cyan]Usage:[/bold cyan] htb

        Starts the Hack the Box module and its commands.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)

    def help_notion(self) -> None:
        """
        Prints help menu for the notion command.
        """
        help_text = """
        [bold cyan]Usage:[/bold cyan] notion

        Starts the Notion module and its commands.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)
