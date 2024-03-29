from settings.base import BaseSettings


class Settings(BaseSettings):
    LOGGING_LEVEL: str = "DEBUG"
    LOGGING_JSON: bool = True

    @property
    def log_config(self) -> dict:
        config = {
            "loggers": {
                "uvicorn": {
                    "handlers": ["default"],
                    "level": self.LOGGING_LEVEL,
                    "propagate": False,
                },
                "sqlalchemy": {
                    "handlers": ["default"],
                    "level": self.LOGGING_LEVEL,
                    "propagate": False,
                },
                "aio-pika": {
                    "handlers": ["default"],
                    "level": self.LOGGING_LEVEL,
                    "propagate": False,
                },
            }
        }

        return config


logger_settings = Settings()
