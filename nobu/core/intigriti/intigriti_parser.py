import logging
from typing import Any

from .entities import IntigritiDomain, IntigritiProgram, IntigritiProgramSlim


class IntigritiParser:
    _logger: logging.Logger = logging.getLogger(__name__)

    @classmethod
    def to_domains(
        cls, domains_dict: dict[str, Any]
    ) -> list[IntigritiDomain | None]:
        content = domains_dict['content']
        domains: list[IntigritiDomain] = []

        for item in content:
            domains.append(IntigritiDomain(**item))

        return domains

    @classmethod
    def to_program(cls, program_dict: dict[str, Any]) -> IntigritiProgram:
        domains: list[IntigritiDomain] = IntigritiParser.to_domains(
            program_dict['domains']
        )
        del program_dict['domains']

        return IntigritiProgram(**program_dict, domains=domains)

    @classmethod
    def to_program_slim(
        cls, program_slim_dict: dict[str, Any]
    ) -> IntigritiProgramSlim:
        return IntigritiProgramSlim(**program_slim_dict)
