import textwrap
from pathlib import Path

from rich.console import Console
from rich.table import Table

from parabellum.commons import Printer
from parabellum.core import (
    NotionDatabase,
    NotionPage,
    NotionService,
)
from parabellum.core.htb import HtbMachine, HtbService

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

    def _print_dbs(self, dbs: list[NotionDatabase]) -> None:
        table: Table = Table()
        table.add_column('ID', header_style='b', justify='left')
        table.add_column('Title', header_style='b', justify='full')

        [table.add_row(db.identifier, db.title) for db in dbs]

        self.console.print(table)

    def _print_machines(self, machines: list[HtbMachine]) -> None:
        table: Table = Table()
        columns: list[str] = [
            'ID',
            'Machine',
            'Difficulty',
            'OS',
            'Rating',
            'User Owns',
            'System Owns',
        ]

        for index, column in enumerate(columns):
            if index == 1:
                table.add_column(column, header_style='b', justify='left')
            elif index == len(columns):
                table.add_column(column, header_style='b', justify='right')
            else:
                table.add_column(column, header_style='b', justify='center')

        for machine in machines:
            table.add_row(
                str(machine.id),
                machine.name,
                machine.difficulty_text,
                machine.os,
                str(machine.stars),
                str(machine.user_owns_count),
                str(machine.root_owns_count),
            )

        self.console.print(table)

    def _print_pages(self, pages: list[NotionPage]) -> None:
        table: Table = Table()
        table.add_column('ID', header_style='b', justify='left')
        table.add_column('Title', header_style='b', justify='full')

        [table.add_row(page.identifier, page.title) for page in pages]

        self.console.print(table)

    def do_create_db(self, line: str | None = None) -> bool:
        try:
            args = line.split(' ')
            if not args[0]:
                Printer.err('missing template file')
                return False

            template = Path(args[0])
            service: NotionService = NotionService()
            service.create_db(template)
            Printer.suc('database created successfully.')

        except Exception as ex:
            Printer.err(str(ex))

    def do_machines(self, line: str | None = None) -> None:
        try:
            args: list[str] = line.split(' ')
            update: bool = '-u' in args
            retired: bool = '-r' in args
            size: int = int(args[args.index('-s') + 1]) if '-s' in args else 5

            service: HtbService = HtbService()
            machines: list[HtbMachine] = service.list_machines(
                size=size, update=update, retired=retired
            )
            self._print_machines(machines)

        except Exception as ex:
            Printer.err(str(ex))

    def do_notion_dbs(self, line: str | None = None) -> None:
        try:
            service: NotionService = NotionService()
            dbs: list[NotionDatabase] = service.list_dbs()
            self._print_dbs(dbs)

        except Exception as ex:
            Printer.err(str(ex))

    def do_notion_pages(self, line: str | None = None) -> None:
        try:
            service: NotionService = NotionService()
            pages: list[NotionPage] = service.list_pages()
            self._print_pages(pages)

        except Exception as ex:
            Printer.err(str(ex))

    def help_create_db(self) -> None:
        """
        Prints help menu for the create_db command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] create_db notion-templates/template.json

        Create a new Notion database based on a template file.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)

    def help_machines(self) -> None:
        """
        Prints help menu for the machines command.
        """

        help_text = """
        [bold cyan]Usage:[/bold cyan] machines [OPTIONS]

        List active and retired machines. By default it lists
        only active machines.

        [bold cyan]Options:[/bold cyan]
            -r          List only retired machines.
            -s  int     Max size of machines to be printed. Default is 5.
            -u          Force update results rather than getting from cache.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)

    def help_notion_dbs(self) -> None:
        """
        Prints help menu for the notion_dbs command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] notion_dbs

        List all notion databases that is integrated with Parabellum.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)

    def help_notion_pages(self) -> None:
        """
        Prints help menu for the notion_pages command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] notion_pages

        List all notion pages that is integrated with Parabellum.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)
