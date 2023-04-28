# -*- coding: utf-8 -*-
import logging
import sys
from socket import *
import socket
import json
import time
from modules.message import get_message, send_message
import logs.client_log_config
from decorator_log import log


client_logger = logging.getLogger('client')


@log
def presence_message(acc_name='Guest'):
    out = {
        'actions': 'presence',
        'time': time.time(),
        'user': {
            'account_name': 'Guest'
        }
    }
    client_logger.debug('Сформировано сообщение для пользователя ')
    return out


def main():

    try:
        server_address = sys.argv[1]
        server_port = sys.argv[2]
        if server_port != 10000:
            raise ValueError
    except IndexError:
        server_address = '127.0.0.1'
        server_port = 7775
    except ValueError:
        client_logger.critical(f'Попытка запуска клиента с неверным портом')
        sys.exit(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_address, server_port))

    message = presence_message()
    send_message(s, message)
    try:
        answer = presence_message(get_message(s))
        client_logger.info(f'Получен ответ от сервера {answer}')
        print(answer)
    except (ValueError, json.JSONDecodeError):
        client_logger.error('Не удалось декодировать полученый текст')


if __name__ == '__main__':
    main()