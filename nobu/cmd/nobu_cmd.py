import re
from pathlib import Path

from rich.console import Console
from rich.table import Table

from nobu.commons import Printer
from nobu.core.notion import NotionDatabase, NotionPage, NotionService

from .base_cmd import BaseCmd


class NobuCmd(BaseCmd):
    """
    Handle all Nobu commands.
    """

    console: Console = Console()
    notion: NotionService = NotionService()
    notion_context: NotionDatabase | NotionPage | None = None
    prompt_template: str = 'nobu{module} {notion_context} > '

    def __init__(self, module_name: str | None = None) -> None:
        """
        Initializes NobuCmd object.

        :param module_name: A string representing the module's
         name to be used in the prompt. If None, no module name is set.
        """
        super().__init__()
        self.module_name: str | None = module_name
        self._update_prompt()

    def _update_prompt(self) -> None:
        """
        Updates the prompt with the current context and modules in use.
        """
        self.prompt: str = re.sub(
            ' +',
            ' ',
            NobuCmd.prompt_template.format(
                module=f'({self.module_name})' if self.module_name else '',
                notion_context=(
                    f'({NobuCmd.notion_context.title})'
                    if NobuCmd.notion_context
                    else ''
                ),
            ),
        )

    def do_back(self, line: str | None = None) -> bool:
        return True

    def do_create_db(self, line: str | None = None) -> bool:
        try:
            args: list[str] = line.split(' ')
            if not args[0]:
                Printer.err('missing template file')
                return False

            parent_id: str | None = (
                None
                if not self.notion_context
                else self.notion_context.identifier
            )
            template: Path = Path(args[0])
            self.notion.create_db(template, parent_id=parent_id)
            Printer.suc('database created successfully.')

        except Exception as ex:
            Printer.err(str(ex))

    def do_dbs(self, line: str | None = None) -> None:
        try:
            dbs: list[NotionDatabase] = self.notion.list_dbs()
            table: Table = Table()
            table.add_column('ID', header_style='b', justify='left')
            table.add_column('Title', header_style='b', justify='full')

            [table.add_row(db.identifier, db.title) for db in dbs]
            Printer.table(table)

        except Exception as ex:
            Printer.err(str(ex))

    def do_htb(self, line: str | None = None) -> None:
        try:
            from .htb_cmd import HtbCmd

            HtbCmd().cmdloop()
        except Exception as ex:
            Printer.err(str(ex))

    def do_pages(self, line: str | None = None) -> None:
        try:
            pages: list[NotionPage] = self.notion.list_pages()
            table: Table = Table()
            table.add_column('ID', header_style='b', justify='left')
            table.add_column('Title', header_style='b', justify='full')

            [table.add_row(page.identifier, page.title) for page in pages]
            Printer.table(table)

        except Exception as ex:
            Printer.err(str(ex))

    def do_use(self, line: str | None = None) -> bool:
        try:
            args: list[str] = line.split(' ')

            identifier: str = args[0]
            pages: list[NotionPage] = self.notion.list_pages()
            databases: list[NotionDatabase] = self.notion.list_dbs()

            for page in pages:
                if identifier == page.identifier:
                    NobuCmd.notion_context = page
                    Printer.suc(f'using page "{page.title}"')
                    self._update_prompt()
                    return False

            for database in databases:
                if identifier == database.identifier:
                    NobuCmd.notion_context = database
                    Printer.suc(f'using database "{database.title}"')
                    self._update_prompt()
                    return False

        except Exception as ex:
            Printer.err(str(ex))

    def help_back(self) -> None:
        """
        Prints help menu for the back command.
        """
        help_text = """
        [bold cyan]Usage:[/bold cyan] back

        Leaves the current module.
        """
        Printer.help(help_text)

    def help_create_db(self) -> None:
        """
        Prints help menu for the create_db command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] create_db notion-templates/template.json

        Creates a new Notion database based on a template file.
        """
        Printer.help(help_text)

    def help_dbs(self) -> None:
        """
        Prints help menu for the dbs command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] dbs

        Lists all notion databases that is integrated with Nobu.
        """
        Printer.help(help_text)

    def help_htb(self) -> None:
        """
        Prints help menu for the htb command.
        """
        help_text = """
        [bold cyan]Usage:[/bold cyan] htb

        Starts the Hack the Box module and its commands.
        """
        Printer.help(help_text)

    def help_pages(self) -> None:
        """
        Prints help menu for the notion_pages command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] pages

        Lists all notion pages that is integrated with Nobu.
        """
        Printer.help(help_text)

    def help_use(self) -> None:
        """
        Prints help menu for the use command.
        """
        help_text = """
        [bold cyan]Usage:[/bold cyan] use <id>

        Interacts with a database or page by its ID.
        """
        Printer.help(help_text)
