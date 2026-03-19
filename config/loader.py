from dataclasses import dataclass
from environs import Env

env = Env()
env.read_env()


@dataclass
class Bot:
    token: str

    @staticmethod
    def from_env(env_path: str | None = None) -> "Bot":
        if env_path:
            env.read_env(env_path)
        return Bot(token=env.str("BOT_TOKEN"))


@dataclass
class Database:
    host: str
    port: int
    user: str
    name: str
    password: str

    @staticmethod
    def from_env(env_path: str | None = None) -> "Database":
        if env_path:
            env.read_env(env_path)
        return Database(
            host=env.str("DB_HOST"),
            port=env.int("DB_PORT"),
            user=env.str("DB_USER"),
            name=env.str("DB_NAME"),
            password=env.str("DB_PASSWORD"),
        )

@dataclass
class Config:
    bot: Bot
    db: Database

    @staticmethod
    def from_env(env_path: str | None = None) -> "Config":
        if env_path:
            env.read_env(env_path)
        return Config(
            bot=Bot.from_env(),
            db=Database.from_env(),
        )

settings = Config.from_env()
