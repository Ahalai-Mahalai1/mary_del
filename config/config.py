from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
@dataclass
class Database:
    db_url: str

@dataclass
class Config:
    bot: TgBot
    db: Database


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        bot=TgBot(token=env('BOT_TOKEN')),
        d_base=Database(db_url=env('DATABASE_URL'))
        )
