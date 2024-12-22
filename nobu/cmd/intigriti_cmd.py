from rich.table import Table

from nobu.commons import Printer
from nobu.core.intigriti import IntigritiService
from nobu.core.intigriti.entities import IntigritiProgram, IntigritiProgramSlim

from .nobu_cmd import NobuCmd


class IntigritiCmd(NobuCmd):
    """
    Handle the Intigriti module commands.
    """

    def __init__(self) -> None:
        """
        Initializes IntigritiCmd object.
        """
        super().__init__('intigriti')
        self.programs: list[IntigritiProgramSlim | None] = None

    def do_info(self, line: str | None = None) -> bool:
        try:
            if not self.programs:
                service: IntigritiService = IntigritiService()
                self.programs = service.list_programs()

            args: list[str] = line.split(' ')
            identifier: str = args[-1]
            if identifier.isdigit():
                identifier: int = int(identifier) - 1
                id_greater_than_max_size = identifier >= len(self.programs)
                id_less_than_min_size = identifier < 0

                if id_greater_than_max_size or id_less_than_min_size:
                    Printer.err('invalid program ID')
                    return False
            else:
                Printer.err('invalid program ID')
                return False

            program_id: str = self.programs[identifier].id
            service: IntigritiService = IntigritiService()
            program: IntigritiProgram = service.get_program(program_id)

            table = Table()

            columns: list[str] = [
                'Domain',
                'Tier',
                'Type',
                'Description',
            ]

            for index, column in enumerate(columns):
                if index == 1:
                    table.add_column(column, header_style='b', justify='left')
                elif index == len(columns):
                    table.add_column(column, header_style='b', justify='right')
                else:
                    table.add_column(column, header_style='b', justify='full')

            for domain in program.domains:
                table.add_row(
                    domain.endpoint,
                    domain.tier,
                    domain.type,
                    domain.description,
                )

            Printer.table(table)

        except Exception as ex:
            Printer.err(str(ex))

    def do_programs(self, line: str | None = None) -> None:
        try:
            args: list[str] = line.split(' ')
            following: bool = '-f' in args
            limit: int | None = self.get_option_value(args, '-l', int)
            match_status: int | None = self.get_option_value(args, '-ms', int)
            match_type: int | None = self.get_option_value(args, '-mt', int)
            offset: int | None = self.get_option_value(args, '-of', int)
            search: str | None = self.get_option_value(args, '-s', str)

            service: IntigritiService = IntigritiService()
            self.programs = service.list_programs(
                following=following,
                limit=limit,
                match_status=match_status,
                match_type=match_type,
                offset=offset,
                search=search,
            )

            table: Table = Table()
            columns: list[str] = [
                'ID',
                'Name',
                'Status',
                'Confidentiality',
            ]

            for index, column in enumerate(columns):
                if index == 1:
                    table.add_column(column, header_style='b', justify='left')
                elif index == len(columns):
                    table.add_column(column, header_style='b', justify='right')
                else:
                    table.add_column(
                        column, header_style='b', justify='center'
                    )

            for index, program in enumerate(self.programs):
                table.add_row(
                    str(index + 1),
                    program.name,
                    program.status,
                    program.confidentiality_level,
                )

            Printer.table(table)
        except Exception as ex:
            Printer.err(str(ex))

    def help_info(self) -> None:
        """
        Prints help menu for the info command.
        """
        help_text = """
        [bold cyan]Usage:[/bold cyan] info <PROGRAM-ID>

        Get program information.
        """
        Printer.help(help_text)

    def help_programs(self) -> None:
        """
        Prints help menu for the programs command.
        """
        help_text = """
        [bold cyan]Usage:[/bold cyan] programs [OPTIONS]

        List all Intigriti available programs for your user.

        [bold cyan]Options:[/bold cyan]
            -f              Return only programs that you're following.

            -l  int         Limit of programs to be returned.

            -ms int         Return programs with specified status ID.
                            [bold green]3[/bold green] [dim]Open[/dim]
                            [bold green]4[/bold green] [dim]Suspended[/dim]
                            [bold green]5[/bold green] [dim]Closing[/dim]

            -mt int         Return programs with specified type ID.
                            [bold green]1[/bold green] [dim]Bug bounty[/dim]
                            [bold green]2[/bold green] [dim]Hybrid[/dim]

            -of int         Get programs starting by the specified offset.

            -s  string      Filter by specified name.
        """
        Printer.help(help_text)
