# -*- coding: utf-8 -*-
import logging
import socket
import sys
import json
from modules.message import send_message, get_message
import logs.server_log_config

server_logger = logging.getLogger('server')


def client_message(message):
    server_logger.debug(f'{message}')
    if message['user']['account_name'] == 'Guest' and message['actions'] == 'presence':
        return {'response': 200,
                'alert': 'OK'}
    else:
        return {'response': 400,
                'alert': 'Bad request'}


def get_params():

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = 7775
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


def main():

    get_params()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 7775))
    s.listen(5)
    server_logger.info('Ожидаю подключение')

    while True:

        client, address = s.accept()
        server_logger.info(f'Получен запрос на соединение от {address}' )
        try:
            message = get_message(client)
            server_logger.debug(f'{message}')
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = client_message(message)
            send_message(client, response)
            server_logger.info(f'Ответ клиенту {response}')
            server_logger.debug(f'Соединение с  {address} закрывается.')
            client.close()
        except (ValueError, json.JSONDecodeError):
            server_logger.error('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
