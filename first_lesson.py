import subprocess


# 1
from Tools.scripts.objgraph import ignore

var = 'разработка'
var_1 = 'сокет'
var_2 = 'декоратор'

list_var = [var, var_1, var_2]
for i in list_var:
    print(type(i), '-', i)

print()

var_u = u'\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
var_1_u = u'\u0441\u043e\u043a\u0435\u0442'
var_2_u = u'\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

list_var_u = [var_u, var_1_u, var_2]
for i in list_var_u:
    print(type(i), '-', i)

print()

# 2

var = [b'class', b'function', b'method']
for i in var:
    print(type(i), '-', i, '-', len(i))

print()

# 3

# var = [b'attribute', b'класс', b'функция', b'type'] # Кириллица выдает исключение

print()

# 4

for let in ['разработка', 'администрирование', 'protocol', 'standard']:
    e = let.encode('utf-8', ignore)
    d = bytes.decode(e, 'utf-8')
    print(f'encode {e} - decode {d}')

# 5
for sites in ['yandex.ru','youtube.com']:
    args = ['ping', sites]
    subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)

for line in subproc_ping.stdout:
    line = line.decode('cp866').encode('utf-8')
    print(line.decode('utf-8'))

print()
