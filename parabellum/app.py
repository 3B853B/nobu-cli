import logging
import logging.config

from parabellum.cmd import ParabellumCmd


def run() -> None:
    """
    Starts the main application console.
    """
    logging.basicConfig(
        level=logging.CRITICAL,
        format='[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
    )

    parabellum_cmd: ParabellumCmd = ParabellumCmd()
    try:
        parabellum_cmd.cmdloop()
    except KeyboardInterrupt:
        parabellum_cmd.do_exit()
