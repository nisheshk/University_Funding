LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'default': {
            'level': 'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'logs/mylogs.log',
            'formatter': 'standard',
            'maxBytes': 1024*1024*5   #5MB
        },
        'request_handler': {
            'level': 'WARNING',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django_request.log',
            'class':'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'maxBytes': 1024*1024*5   #5MB
        },
    },
    'loggers': {
        '':{
            'handlers': ['default','console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO'
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}
