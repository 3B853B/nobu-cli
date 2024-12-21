from pydantic import BaseModel

from .htb_academy_module_difficulty import HtbAcademyModuleDifficulty
from .htb_academy_module_tier import HtbAcademyModuleTier


class HtbAcademyModule(BaseModel):
    """Represents an HTB Academy module."""

    avatar: str
    """URL of the module avatar."""

    id: int
    """Unique identifier of the module."""

    difficulty: HtbAcademyModuleDifficulty
    """Difficulty of the module."""

    logo: str
    """URL of the module logo."""

    name: str
    """Name of the module."""

    tier: HtbAcademyModuleTier
    """Tier of the module."""

    url: str
    """URL of the module."""
