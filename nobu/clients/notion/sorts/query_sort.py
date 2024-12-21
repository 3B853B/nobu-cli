from pydantic import BaseModel, ConfigDict

from .sort_direction import SortDirection
from .sort_timestamp import SortTimestamp


class QuerySort(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    direction: SortDirection
    timestamp: SortTimestamp
