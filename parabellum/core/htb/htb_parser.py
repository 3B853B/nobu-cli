import logging
from typing import Any

from .htb_machine import HtbMachine
from .htb_user import HtbUser


class HtbParser:
    _logger: logging.Logger = logging.getLogger(__name__)

    @classmethod
    def to_machine_list(cls, machines: dict[str, Any]) -> list[HtbMachine]:
        try:
            data: list[str, Any] = machines['data']
            return [HtbParser.to_machine(machine) for machine in data]
        except Exception as ex:
            cls._logger.exception(str(ex), exc_info=True)
            raise

    @classmethod
    def to_machine(cls, machine_dict: dict[str, Any]) -> HtbMachine:
        try:
            makers: list[HtbUser] = []
            for user in [
                machine_dict.get('maker'),
                machine_dict.get('maker2'),
            ]:
                if user:
                    makers.append(HtbUser(**user))

            return HtbMachine(**machine_dict, makers=makers)

        except Exception as ex:
            cls._logger.exception(str(ex), exc_info=True)
            raise
