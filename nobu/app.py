import logging
import logging.config

from nobu.cmd import NobuCmd


def run() -> None:
    """
    Starts the main application console.
    """
    logging.basicConfig(
        level=logging.CRITICAL,
        format='[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
    )

    nobu_cmd: NobuCmd = NobuCmd()
    try:
        nobu_cmd.cmdloop()
    except KeyboardInterrupt:
        nobu_cmd.do_exit()
