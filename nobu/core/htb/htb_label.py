from pydantic import BaseModel


class HtbLabel(BaseModel):
    """Represents machine labels."""

    color: str
    """Color of the label."""

    name: str
    """Name of the label."""
