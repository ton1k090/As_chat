import json


def write_order_to_json(item, quantity, price, buyer, date):

    order_list = {'item': item,
                  'quantity': quantity,
                   'price': price,
                   'buyer': buyer,
                   'date': date
                  }

    with open('orders.json', 'w', encoding='utf-8') as file:
        json.dump(order_list, file, sort_keys=True, indent=4)


write_order_to_json('iphone', '11', '46500', 'Nouname', '10.04.2022')

