# -*- coding: utf-8 -*-

import socket
import sys
import json
from modules.message import send_message, get_message


def client_message(message):
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
            listen_port = 7777
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('Укажите номер порта после параметра - \'p\'')
        sys.exit(1)
    except ValueError:
        print('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = '127.0.0.1'

    except IndexError:
        print('Укажите адресс после параметра - \'a\'')
        sys.exit(1)


def main():

    get_params()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 7777))
    s.listen(5)
    print('Ожидаю подключение...')

    while True:

        client, address = s.accept()
        print("Получен запрос на соединение от %s" % str(address))
        try:
            message = get_message(client)
            print(message)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = client_message(message)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
