import textwrap

from rich.console import Console
from rich.table import Table

from parabellum.commons import Printer
from parabellum.core import NotionPage, NotionService

from .base_cmd import BaseCmd


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
        super().__init__()

    def _print_pages(self, pages: list[NotionPage]) -> None:
        table: Table = Table()
        table.add_column('ID', header_style='b', justify='left')
        table.add_column('Title', header_style='b', justify='center')

        [table.add_row(page.identifier, page.title) for page in pages]

        self.console.print(table)

    def do_notion_pages(self, line: str | None = None) -> None:
        try:
            service: NotionService = NotionService()
            pages: list[NotionPage] = service.list_pages()
            self._print_pages(pages)

        except Exception as ex:
            Printer.err(str(ex))

    def help_notion_pages(self) -> None:
        """
        Prints help menu for the notion_pages command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] notion_pages

        List all notion pages that is integrated with Parabellum.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)
