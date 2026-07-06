from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_name: str = 'UCC CoDE Connect'
    environment: str = 'development'
    secret_key: str = 'change-this-before-production-minimum-32-chars'
    access_token_expire_minutes: int = 1440
    database_url: str = 'sqlite:///./code_connect.db'
    cors_origins: str = '*'
    myucc_url: str = 'https://my.ucc.edu.gh/login'
    ucc_elearning_url: str = 'https://elearning.ucc.edu.gh/'
    code_website_url: str = 'https://code.ucc.edu.gh/'

    @property
    def cors_origin_list(self) -> List[str]:
        if self.cors_origins.strip() == '*':
            return ['*']
        return [item.strip() for item in self.cors_origins.split(',') if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
