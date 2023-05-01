"""Лаунчер"""

import subprocess

process_lists = []

while True:
    user_actions = input('S - запустить, X - закрыть, Q -  выход')

    if user_actions == 'q'.upper().lower():
        break
    elif user_actions == 's'.upper().lower():
        process_lists.append(subprocess.Popen('python server.py',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(2):
            process_lists.append(subprocess.Popen('python client.py -m send',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(5):
            process_lists.append(subprocess.Popen('python client.py -m listen',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif user_actions == 'x':
        while process_lists:
            VICTIM = process_lists.pop()
            VICTIM.kill()
