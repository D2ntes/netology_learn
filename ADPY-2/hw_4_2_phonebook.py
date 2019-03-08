# -*- coding: utf-8 -*-

# Домашнее задание к лекции 1.4 «Function 2.0 *args, **kwargs»
# 2. Создать приложение телефонная книга. класс Contact имеет следующие поля:
# Имя, фамилия, телефонный номер - обязательные поля;
# избранный контакт - необязательное поле. По умолчанию False;
# Дополнительная информация - необходимо использовать *args, **kwargs.
# Переопределить "магический" метод str для красивого вывода контакта. Вывод контакта должен быть следующим
#
#     jhon = Contact('Jhon', 'Smith', '+71234567809', telegram='@jhony', email='jhony@smith.com')
#     print(jhon)
# Вывод
#
# Имя: Jhon
# Фамилия: Smith
# Телефон: +71234567809
# В избранных: нет
# Дополнительная информация:
# 	 telegram : @jhony
# 	 email : jhony@smith.com

# 3. класс PhoneBook:
# Название телефоной книги - обязательное поле.
# Методы:
# Вывод контактов из телефонной книги;
# Добавление нового контакта;
# Удаление контакта по номеру телефона;
# Добавить два метода для поиска контактов в телефонной книге
# Поиск всех избранных номеров
# Поиск контакта по имени и фамилии


class Contact:
    def __init__(self, name, surname, number, chosen=False, **kwargs):
        self.name = name
        self.surname = surname
        self.number = number
        self.other = kwargs
        self.other_print = '    нет'
        self.chosen = chosen

    def __str__(self):
        if self.other:
            self.other_print = ''
            for key, value in self.other.items():
                self.other_print += f'    {key} : {value}\n'

        return f'Имя: {self.name}\nФамилия: {self.surname}\n' \
            f'Телефон: {self.number}\nДополнительная информация:\n{self.other_print}'


class NumBook(object):

    def __init__(self, namebook):
        self.namebook = namebook
        self.abonents = []

    def __str__(self):
        print(f'\n---Телефонная книга "{self.namebook}"---')
        str_book = ''
        for num, abonent in enumerate(self.abonents, 1):
            str_book += f"{num}.\n{str(abonent)}"
        return str_book

    def add_abonent(self, abonent):
        self.abonents.append(abonent)

    def del_abonent(self, number):
        del_list = []
        for abonent in self.abonents:
            if abonent.number == number:
                del_list.append(abonent)
        print("\n---Удаленные абоненты---\n", ', '.join(list(map(lambda x: f'{x.name} {x.surname}', del_list))))
        list(map(lambda x: self.abonents.remove(x), del_list))

    def find_num_abonent(self, number):
        find_list = []
        for abonent in self.abonents:
            if abonent.number == number:
                find_list.append(abonent)
        if not find_list:
            find_list.append("не дал результатов")
        print(f"\n--Поиск по номеру {number}---\n" + '\n'.join(list(map(lambda x: f'{str(x)}', find_list))))

    def find_chosen_abonent(self):
        find_list = []
        for abonent in self.abonents:
            if abonent.chosen == True:
                find_list.append(abonent)
        if not find_list:
            find_list.append("Поиск не дал результатов")
        print("\n---Избранные абоненты---\n" + '\n'.join(list(map(lambda x: f'{str(x)}', find_list))))

    def find_abonent_by_name(self, name, surname):
        find_list = []
        for abonent in self.abonents:
            if abonent.name == name and abonent.surname == surname:
                find_list.append(abonent)
        if not find_list:
            find_list.append("не дал результатов")
        print(f"\n---Поиск по имени {name} {surname}---\n" + '\n'.join(list(map(lambda x: f'{str(x)}', find_list))))


if __name__ == '__main__':
    # Создание телефонной книги
    num_book = NumBook(input('Введите название телефонной книги: '))

    # Создание контакта и добавление в книгу
    num_book.add_abonent(Contact('Jhon', 'Smith', '+71234567809', telegram='@jhony', email='jhony@smith.com'))
    num_book.add_abonent(Contact('Ivan', 'Smith', '+71346453645', vkontakte='id23423', email='ivsm@smith.com'))
    num_book.add_abonent(Contact('Smith', 'XXX', '+77777777777', telegram='@xxx', chosen=True))
    num_book.add_abonent(Contact('Maria', 'Smith', '+71234567809', telegram='@jhony', email='jhony@smith.com'))
    num_book.add_abonent(Contact('Elon', 'Musk', '+66666666666', twitter='elonmusk', chosen=True))
    num_book.add_abonent(Contact('Jhon', 'Jhonov', '+71346453645'))

    # Вывод телефонной книги
    print(num_book)

    # Удаление контакта по номеру телефона
    num_book.del_abonent('+71234567809')

    # Поиск всех избранных номеров
    num_book.find_chosen_abonent()

    # Поиск контакта по имени и фамилии
    num_book.find_abonent_by_name('Elon', 'Musk')

    # Поиск контакта по номеру телефона
    num_book.find_num_abonent('+71346453645')
    num_book.find_num_abonent('+71234567809')

    # Вывод телефонной книги
    print(num_book)
