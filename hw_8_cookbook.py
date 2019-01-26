# файла, запись в файл»
# Необходимо написать программу для кулинарной книги.
#
# Список рецептов должен храниться в отдельном файле в следующем формате:
#
# Название блюда
# Kоличество ингредиентов в блюде
# Название ингредиента | Количество | Единица измерения
# Название ингредиента | Количество | Единица измерения
# ...

# В одном файле может быть произвольное количество блюд.
# Читать список рецептов из этого файла.
# Соблюдайте кодстайл, разбивайте новую логику на функции и не используйте глобальных переменных.

# Задача №1
# Должен получится следующий словарь
#
# cook_book = {
#   'Омлет': [
#     {'ingridient_name': 'Яйцо', 'quantity': 2, 'measure': 'шт.'},
#     {'ingridient_name': 'Молоко', 'quantity': 100, 'measure': 'мл'},
#     {'ingridient_name': 'Помидор', 'quantity': 2, 'measure': 'шт'}
#     ],
#   'Утка по-пекински': [
#     {'ingridient_name': 'Утка', 'quantity': 1, 'measure': 'шт'},
#     {'ingridient_name': 'Вода', 'quantity': 2, 'measure': 'л'},
#     {'ingridient_name': 'Мед', 'quantity': 3, 'measure': 'ст.л'},
#     {'ingridient_name': 'Соевый соус', 'quantity': 60, 'measure': 'мл'}
#     ],
#   'Запеченный картофель': [
#     {'ingridient_name': 'Картофель', 'quantity': 1, 'measure': 'кг'},
#     {'ingridient_name': 'Помидор', 'quantity': 2, 'measure': 'шт'},
#     {'ingridient_name': 'Сыр гауда', 'quantity': 100, 'measure': 'г'},
#     ]
#   }

def load_book_from_file(book_file='cookbook.txt'):
    with open(book_file) as book:
        cook_dict = dict()
        key_ingridient_dict = ['ingridient_name', 'quantity', 'measure']
        book.seek(0, 2)
        eof = book.tell()
        book.seek(0, 0)
        while book.tell() != eof:
            ingridient_list = []
            key = book.readline().strip()
            for ingridient in range(int(book.readline().strip())):
                value_ingridient_dict = book.readline().strip().split(' | ')
                value_ingridient_dict[1] = int(value_ingridient_dict[1])
                ingridient_list.append(dict(zip(key_ingridient_dict, value_ingridient_dict)))
                # print(value_ingridient_dict)
            cook_dict.setdefault(key, ingridient_list)
            book.readline()
    return cook_dict


# Задача №2
# Нужно написать функцию, которая на вход принимает список блюд из cook_book и количество персон для кого мы будем готовить
#
# get_shop_list_by_dishes(dishes, person_count)
# На выходе мы должны получить словарь с названием ингредиентов и его количетсва для блюда. Например, для такого вызова
#
# get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2)
# Должен быть следующий результат:
#
# {
#   'Картофель': {'measure': 'кг', 'quantity': 2},
#   'Молоко': {'measure': 'мл', 'quantity': 200},
#   'Помидор': {'measure': 'шт', 'quantity': 8},
#   'Сыр гауда': {'measure': 'г', 'quantity': 200},
#   'Яйцо': {'measure': 'шт', 'quantity': 4},
#   'Чеснок': {'measure': 'зубч', 'quantity': 6}
# }
# Обратите внимание, что ингредиенты могут повторяться

def get_shop_list_by_dishes(*args):
    dishes = args[0][0]
    person_count = int(args[-1][-1])

    ingridients_diner_dict = {}

    for dish in dishes:
        for ingridient in cook_book[dish]:

            if ingridient['ingridient_name'] in ingridients_diner_dict:
                ingridients_diner_dict[ingridient['ingridient_name']]['quantity'] += ingridient[
                                                                                         'quantity'] * person_count

            ingridients_diner_dict.setdefault(ingridient['ingridient_name'],
                                              {'measure': ingridient['measure'],
                                               'quantity': ingridient['quantity'] * person_count})

    print(f"Для приготовления блюд: {', '.join(dishes)}\n"
          f"Количество персон: {person_count}\n"
          f"Потреюуется:"
          )
    for ingridient in ingridients_diner_dict:
        print(f"{ingridient} | {ingridients_diner_dict[ingridient]['quantity']} " 
        f"{ingridients_diner_dict[ingridient]['measure']}")


def choice_of_dishes(book):
    i = 0
    menu = dict()
    dishes = []
    print('Кулинарная книга\nСодержание:')
    for dish in book:
        i += 1
        menu.setdefault(str(i), dish)
        print(f'{i}. {dish}')

    try:
        number_dishes = list(input(f'Введите номера блюд(через пробелы от 1 до {i}): ').split())
        person = input("На сколько персон? ")

        for numer_dish in number_dishes:
            dishes.append(menu[numer_dish])

    except TypeError:
        print("!!!Cледует ввести номер блюд и кол-во персон цифрами!!!")
        get_shop_list_by_dishes(choice_of_dishes(cook_book))

    except KeyError:
        print("!!!Блюда под таким номером в книге нет!!!")
        get_shop_list_by_dishes(choice_of_dishes(cook_book))

    return (dishes, person)


cook_book = load_book_from_file('cookbook.txt')
get_shop_list_by_dishes(choice_of_dishes(cook_book))
