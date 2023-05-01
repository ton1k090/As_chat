# -*- coding: utf-8 -*-
import logging
import socket
import sys
import json

import select

from modules.message import send_message, get_message
import logs.server_log_config
from decorator_log import log

server_logger = logging.getLogger('server')


@log
def client_message(message):
    server_logger.debug(f'{message}')
    if message['user']['account_name'] == 'Guest' and message['actions'] == 'presence':
        return {'response': 200,
                'alert': 'OK'}
    else:
        return {'response': 400,
                'alert': 'Bad request'}


@log
def get_params():

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = 7774
        if listen_port < 1024 or listen_port > 65535:
            server_logger.critical(ValueError)
    except IndexError:
        print('Укажите номер порта после параметра - \'p\'')
        server_logger.error('Не указан порт')
        sys.exit(1)
    except ValueError:
        server_logger.error('Указан неверный порт')
        print('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = '127.0.0.1'

    except IndexError:
        server_logger.error('Не указан адресс после параметров')
        print('Укажите адресс после параметра - \'a\'')
        sys.exit(1)

    return listen_address, listen_port


def main():

    listen_address, listen_port = get_params()

    server_logger.info(
        f'Запущен сервер, порт для подключений: {listen_port}, '
        f'адрес с которого принимаются подключения: {listen_address}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((listen_address, listen_port))
    s.settimeout(0.5)
    server_logger.info('Ожидаю подключение')

    clients = []
    messages = []
    s.listen(5)

    while True:
        try:
            client, address = s.accept()
        except OSError:
            pass
        else:
            server_logger.info(f'Получен запрос на соединение от {address}' )
            clients.append(client)
        finally:

            recv = []
            send = []
            err = []

        try:
            if clients:
                recv, send, err = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv:
            for mess in recv:
                try:
                    client_message(get_message(mess), messages, mess)
                except:
                    server_logger.info(f'Клиент {mess.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(mess)








if __name__ == '__main__':
    main()
