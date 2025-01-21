DATABASE = {
    "host": "db",
    "user": "admin",
    "password": "admin",
    "database": "app_db",
    "test_database": "test_db",
    "check_same_thread": False,
    "connection": "postgresql+asyncpg",
    "autocommit": False,
    "autoflush": False,
    "port": 5439,
    "test_port": 5440,
    "extra_params": ""
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
