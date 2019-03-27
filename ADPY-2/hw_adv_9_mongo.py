# -*- coding: utf-8 -*-
# Домашнее задание к лекции 2.4 «Database. Mongo. ORM»
# Вы реализуете приложение для поиска билетов на концерт.
# Заполните коллекцию в Монго данными о предстоящих концертах и реализуйте следующие функции:
# read_data: импорт данных из csv файла
# find_cheapest: отсортировать билеты из базы по возрастания цены
# find_by_name: найти билеты по исполнителю, где имя исполнителя может быть задано не полностью.

# Дополнительное задание
# Реализовать сортировку по дате мероприятия. Д
# ля этого вам потребуется строку с датой в csv-файле приводить к объекту datetime (можете считать,
# что все они текущего года) и сохранять его.
# Пример поиска: найти все мероприятия с 1 по 30 июля.

import csv
import re
from datetime import datetime

import pymongo
from pymongo import MongoClient

client = MongoClient()
songs_db = client['song']
song_collection = songs_db['song']


def read_data(csv_file, db):
    """
    Загрузить данные в бд из CSV-файла
    """
    with open(csv_file, encoding='utf8') as csvfile:
        songs = list()
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = dict(row)
            row['Цена'] = int(row['Цена'])
            row['Дата'] += f'.{datetime.now().year}'
            row['Дата'] = datetime.strptime(row['Дата'], '%d.%m.%Y')
            songs.append(row)

        db.songs.insert_many(songs)
        print()


def find_cheapest(db):
    """
    Найти самые дешевые билеты
    Документация: https://docs.mongodb.com/manual/reference/operator/aggregation/sort/
    """
    print('\nСамые дешёвые билеты:')
    for event in list(db.songs.find().sort([('Цена', pymongo.ASCENDING)])):
        print(event['Исполнитель'], event['Дата'], event['Цена'])


def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке),
    и выведите их по возрастанию цены
    """

    regex = re.compile(rf'\w*{re.escape(name)}\w*')
    print(f'\nНадены следующие исполнители по запросу: "{name}"')
    for event in list(db.songs.find({'Исполнитель': regex}).sort([('Цена', pymongo.ASCENDING)])):
        print(f"{event['Исполнитель']} {event['Место']} "
              f"{event['Дата']} {event['Цена']}")


def sort_by_date(start_time, end_time, db):
    start_time_f = datetime.strptime(start_time, '%d.%m.%Y')
    end_time_f = datetime.strptime(end_time, '%d.%m.%Y')
    sorted_by_date_list = list(db.songs.find({'Дата': {'$gt': start_time_f, '$lt': end_time_f}}))
    print(f'\nНайдено мероприятий в период с {start_time} по {end_time}: {len(sorted_by_date_list)}')
    for event in sorted_by_date_list:
        print(f"{event['Исполнитель']} {event['Место']} "
              f"{event['Дата']} {event['Цена']}")


def run():
    read_data('artists.csv', songs_db)

    find_cheapest(songs_db)

    start_time = f'01.07.{datetime.now().year}'
    end_time = f'30.07.{datetime.now().year}'
    sort_by_date(start_time, end_time, songs_db)

    find_by_name('Se', songs_db)


if __name__ == '__main__':
    run()
