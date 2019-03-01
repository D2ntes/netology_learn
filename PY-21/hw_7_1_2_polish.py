# Задача №1
# Нужно реализовать Польскую нотацию для двух положительных чисел. Реализовать нужно будет следующие операции:
#
# Сложение
# Вычитание
# Умножение
# Деление
# Например, пользователь вводит: + 2 2 Ответ должен быть: 4

# Задача №2
# С помощью выражения assert проверять, что первая операция в списке доступных операций (+, -, *, /).
# С помощью конструкций try/expcept ловить ошибки и выводить предупреждения
# Типы ошибок:
# Деление на 0
# Деление строк
# Передано необходимое количество аргументов
# и тд.


def input_command():
    operation_dict = {'+': polish_sum, '-': polish_sub, '*': polish_mul, '/': polish_div}
    help()
    calc_list = input('Введите выражение:').split()
    assert calc_list[0] in operation_dict.keys(), 'Первый символ - одна из доступных операций: +, -, *, /'

    try:
        int(calc_list[1])
        int(calc_list[2])
        if int(calc_list[1]) < 0 or int(calc_list[2]) < 0:
            raise ValueError

    except ValueError:
        input_command()

    try:
        operation_dict.get(calc_list[0])(*calc_list[1:])
    except TypeError:
        input_command()


def polish_sum(x, y):
    print('Сумма равна {}'.format(int(x) + int(y)))


def polish_sub(x, y):
    print('Разность равна {}'.format(int(x) - int(y)))


def polish_mul(x, y):
    print('Произведение равно {}'.format(int(x) * int(y)))


def polish_div(x, y):
    try:
        print('Частное равно {}'.format(int(x) / int(y)))
    except ZeroDivisionError:
        print('Деление на ноль!')


def help():
    print('После оператора введите два неотрицацельных числа через пробел')


input_command()
