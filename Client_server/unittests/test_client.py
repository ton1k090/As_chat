import sys
import os
import unittest
import time

sys.path.append(os.path.join(os.getcwd(), '..'))
from Client_server.client import presence_message


class TestClient(unittest.TestCase):

    def test_message(self):
        '''Тест корреутного запроса'''
        test = presence_message()
        test['time'] = 1
        self.assertEqual(test,
            {'actions': 'presence', 'time': 1, 'user': {'account_name': 'Guest'}})


if __name__ == '__main__':
    unittest.main()