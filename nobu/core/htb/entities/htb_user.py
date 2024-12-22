from pydantic import AliasChoices, BaseModel, Field


class HtbUser(BaseModel):
    """
    Represents an HTB user.
    """

    avatar: str
    """Endpoint of the user's avatar."""

    id: int
    """Unique identifier of the user."""

    is_respected: bool | None = Field(default=None, alias='isRespected')
    """If the current user already respected this user."""

    name: str = Field(validation_alias=AliasChoices('name', 'value'))
    """Name of the user."""
