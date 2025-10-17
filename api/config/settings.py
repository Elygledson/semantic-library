from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_DB: str
    REDIS_HOST: str
    REDIS_PORT: str
    SECRET_KEY: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_PASSWORD: str
    AI_SERVICE_KEY: str
    SWAGGER_USERNAME: str
    SWAGGER_PASSWORD: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @property
    def redis_url(self) -> str:
        return (
            f"redis://{self.REDIS_HOST}:"
            f"{self.REDIS_PORT}/"
            f"{self.REDIS_DB}"
        )

    class Config:
        env_file = ".env",
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
