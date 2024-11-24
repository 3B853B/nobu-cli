import textwrap
from pathlib import Path

from rich.console import Console
from rich.table import Table

from parabellum.commons import Printer
from parabellum.core.notion import (
    NotionDatabase,
    NotionPage,
    NotionService,
)

from .base_cmd import BaseCmd


class NotionCmd(BaseCmd):
    """
    Handle all Notion commands.
    """

    def __init__(self, base_prompt: str) -> None:
        """
        Initializes NotionCmd object.
        """
        self.console: Console = Console()
        self.latest_prompt: str = base_prompt
        self.default_prompt: str = f'{base_prompt.split(" ")[0]}(notion)'
        self.prompt: str = f'{self.default_prompt} > '
        self.context: NotionDatabase | NotionPage | None = None
        self.service: NotionService = NotionService()
        super().__init__()

    def _print_dbs(self, dbs: list[NotionDatabase]) -> None:
        table: Table = Table()
        table.add_column('ID', header_style='b', justify='left')
        table.add_column('Title', header_style='b', justify='full')

        [table.add_row(db.identifier, db.title) for db in dbs]

        self.console.print(table)

    def _print_pages(self, pages: list[NotionPage]) -> None:
        table: Table = Table()
        table.add_column('ID', header_style='b', justify='left')
        table.add_column('Title', header_style='b', justify='full')

        [table.add_row(page.identifier, page.title) for page in pages]

        self.console.print(table)

    def do_back(self, line: str | None = None) -> bool:
        if self.context:
            self.context = None
            self.prompt = f'{self.default_prompt} > '
        else:
            return True

    def do_create_db(self, line: str | None = None) -> bool:
        try:
            args: list[str] = line.split(' ')
            if not args[0]:
                Printer.err('missing template file')
                return False

            parent_id: str | None = (
                None if not self.context else self.context.identifier
            )
            template: Path = Path(args[0])
            service: NotionService = NotionService()
            service.create_db(template, parent_id=parent_id)
            Printer.suc('database created successfully.')

        except Exception as ex:
            Printer.err(str(ex))

    def do_dbs(self, line: str | None = None) -> None:
        try:
            service: NotionService = NotionService()
            dbs: list[NotionDatabase] = service.list_dbs()
            self._print_dbs(dbs)

        except Exception as ex:
            Printer.err(str(ex))

    def do_pages(self, line: str | None = None) -> None:
        try:
            service: NotionService = NotionService()
            pages: list[NotionPage] = service.list_pages()
            self._print_pages(pages)

        except Exception as ex:
            Printer.err(str(ex))

    def do_use(self, line: str | None = None) -> bool:
        try:
            args: list[str] = line.split(' ')

            identifier: str = args[0]
            pages: list[NotionPage] = self.service.list_pages()
            databases: list[NotionDatabase] = self.service.list_dbs()

            for page in pages:
                if identifier == page.identifier:
                    self.context = page
                    self.prompt = f'{self.default_prompt} ({page.title}) > '
                    Printer.suc(f'using page "{page.title}"')
                    return False

            for database in databases:
                if identifier == database.identifier:
                    self.context = database
                    self.prompt = (
                        f'{self.default_prompt} ({database.title}) > '
                    )
                    Printer.suc(f'using database "{database.title}"')
                    return False

        except Exception as ex:
            Printer.err(str(ex))

    def help_back(self) -> None:
        """
        Prints help menu for the back command.
        """
        help_text = """
        [bold cyan]Usage:[/bold cyan] back

        Leaves the current context.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)

    def help_create_db(self) -> None:
        """
        Prints help menu for the create_db command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] create_db notion-templates/template.json

        Creates a new Notion database based on a template file.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)

    def help_dbs(self) -> None:
        """
        Prints help menu for the dbs command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] dbs

        Lists all notion databases that is integrated with Parabellum.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)

    def help_pages(self) -> None:
        """
        Prints help menu for the notion_pages command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] pages

        Lists all notion pages that is integrated with Parabellum.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)

    def help_use(self) -> None:
        """
        Prints help menu for the use command.
        """
        help_text = """
        [bold cyan]Usage:[/bold cyan] use <id>

        Interacts with a database or page by its ID.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)
