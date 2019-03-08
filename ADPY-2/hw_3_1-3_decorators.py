# -*- coding: utf-8 -*

# Домашнее задание к лекции 1.3 «Decorators»
# Написать декоратор - логгер. Он записывает в файл дату и время вызова функции, имя функции,
# аргументы, с которыми вызвалась и возвращаемое значение.
# Написать декоратора из п.1 но с параметром – пути к логам.
# Применить написанный логгер к приложению из любого предыдущего д/з.

# Взята функция из задания к лекции 1.2 «Iterators. Generators. Yield»

import datetime
import hashlib
import logging
import os

def parametrized(path_log):

    def with_logging(func):

        def wrap_log(*args, **kwargs):
            nonlocal path_log
            try:
                os.mkdir(path_log)
            except OSError:
                pass
            name = func.__name__
            logging.basicConfig(filename=os.path.join(path_log, f'log.txt'), level=logging.INFO)
            result = func(*args, **kwargs)
            logging.info(f'{datetime.datetime.now().replace(microsecond=0)} Вызов функции: {name}, Результат: {result}\n')
            return func(*args, **kwargs)

        return wrap_log

    return with_logging


@parametrized(input('Введите путь для лог-файла(по умолчанию текущая папка):'))
def hash_lines(filename):
    try:
        with open(filename, 'rb') as datafile:
            m = hashlib.md5()
            line = datafile.readline()
            while line:
                m.update(line)
                line = datafile.readline()
                yield m.hexdigest()
    except FileNotFoundError as text_error:
        print(text_error)


if __name__ == '__main__':
    for number, hash_line in enumerate(hash_lines(input('Введите путь к файлу для хеширования: ')), 1):
        print(f'{number}: {hash_line}')
