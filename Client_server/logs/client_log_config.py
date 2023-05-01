# -*- coding: utf-8 -*-
import logging
import os
import sys

sys.path.append('../')


client_format = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s ')

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'client.logs')
login_lvl = logging.DEBUG

hand = logging.StreamHandler(sys.stderr)
hand.setLevel(login_lvl)
hand.setFormatter(client_format)

file = logging.FileHandler(path, encoding='utf-8')
file.setFormatter(client_format)

log = logging.getLogger('client')
log.addHandler(hand)
log.addHandler(file)
log.setLevel(login_lvl)

if __name__ == '__main__':
    log.critical('Критическая ошибка')
    log.error('Ошибка')
    log.debug('Отладочная информация')
    log.info('Информационное сообщение')