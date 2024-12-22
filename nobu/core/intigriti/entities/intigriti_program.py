from pydantic import AliasPath, BaseModel, Field

from .intigriti_domain import IntigritiDomain


class IntigritiProgram(BaseModel):
    id: str
    handle: str
    name: str
    confidentiality_level: str = Field(
        validation_alias=AliasPath('confidentialityLevel', 'value')
    )
    status: str = Field(validation_alias=AliasPath('status', 'value'))
    domains: list[IntigritiDomain | None]
