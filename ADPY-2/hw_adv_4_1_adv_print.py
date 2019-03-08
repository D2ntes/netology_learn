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


def print_to_file(string, in_file):
    with open(in_file, 'w') as file:
        file.write(string)


def adv_print(*args, **kwargs):
    sep = kwargs.get('sep', ' ')
    start = kwargs.get('start', '')
    end = kwargs.get('end', '\n')
    max_line = kwargs.get('max_line', 0)
    in_file = kwargs.get('in_file', '')
    file = kwargs.get('file', '')
    string = sep.join([str(arg) for arg in args]) + end

    if max_line:
        string = split_max_line(string, max_line)
    if file:
        print(start, string, sep='\n', file=file)
    else:
        print(start, string, sep='\n')
    if in_file:
        print_to_file(string, in_file)


if __name__ == '__main__':
    a = 234233333333334444444444444444444333333333333333333333333333333333333333333333333333333333333333333333333333333
    b = ['asd\n', '23423,', 'sdfsd']
    c = {'g': 'sdfsdfsd', 'k': '34534'}

    adv_print(a, *b, c, max_line=60, sep='', start='sdf', end='!!!!', in_file=True)

