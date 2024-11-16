from pydantic import BaseModel


class HtbAcademyModuleDifficulty(BaseModel):
    """Represents an HTB Academy module difficulty."""

    color: str
    """Color of the module difficulty label."""

    level: int
    """Level of the difficulty."""

    title: str
    """Title of the difficulty."""
