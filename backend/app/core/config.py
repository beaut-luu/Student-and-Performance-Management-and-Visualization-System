# pydantic-settings：DATABASE_URL / SECRET_KEY / ADMIN_SECRET / 过期时间
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # MYSQL配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    # JWT配置与管理员密钥
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 访问令牌过期时间（分钟）
    SECRET_KEY: str  # 签名密钥
    ALGORITHM: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        return (f"mysql+aiomysql://{self.DB_USERNAME}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
