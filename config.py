import os
from typing import Optional, Type


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(os.path.dirname(__file__), 'instance', 'app.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config_by_name: dict[str, Type[Config]] = {
    "default": Config,
    "testing": TestConfig,
}


def get_config(name: Optional[str] = None) -> Type[Config]:
    return config_by_name.get(name or os.environ.get("FLASK_ENV", "default"), Config)
