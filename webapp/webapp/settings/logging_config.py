"""Logging configuration."""

from django.template.base import VariableDoesNotExist

EXCLUDE_EXCEPTIONS = [
    VariableDoesNotExist,
]


def filter_exc_types(record):
    """Exclude whitelisted exception types."""
    if record.exc_info:
        exc = record.exc_info[1]
        for excluded in EXCLUDE_EXCEPTIONS:
            if isinstance(exc, excluded):
                return False
    return True


def configure_logging(LOG_ROOT):
    """Return logging configuration."""
    return {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '{levelname} | {asctime} | {module}: {message}',
                'style': '{',
            },
        },
        'filters': {
            'filter_exc_type': {
                '()': 'django.utils.log.CallbackFilter',
                'callback': filter_exc_types,
            },
        },
        'handlers': {
            'debug_file': {
                'delay': True,
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 1000000,  # 1MB ~ 20k rows
                'backupCount': 5,
                'filename': LOG_ROOT / 'debug.log',
                'formatter': 'verbose',
                'filters': ['filter_exc_type'],
            },
            'main_file': {
                'delay': True,
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 1000000,  # 1MB ~ 20k rows
                'backupCount': 5,
                'filename': LOG_ROOT / 'main.log',
                'formatter': 'verbose',
            },
            'error_file': {
                'delay': True,
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 1000000,  # 1MB ~ 20k rows
                'backupCount': 5,
                'filename': LOG_ROOT / 'error.log',
                'formatter': 'verbose',
            },
            'error_mail': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'formatter': 'verbose',
            },
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['debug_file', 'error_file', 'console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.utils.autoreload': {
                'level': 'WARNING',  # This logger is way too noisy on DEBUG
            }
        },
    }
