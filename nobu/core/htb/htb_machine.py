from datetime import datetime

from pydantic import AliasChoices, BaseModel, Field

from .htb_academy_module import HtbAcademyModule
from .htb_feedback import HtbFeedback
from .htb_first_blood import HtbFirstBlood
from .htb_label import HtbLabel
from .htb_play_info import HtbPlayInfo
from .htb_user import HtbUser


class HtbMachine(BaseModel):
    """Represents an HTB machine."""

    academy_modules: list[HtbAcademyModule] = None
    """Related HTB Academy modules."""

    active: bool | None = None
    """If machine is in active state."""

    auth_user_first_user_time: str | None = Field(
        default=None, alias='authUserFirstUserTime'
    )
    """Total time taken to get user flag by the user since machine
    release."""

    auth_user_first_root_time: str | None = Field(
        default=None, alias='authUserFirstRootTime'
    )
    """Total time taken to get root flag by the user since machine
    release."""

    auth_user_has_reviewed: bool | None = Field(
        default=None, alias='authUserHasReviewed'
    )
    """If the user already reviewed the machine."""

    auth_user_has_submitted_matrix: bool | None = Field(
        default=None, alias='authUserHasSubmittedMatrix'
    )
    """If the user already submitted machine matrix rates."""

    auth_user_in_root_owns: bool | None = Field(
        default=None, alias='authUserInRootOwns'
    )
    """If the user already got the root flag."""

    auth_user_in_user_owns: bool | None = Field(
        default=None, alias='authUserInUserOwns'
    )
    """If the user already got the user flag."""

    avatar: str
    """Endpoint of the machine's avatar."""

    can_access_walkthrough: bool | None = None
    """If user can access the machine walkthrough."""

    difficulty: int | None = None
    """Difficulty rate of the machine."""

    difficulty_text: str | None = Field(default=None, alias='difficultyText')
    """Difficulty rate of the machine in a text format."""

    feedback: HtbFeedback | None = Field(
        default=None, alias='feedbackForChart'
    )
    """Difficulty of the machine rated by users."""

    free: bool | None = None
    """If the machine is free or needs a VIP plan to be played."""

    has_changelog: bool | None = None
    """If the machine has any change log."""

    id: int
    """Unique identifier of the machine."""

    ip: str | None = None
    """Machine IP if spawned."""

    is_competitive: bool | None = None
    """If machine is related to an active season."""

    is_completed: bool | None = Field(default=None, alias='isCompleted')
    """If the user already finished the machine."""

    is_guided_enabled: bool | None = Field(
        default=None, alias='isGuidedEnabled'
    )
    """If machine guided mode is enabled."""

    is_todo: bool | None = Field(
        default=None, validation_alias=AliasChoices('isTodo', 'is_todo')
    )
    """If machine is selected as todo by the user."""

    labels: list[HtbLabel] | None = None
    """Labels for the machine."""

    last_reset_time: datetime | None = None
    """Last time the machine was reset."""

    machine_mode: str | None = None
    """Spawn mode for the machine."""

    makers: list[HtbUser] | None = None
    """Makers of the machine."""

    name: str = Field(validation_alias=AliasChoices('name', 'value'))
    """Name of the machine."""

    os: str | None = None
    """Operating system of the machine."""

    own_rank: int | None = Field(default=None, alias='ownRank')
    """User position in own rank."""

    play_info: HtbPlayInfo | None = Field(default=None, alias='playInfo')
    """Play info state of the machine."""

    points: int | None = None
    """How many points the machine is currently worth."""

    recommended: int | None = None
    """If machine is recommended to the player by HTB."""

    release: datetime | None = None
    """Release date of the machine."""

    retired: int | None = None
    """If the machine is in retired state."""

    reviews_count: int | None = None
    """Total reviews of the machine."""

    root_blood: HtbFirstBlood | None = Field(default=None, alias='rootBlood')
    """First root blood of the machine."""

    root_owns_count: int | None = None
    """Total users that already got root flag."""

    season_id: int | None = None
    """Season identifier."""

    static_points: int | None = None
    """How many points the machine is worth."""

    sp_flag: int | None = None
    """Starting point flag."""

    stars: float | None = Field(
        default=None, validation_alias=AliasChoices('star', 'stars')
    )
    """Machine rate."""

    synopsis: str | None = None
    """Synopsis of the machine."""

    user_blood: HtbFirstBlood | None = Field(default=None, alias='userBlood')
    """First user blood of the machine."""

    user_can_review: bool | None = None
    """If user can submit a review to the machine."""

    user_owns_count: int | None = None
    """Total users that already got user flag."""

    def __gt__(self, other: 'HtbMachine') -> bool:
        """
        Overrides the default way to compare if a machine is greater
        than another based on its ID.

        :param: Machine to be compared.

        :return: True if the current object machine ID is greater than
         other machine ID, false otherwise.
        """
        return self.id > other.id
