# -*- coding: utf-8 -*-

# Домашнее задание к лекции 1.2 «Iterators. Generators. Yield»
# Написать генератор, который принимает путь к файлу. При каждой итерации возвращает md5 хеш каждой строки файла.

import hashlib


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
    for number, hash_line in enumerate(hash_lines(input('Введите путь к файлу: ')), 1):
        print(f'{number}: {hash_line}')
