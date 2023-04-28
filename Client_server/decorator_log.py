# -*- coding: utf-8 -*-
import sys
import logging
import logs.server_log_config
import logs.client_log_config

if __name__ == 'server':
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log(func):

    def log_server(*args, **kwargs):
        res = func(*args, **kwargs)
        logger.debug(f'Вызов функции {func.__name__} из модуля {func.__module__}  с  параметрами {args}, {kwargs}')
        return res

    return log_server
