from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', extra='allow'
    )


settings = Settings().model_dump()
# print(settings)
DB_URL: str = settings["db_url"]
SECRET_KEY: str = settings["secret_key"]
ALGORITHM: str = settings["algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES: int = settings["access_token_expire_minutes"]
LOG_FILE: str = settings["log_file"]
