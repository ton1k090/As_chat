# -*- coding: utf-8 -*-
import argparse
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
def client_message(message, messages_list, client, clients, names):
    server_logger.debug(f'Разбор сообщения от клиента : {message}')
    if 'action' in message and message['action'] == 'presence' and \
            'time' in message and 'user' in message:
        if message['user']['account_name'] not in names.keys():
            names[message['user']['account_name']] = client
            send_message(client, {'response': 200})
        else:
            response = {'response': 400}
            response['error'] = 'Имя пользователя занято.'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    elif 'action' in message and message['action'] == 'message' and \
            'to' in message and 'time' in message \
            and 'from' in message and 'message_text' in message:
        messages_list.append(message)
        return
    elif 'action' in message and message['action'] == 'exit' and 'account_name' in message:
        clients.remove(names[message['account_name']])
        names[message['account_name']].close()
        del names[message['account_name']]
        return
    else:
        response = {'response': 400}
        response['error'] = 'Запрос некорректен.'
        send_message(client, response)
        return


@log
def get_params():

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = 7773
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


@log
def process_message(message, names, listen_socks):
    if message['to'] in names and names[message['to']] in listen_socks:
        send_message(names[message['to']], message)
        server_logger.info(f'Отправлено сообщение пользователю {message["to"]} '
                    f'от пользователя {message["from"]}.')
    elif message['to'] in names and names[message['to']] not in listen_socks:
        raise ConnectionError
    else:
        server_logger.error(
            f'Пользователь {message["to"]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=7773, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        server_logger.critical(
            f'Попытка запуска сервера с указанием неподходящего порта {listen_port}. '
            f'Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


@log
def main():

    listen_address, listen_port = arg_parser()

    server_logger.info(
        f'Запущен сервер, порт для подключений: {listen_port}, '
        f'адрес с которого принимаются подключения: {listen_address}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((listen_address, listen_port))
    s.settimeout(0.5)

    clients = []
    messages = []

    names = dict()
    s.listen(5)
    while True:
        try:
            client, client_address = s.accept()
        except OSError:
            pass
        else:
            server_logger.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    client_message(get_message(client_with_message),
                                           messages, client_with_message, clients, names)
                except Exception:
                    server_logger.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_with_message)

        for i in messages:
            try:
                process_message(i, names, send_data_lst)
            except Exception:
                server_logger.info(f'Связь с клиентом с именем {i["to"]} была потеряна')
                clients.remove(names[i["to"]])
                del names[i["to"]]
        messages.clear()


if __name__ == '__main__':
    main()