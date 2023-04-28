# -*- coding: utf8 -*-
import csv
import os
import re


def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []

    for i in range(0, len([file for file in os.listdir() if file.endswith('.txt')])):
        files = open(f'info_{i}.txt', encoding='cp1251')
        data = files.read()

        def get_find(name):
            return name.findall(data)[0].split()[2]

        system_manufacturer = re.compile(r'Изготовитель системы:\s*\S*')
        os_prod_list.append(get_find(system_manufacturer))

        os_name = re.compile(r'Название ОС:\s*\S*')
        os_name_list.append(get_find(os_name))

        product_code = re.compile(r'Код продукта:\s*\S*')
        os_code_list.append(get_find(product_code))

        system_type = re.compile(r'Тип системы:\s*\S*')
        os_type_list.append(get_find(system_type))

    main_data.extend(['Изготовитель системы', 'Название OC', 'Код продукта', 'Тип системы'])

    for i in range(0, len([file for file in os.listdir() if file.endswith('.txt')])):
        values_data = []
        values_data.append(os_prod_list[i])
        values_data.append(os_name_list[i])
        values_data.append(os_code_list[i])
        values_data.append(os_type_list[i])
        main_data.append(values_data)
    print(main_data)
    return main_data


def write_to_csv(source_file):

    data = get_data()
    with open(source_file, 'w', encoding='utf-8', newline='') as file:
        file_writer = csv.writer(file)
        for row in data:
            file_writer.writerow([row])


write_to_csv('data.csv')




