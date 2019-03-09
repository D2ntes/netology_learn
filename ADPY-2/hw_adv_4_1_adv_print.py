# Домашнее задание к лекции 1.4 «Function 2.0 *args, **kwargs»
# Разработать свою реализацию функции print - adv_print.
# Она ничем не должна отличаться от классической функции кроме трех новых необязательных аргументов:
# start - с чего начинается вывод. По умолчанию пустая строка;
# max_line - максимальная длин строки при выводе. Если строка превыщает max_line,
# то вывод автоматически переносится на новую строку;
# in_file - аргумент, определяющий будет ли записан вывод ещё и в файл.
import textwrap


def split_max_line(string, max_len):
    return textwrap.fill(string, width=max_len)


def print_to_file(string):
    with open('adv_print.txt', 'w', encoding='utf-8') as file:
        file.write(string)


def adv_print(*args, **kwargs):
    sep = kwargs.get('sep', ' ')
    start = kwargs.get('start', '')
    end = kwargs.get('end', '\n')
    max_line = kwargs.get('max_line', 0)
    in_file = kwargs.get('in_file', '')
    file = kwargs.get('file', '')
    string = start + sep.join([str(arg) for arg in args]) + end
    print(string)
    if max_line:
        string = split_max_line(string, max_line)
    if file:
        print(string, file=file)
    else:
        print(string)
    if in_file:
        print_to_file(f"{start}{string}")


if __name__ == '__main__':
    a = [i for i in range(120)]
    b = ['asjkgjkgd', ('tuple', 123456789), 'sdfgdfsd']
    c = {'Ключ1': 'Значение', 'Ключ2': 123456789}

    print(a, *b, c, sep='|Разделитель|', end='Конец вывода(print)')

    adv_print(a, *b, c, max_line=60, start='Начало вывода adv_print', sep='|Разделитель|',
              end='Конец вывода adv_print', in_file=True)
