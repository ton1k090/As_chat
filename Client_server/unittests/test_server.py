# -*- coding: utf-8 -*-
import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from Client_server.server import client_message


class TestServer(unittest.TestCase):

    def test_correct(self):
        '''Тест корректного запроса'''
        self.assertEqual(client_message(
            {'actions': 'presence', 'user': {'account_name': 'Guest'}}), ({'response': 200, 'alert': 'OK'}))

    def test_user(self):
        '''Тест проверки имя пользователя'''
        self.assertEqual(client_message(
            {'actions': 'presence', 'user': {'account_name': 'Guest1'}}), ({'response': 400, 'alert': 'Bad request'}))

    def test_action(self):
        '''Тест проверки действия'''
        self.assertEqual(client_message(
            {'user': {'account_name': 'Guest1'}}), ({'response': 400, 'alert': 'Bad request'}))

    def test_actions_wrong(self):
        '''Тест проверки неизвестного действия'''
        self.assertEqual(client_message(
            {'actions': 'wrong', 'user': {'account_name': 'Guest'}}), ({'response': 400, 'alert': 'Bad request'}))


if __name__ == '__main__':
    unittest.main()