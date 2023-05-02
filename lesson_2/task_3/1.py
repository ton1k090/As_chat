import yaml

data = {
    'item': ['iphone', 'samsung'],
    'quantity': 2,
    'price': {
        'iphone': '600$ - 2000$',
        'samsung': '400$ - 2000$'
    }
}

with open('file.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(data, file, default_flow_style=True, allow_unicode=True)

with open('file.yaml', 'r', encoding='utf-8') as file:
    print(file.read())