import logging
from typing import Any

from nobu.clients.intigriti import IntigritiClient
from nobu.settings import Settings

from .entities import IntigritiProgram, IntigritiProgramSlim
from .intigriti_parser import IntigritiParser


class IntigritiService:
    def __init__(self) -> None:
        """
        Initializes all IntigritiService object attributes.

        :raise ValueError: When Intigriti token is not found.
        """
        self.logger: logging.Logger = logging.getLogger(
            self.__class__.__name__
        )
        self.settings: Settings = Settings()
        self.token: str = (
            None
            if not self.settings.intigriti_token
            else self.settings.intigriti_token
        )

        if not self.token:
            raise ValueError('could not find Intigriti token')

        self.client = IntigritiClient(token=self.token)

    def list_programs(
        self,
        following: bool | None = None,
        limit: int | None = None,
        match_status: int | None = None,
        match_type: int | None = None,
        offset: int | None = None,
        search: str | None = None,
    ) -> list[IntigritiProgramSlim]:
        """
        Lists all Intigriti programs for your user.

        :param following: Return only programs that you're following.
        :param limit: Limit of programs to be returned.
        :param match_status: Return programs with specified status ID.
        :param match_type: Return programs with specified type ID.
        :param offset: Get programs starting by the specified offset.
        :param search: Filter by specified name.

        :return: A list of programs.

        :raise Exception: When an unexpected error occurs.
        """
        try:
            records: list[dict[str, Any]] = []
            limit: int = 50 if not limit else limit
            offset: int = 0 if not offset else offset

            while True:
                response: dict[str, Any] = self.client.get_all_programs(
                    following=following,
                    limit=limit,
                    offset=offset,
                    status_id=match_status,
                    type_id=match_type,
                )
                offset += limit
                records.extend(response['records'])

                if offset >= response['maxCount']:
                    break

            programs: list[IntigritiProgramSlim] = [
                IntigritiParser.to_program_slim(record) for record in records
            ]

            programs.sort()

            filtered_programs: list[IntigritiProgramSlim] = []

            if search:
                [
                    filtered_programs.append(program)
                    for program in programs
                    if search.lower() in program.name.lower()
                ]
                return filtered_programs

            return programs

        except Exception as ex:
            self.logger.exception(str(ex), exc_info=True)
            raise

    def get_program(self, program_id: str) -> IntigritiProgram:
        """
        Gets program information.

        :return: A program with its information.

        :raise Exception: When an unexpected error occurs.
        """
        try:
            response: dict[str, Any] = self.client.get_program_details(
                program_id=program_id
            )

            return IntigritiParser.to_program(response)

        except Exception as ex:
            self.logger.exception(str(ex), exc_info=True)
            raise
