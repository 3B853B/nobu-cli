from datetime import datetime

from pydantic import BaseModel, Field


class HtbPlayInfo(BaseModel):
    """
    Represents the current play info state of the machine.
    """

    active_player_count: int | None = None
    """Numbers of players currently playing the machine."""

    expires_at: datetime | None = None
    """Expiration date if the machine is active."""

    is_active: bool | None = Field(default=None, alias='isActive')
    """If the machine is currently active."""

    is_spawned: bool | None = Field(default=None, alias='isSpawned')
    """If the machine is already spawned."""

    is_spawning: bool | None = Field(default=None, alias='isSpawning')
    """If the machine is currently spawning."""
