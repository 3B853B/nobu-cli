from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    htb_token: str | None = None
    notion_root_page_id: str | None = None
    notion_token: str | None = None
