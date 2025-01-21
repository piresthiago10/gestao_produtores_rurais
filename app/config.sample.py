DATABASE = {
    "host": "postgres_db",
    "user": "admin",
    "password": "admin",
    "database": "app_db",
    "connection": "postgresql+asyncpg",
    "autocommit": False,
    "autoflush": False,
    "port": 5432,
}

DATABASE_TEST = {
    "host": "postgres_db_test",
    "user": "admin",
    "password": "admin",
    "database": "test_db",
    "connection": "postgresql+asyncpg",
    "autocommit": False,
    "autoflush": False,
    "port": 5432,
}

JWT = {
    "secret_key": "your_secret_key_here",
    "algotithm": "HS256",
    "access_token_expire_minutes": 30
}

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app/logs/log_files/app.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "default"
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
