# -*- coding: utf-8 -*-
#                       "Регулярные выражения".
#                   Задача №1. Исправить адресную книгу.
#
from typing import List, Any

from modules import Employee


def main():
    """Исправляет адресную книгу."""
    raw_file: str = 'phonebook_raw.csv'
    contacts_list: List[Any] = Employee.read_raw_data(raw_file)
    if type(contacts_list[0]) is list and contacts_list[0][0].endswith(' не найден.'):
        res: str = f"Задан отсутствующий файл: '{raw_file}'"
    elif type(contacts_list[0]) is list and contacts_list[0][0].endswith(' пустой.'):
        res = f"Задан пустой файл: '{raw_file}'"
    else:
        fix_contacts: List[Any] = Employee.transform_records(contacts_list)
        fix_file: str = 'phonebook_fix.csv'
        dialect: str = 'ru____excel'    # Исправить на 'ru_excel', (для разнообразия).
        res = Employee.write_data(fix_contacts, fix_file, dialect)
    print(res)


if __name__ == '__main__':
    main()
    # input('\n  -- Конец --  ')  # Типа  "Пауза" - Для среды
    # print('\n  -- Конец --  ')  # - Для блокнота
