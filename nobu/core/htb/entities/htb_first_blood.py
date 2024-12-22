from datetime import datetime

from pydantic import BaseModel

from .htb_user import HtbUser


class HtbFirstBlood(BaseModel):
    """
    Holds information related to first blood.
    """

    blood_difference: str
    """Difference between release date and first blood in text
    format."""

    created_at: datetime
    """Date the blood was got."""

    user: HtbUser
    """User that got the first blood."""
