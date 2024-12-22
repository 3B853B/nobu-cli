from pydantic import BaseModel


class HtbAcademyModuleTier(BaseModel):
    """Represents an HTB Academy module tier."""

    color: str
    """Color of the module tier label."""

    name: str
    """Name of the tier."""

    number: int
    """Number of the tier."""
