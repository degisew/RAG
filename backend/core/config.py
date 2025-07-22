from pydantic_settings import BaseSettings, SettingsConfigDict, DotEnvSettingsSource


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore")


settings = Settings()  # type: ignore
