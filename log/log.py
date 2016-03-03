# -*- coding: utf-8 -*-
"""日志记录模块
usage:
    from log import get_logger
    ....
    logger = get_logger("name", path)
    ...
    logger.info(...)
    logger.error(...)

    ======
    or
    import logging
    from logging import config

    from log import config

    config.dictConfig(config)
    logger = logging.getLogger(__name__)

    logger.info(...)
    logger.error(...)
"""
import logging
from logging import handlers

config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': ("[%(asctime)s] #%(levelname)s "
                       "[%(name)s, line:%(lineno)s] %(message)s"),
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            # 当达到100MB时分割日志
            'maxBytes': 1024 * 1024 * 100,
            # 最多保留50份文件
            'backupCount': 50,
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': True,
            'filename': 'mysite.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    }
}


def setup_logger(logger, log_path, level="debug"):
    level_dict = {"critical": logging.CRITICAL,
                  "error": logging.ERROR,
                  "warning": logging.WARNING,
                  "info": logging.INFO,
                  "debug": logging.DEBUG}
    log_level = level_dict.get(level, logging.DEBUG)
    logger.setLevel(log_level)
    handler = handlers.TimedRotatingFileHandler(log_path, when='d', interval=1)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_logger(name, path):
    logger = logging.getLogger(name)
    setup_logger(logger, path)
    return logger


if __name__ == "__main__":
    import logging.config
    logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)
    logger.info('log info')
