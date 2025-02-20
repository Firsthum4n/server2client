dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": f" %(asctime)s ; %(message)s ",
            "datefmt": "%Y-%m-%d"
        }
    },
    "handlers": {
        "file_1": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filename": "server.log",
            "mode": "a",
        },
        "file_2": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filename": "client.log",
            "mode": "a",
        }
    },
    "loggers": {
        "server_logger": {
            "level": "DEBUG",
            "handlers": ["file_1"]
        },
        "client_logger": {
            "level": "DEBUG",
            "handlers": ["file_2"]
        }
    }
}