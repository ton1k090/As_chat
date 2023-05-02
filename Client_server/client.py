# -*- coding: utf-8 -*-
import argparse
import logging
import sys
import threading
from socket import *
import socket
import json
import time
from modules.message import get_message, send_message
import logs.client_log_config
from decorator_log import log


client_logger = logging.getLogger('client')


@log
def create_logout(acc_name):
    return {
        'action': 'exit',
        'time': time.time(),
        'account_name': acc_name
    }


@log
def message_from_server(socks, my_username):
    while True:
        try:
            message = get_message(socks)
            if 'action' in message and message['action'] == message and 'from' in message and \
                'to' in message and 'message_text' in message and message['to'] == my_username:
                    print(f'\nПолучено сообщение от пользователя {message["from"]}:'
                    f'\n{message["message_text"]}')
                    client_logger.info(f'Получено сообщение от пользователя {message["from"]}:'
                    f'\n{message["message_text"]}')
            else:
                client_logger.error(f'Получено некорректное сообщение с сервера: {message}')
        except BaseException :
            client_logger.error(f'Не удалось декодировать полученное сообщение.')
        except ConnectionResetError:
            client_logger.critical(f'Потеряно соединение с сервером.')
            break


@log
def create_message(socks, acc_name='Guest'):
    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        'action': 'message',
        'from': 'acc_name',
        'to': to_user,
        'time': time.time(),
        'message_text': message
    }
    client_logger.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_message(socks, message_dict)
        client_logger.info(f'Отправлено сообщение для пользователя {to_user}')
    except:
        client_logger.critical('Потеряно соединение с сервером.')
        sys.exit(1)


@log
def user_interactive(socks, username):
    while True:
        command = input(f'Введите команду'
                        '(message - отправить сообщение, exit - выход из программы)')
        if command == 'message':
            create_message(socks, username)
        elif command == 'exit':
            send_message(socks, create_logout(username))
            print('Завершение соединения.')
            client_logger.info('Завершение работы по команде пользователя.')
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова.')


@log
def create_presence(acc_name):

    out = {
        'action': 'presence',
        'time': time.time(),
        'user': {
            'account_name': acc_name
        }
    }
    client_logger.debug(f'Сформировано {"presence"} сообщение для пользователя {acc_name}')
    return out


@log
def process_response_ans(message):

    client_logger.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if 'response' in message:
        if message['response'] == 200:
            return '200 : OK'
        elif message['response'] == 400:
            raise ConnectionResetError(f'400 : {message["error"]}')
    raise ConnectionError('response')


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default='127.0.0.1', nargs='?')
    parser.add_argument('port', default=7773, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    if not 1023 < server_port < 65536:
        client_logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    return server_address, server_port, client_name


@log
def main():
    print('Консольный месседжер. Клиентский модуль.')

    server_address, server_port, client_name = arg_parser()
    if not client_name:
        client_name = input('Введите имя пользователя: ')
        client_logger.info(
            f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
            f'порт: {server_port}, имя пользователя: {client_name}')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_address, server_port))
        send_message(s, create_presence(client_name))
        answer = process_response_ans(get_message(s))
        client_logger.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером. Ответ сервера: {answer}')
    except json.JSONDecodeError:
        client_logger.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except (ConnectionRefusedError, ConnectionError):
        client_logger.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        receiver = threading.Thread(target=message_from_server, args=(s, client_name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=user_interactive, args=(s, client_name))
        user_interface.daemon = True
        user_interface.start()
        client_logger.debug('Запущены процессы')

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()