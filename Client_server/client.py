# -*- coding: utf-8 -*-

import sys
from socket import *
import socket
import json
import time
from modules.message import get_message, send_message


def presence_message(acc_name='Guest'):
    out = {
        'actions': 'presence',
        'time': time.time(),
        'user': {
            'account_name': 'Guest'
        }
    }
    return out


def main():

    try:
        server_address = sys.argv[1]
        server_port = sys.argv[2]
        if server_port != 10000:
            raise ValueError
    except IndexError:
        server_address = '127.0.0.1'
        server_port = 7777
    except ValueError:
        print(f'Сервер использует порт - 7777')
        sys.exit(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_address, server_port))

    message = presence_message()
    send_message(s, message)
    try:
        answer = presence_message(get_message(s))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()