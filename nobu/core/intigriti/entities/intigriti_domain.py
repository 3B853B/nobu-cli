from pydantic import AliasPath, BaseModel, Field, field_validator


class IntigritiDomain(BaseModel):
    id: str
    type: str = Field(validation_alias=AliasPath('type', 'value'))
    tier: str = Field(validation_alias=AliasPath('tier', 'value'))
    endpoint: str
    description: str

    @field_validator('description', mode='before')
    @classmethod
    def default_description(cls, description: str) -> str:
        return description or '-'
