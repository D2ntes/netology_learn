# -*- coding: utf-8 -*-
# Домашнее задание к лекции 2.2 «Regular expressions»
# Иногда при знакомстве мы записываем контакты в адресную книгу кое-как с мыслью,
# что "когда-нибудь потом все обязательно поправим". Копируем данные из интернета или из смски.
# Добавляем людей в разных мессенджерах. В результате получается адресная книга,
# в которой совершенно невозможно кого-то нормально найти: мешает множество дублей и разная запись одних и тех же имен.
#
# Кейс основан на реальных данных из https://www.nalog.ru/opendata/, https://www.minfin.ru/ru/opendata/
#
# Ваша задача: починить адресную книгу, используя регулярные выражения.
# Структура данных будет всегда:
# lastname,firstname,surname,organization,position,phone,email
# Предполагается, что телефон и e-mail у человека может быть только один.
# Необходимо:
#
# -  поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
#   В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О;
# -  привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой:
# +7(999)999-99-99 доб.9999;
# -  объединить все дублирующиеся записи о человеке в одну.


import csv
import re
from pprint import PrettyPrinter


def open_csv(filename="phonebook_raw.csv"):
    with open(filename, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


class PhoneBook:
    def __init__(self, phonebook):
        self.phonebook = phonebook
        self.fieldnames = phonebook[0]
        self.patterns = {'phone_pattern': [
            r'(\s*)(\+7|8)(\s*)(\(*)(\d{3})(\)*)(\s*|\-*)(\d{3})(\s*)(\-*)(\d{2})(\s*)(\-*)(\d{2})((\s*)(\(*)(доб\.)(\s*)(\d{4})(\)*))*',
            r',+7(\5)\8-\11-\14\16\18\20'
        ],
            'name_job_pattern': [
                r'^([А-ЯЁ]{1}[а-яё]*)(\s*)([А-ЯЁ]{1}[а-яё]*)(\s*)([А-ЯЁ]{1}[а-яё]*[(вич)(вна)])?(\s*)([А-ЯЁ]{1}\w+)?',
                r'\1,\3,\5,\7,'
            ],
            'email_pattern': [
                r'(\s*)([a-zA-Z1-9\-\._]+@[a-z1-9]+(.[a-z1-9]+){1,})$', r',\2'
            ],
        }

    def __str__(self):
        pp = PrettyPrinter()
        return pp.pformat(self.phonebook)

    def normalize(self):
        normalize_phonebook = []
        for contact in self.phonebook:
            contact = ' '.join(contact)

            mail_normalize = re.sub(self.patterns['email_pattern'][0],
                                    self.patterns['email_pattern'][1],
                                    str(contact))

            name_job_normalize = re.sub(self.patterns['name_job_pattern'][0],
                                        self.patterns['name_job_pattern'][1],
                                        str(mail_normalize))

            phone_normalize = re.sub(self.patterns['phone_pattern'][0],
                                     self.patterns['phone_pattern'][1],
                                     str(name_job_normalize))

            contact_normalize = dict(zip(self.fieldnames, phone_normalize.strip().split(',')))

            for contact_in_phonebook in normalize_phonebook:
                if tuple(contact_normalize.values())[:2] == tuple(contact_in_phonebook.values())[:2]:
                    for key in contact_normalize:
                        if contact_normalize[key] not in contact_in_phonebook[key]:
                            contact_in_phonebook[key] += contact_normalize[key]
                    contact_normalize = {}

            if contact_normalize:
                normalize_phonebook.append(contact_normalize)

        self.phonebook = normalize_phonebook

    def save_book(self, filename="phonebook.csv"):
        with open(filename, "w", newline='') as out_file:
            writer = csv.DictWriter(out_file, delimiter=',', fieldnames=self.fieldnames)
            writer.writeheader()
            for row in self.phonebook[1:]:
                writer.writerow(row)


def run():
    my_phonebook = PhoneBook(open_csv())
    my_phonebook.normalize()
    my_phonebook.save_book()


if __name__ == '__main__':
    run()
