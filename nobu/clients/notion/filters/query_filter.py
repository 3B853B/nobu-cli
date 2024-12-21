from pydantic import BaseModel, ConfigDict

from .filter_property import FilterProperty
from .filter_value import FilterValue


class QueryFilter(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    value: FilterValue
    property: FilterProperty
