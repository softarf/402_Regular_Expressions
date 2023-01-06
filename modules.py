# -*- coding: utf-8 -*-
#                       "Регулярные выражения".
#                   Класс к задаче №1. Исправить адресную книгу.
#
from typing import List, Any

import os
import csv
import re


class Employee:

    def __init__(self, all_fields) -> None:
        """Создаёт карточку заданного сотрудника."""
        self.lastname: str = all_fields[0]
        self.firstname: str = all_fields[1]
        self.surname: str = all_fields[2]
        self.organization: str = all_fields[3]
        self.position: str = all_fields[4]
        self.phone: str = all_fields[5]
        self.email: str = all_fields[6]

    def __str__(self) -> str:
        """Переводит карточку сотрудника в печатаемый вид."""
        out_string: str = "{0},{1},{2},{3},{4},{5},{6}".format(
            self.lastname,
            self.firstname,
            self.surname,
            self.organization,
            self.position,
            self.phone,
            self.email)
        return out_string

    def e_list(self) -> List[str]:
        """Конвертирует карточку сотрудника из объекта Employee в список."""
        out_list: List[str] = [
            self.lastname,
            self.firstname,
            self.surname,
            self.organization,
            self.position,
            self.phone,
            self.email]
        return out_list

    def read_raw_data(file_name: str) -> List[Any]:
        """Читает данные из заданного файла"""
        if not os.path.isfile(file_name):
            return [[f'Файл {file_name} не найден.']]
        with open(file_name, "r", newline="\n", encoding='utf-8') as csv_file:
            reader_obj = csv.reader(
                csv_file,
                delimiter=",",
                quotechar=" ",
                quoting=csv.QUOTE_NONE)
            contacts_list: List[List[str]] = list(reader_obj)
        if len(contacts_list) > 0:
            csv_data: List[Any] = []
            for item in contacts_list:
                csv_data.append(Employee(item))
            return csv_data
        return [[f'Файл {file_name} пустой.']]

    def _fix_full_name(self) -> None:
        """Распределяет ФИО сотрудника по трём полям: lastname, firstname и surname"""
        full_name: List[str] = self.e_list()[:3]
        i: int
        for i in range(len(full_name) - 1):
            list_item: List[str] = full_name[i].strip().split()
            full_name[i] = list_item[0]
            if len(list_item) > 1:
                full_name[i + 1] = " ".join(list_item[1:]) + " " + full_name[i + 1]
        full_name[-1] = full_name[-1].strip()
        self.lastname, self.firstname, self.surname = full_name[0], full_name[1], full_name[2]

    def _fix_phone_number(self) -> None:
        """Приводит номер телефона сотрудника к виду +7(999)999-99-99 доб.9999."""
        pattern: str = (r"(\+7|7|8)?\s*\(?(\d{3})\)?[\s|-]*(\d+)[\s|-]*(\d{2})[\s|-]*(\d{2})"
                       + r"((\s)*\(?(доб\.?)\s*(\d+)\)?)?")
        repl: str = r"+7(\2)\3-\4-\5\7\8\9"
        self.phone = re.sub(pattern=pattern, repl=repl, string=self.phone)

    def add_record(raw_list: List[Any]) -> List[Any]:
        """Группирует повторящиеся записи."""
        list_cor_record: List[str]
        list_raw_record: List[str]
        correct_list: List[Any] = [raw_list[0]]
        cor_id: int
        raw_id: int
        len_cont: int
        cor_lastname: str
        for cor_id in range(1, len(raw_list[:])):
            len_cont = len(raw_list)
            if cor_id < len_cont:
                cor_lastname = raw_list[cor_id].lastname
                for raw_id in range(len_cont - 1, 0, -1):
                    if cor_id < raw_id:
                        if raw_list[raw_id].lastname == cor_lastname:
                            if ((raw_list[raw_id].firstname == ""
                                    or raw_list[raw_id].firstname == raw_list[cor_id].firstname
                                    or raw_list[cor_id].firstname == "")
                                    and (raw_list[raw_id].surname == ""
                                    or raw_list[raw_id].surname == raw_list[cor_id].surname
                                    or raw_list[cor_id].surname == "")):
                                list_cor_record = raw_list[cor_id].e_list()
                                list_raw_record = raw_list[raw_id].e_list()
                                for i in range(1, len(list_cor_record)):
                                    if list_cor_record[i] == "" and list_raw_record[i] != "":
                                        list_cor_record[i] = list_raw_record[i]
                                correct_list.append(Employee(list_cor_record))
                                raw_list.pop(raw_id)
                                break
                    else:
                        correct_list.append(raw_list[cor_id])
                        break
            else:
                break
        return correct_list

    def transform_records(raw_contacts: List[Any]) -> List[Any]:
        """Приводит к единому виду все карточки сотрудников."""
        record: Employee
        for record in raw_contacts:
            record._fix_full_name()
        correct_contacts: List[Employee] = Employee.add_record(raw_contacts)
        for record in correct_contacts:
            if record.phone != "":
                record._fix_phone_number()
        return correct_contacts

    def write_data(employees_records: List[Any], save_file: str, used_dialect: str = 'ru_excel') -> str:
        """Сохраняет карточки сотрудников в указанном файле."""
        list_employees_records: List[List[str]] = []
        record: Employee
        for record in employees_records:
            list_employees_records.append(record.e_list())
        #                Задаёт два диалекта (на выбор):
        xls_coding: str = 'windows-1251'
        csv.register_dialect('ru_excel',
                             delimiter=";",
                             doublequote=False,
                             escapechar="\\",
                             quotechar="'",
                             lineterminator="\n",
                             quoting=csv.QUOTE_NONNUMERIC
                             )
        nml_coding = 'utf - 8'
        csv.register_dialect('nameless',
                             delimiter=","
                             )
        if used_dialect == 'ru_excel':
            coding: str = xls_coding
        else:
            used_dialect = 'nameless'
            coding = nml_coding
        with open(file=save_file, mode="w", newline="\n", encoding=coding) as csv_file:
            data_writer = csv.writer(csv_file, dialect=used_dialect)
            data_writer.writerows(list_employees_records)
        return 'OK'
