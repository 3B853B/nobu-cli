from parabellum.cmd import ParabellumCmd


def run() -> None:
    """
    Starts the main application console.
    """
    parabellum_cmd = ParabellumCmd()
    try:
        parabellum_cmd.cmdloop()
    except KeyboardInterrupt:
        parabellum_cmd.do_exit()
