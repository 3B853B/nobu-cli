from pydantic import AliasPath, BaseModel, Field


class IntigritiProgramSlim(BaseModel):
    id: str
    handle: str
    name: str
    confidentiality_level: str = Field(
        validation_alias=AliasPath('confidentialityLevel', 'value')
    )
    status: str = Field(validation_alias=AliasPath('status', 'value'))

    def __lt__(self, other: 'IntigritiProgramSlim') -> bool:
        return self.name < other.name
