# -*- coding: utf-8 -*-
# Домашнее задание к лекции 2.3 «Database. PostgreSQL»
# Напишите следующие функции для работы с таблицами:
# def create_db(): # создает таблицы
#     pass
#
# def get_students(course_id): # возвращает студентов определенного курса
#     pass
#
# def add_students(course_id, students): # создает студентов и
#                                        # записывает их на курс
#     pass
#
#
# def add_student(student): # просто создает студента
#     pass
#
# def get_student(student_id):
#     pass
# Объекты "Студент" передаются в функцию в виде словаря.
# Вызов функции add_students должен выполнять создание всех сущностей в транзакции.
#
# Схемы:
#
# Student:
#  id     | integer                  | not null
#  name   | character varying(100)   | not null
#  gpa    | numeric(10,2)            |
#  birth  | timestamp with time zone |
#
# Course:
#  id     | integer                  | not null
#  name   | character varying(100)   | not null

import psycopg2 as pg

DB_NAME = 'student_db'
USER = 'test'
PASSWORD = 'test'



def create_db(): # создает таблицы
    with pg.connect(dbname=DB_NAME, user=USER, password=PASSWORD) as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS student (
            id serial PRIMARY KEY,
            name varchar(100) NOT NULL ,
            gpa numeric(10, 2),
            birth timestamp with time zone );""")

            cur.execute("""CREATE TABLE IF NOT EXISTS course (
            id serial PRIMARY KEY,
            name varchar(100) NOT NULL );""")

            cur.execute("""CREATE TABLE IF NOT EXISTS student_courses (
            id serial PRIMARY KEY,
            student_id integer REFERENCES student(id)  ON DELETE CASCADE,
            course_id integer REFERENCES course(id)  ON DELETE CASCADE);""")


def add_student(student):  # просто создает студента
    with pg.connect(dbname=DB_NAME, user=USER, password=PASSWORD) as conn:
        with conn.cursor() as cur:
            cur.execute("""insert into student (name, gpa, birth) values (%s, %s, %s) RETURNING id;""",
                        (student['name'], student['gpa'], student['birth']))
            return cur.fetchone()


def get_student(student_id):  # возвращает студента по id
    with pg.connect(dbname=DB_NAME, user=USER, password=PASSWORD) as conn:
        with conn.cursor() as cur:
            cur.execute("""select * from student where student.id = (%s)""", str(student_id))
            return cur.fetchone()


def add_students(course_id, students):  # создает студентов и записывает их на курс
    with pg.connect(dbname=DB_NAME, user=USER, password=PASSWORD) as conn:
        with conn.cursor() as cur:

            cur.execute("""select * from course where course.id = (%s)""", (str(course_id),))
            if cur.fetchone() is None:
                message = f'Курс с  id {course_id} не найден'
                return message

            for student in students:
                id_last_student = add_student(student)
                cur.execute("""insert into student_courses (student_id, course_id) values (%s, %s)""",
                            (id_last_student, course_id))


def get_students(course_id):  # возвращает студентов определенного курса
    with pg.connect(dbname=DB_NAME, user=USER, password=PASSWORD) as conn:
        with conn.cursor() as cur:
            cur.execute("""      
            select student.name, course.name from student
            join student_courses on student_courses.student_id = student.id
            join course on course.id = (%s)""", (str(course_id),))
            return cur.fetchall()


if __name__ == "__main__":
    create_db()

    add_student({'name': 'Nikita', 'gpa': 5, 'birth': '1967-06-03'})
    add_students(1, [{'name': 'Evgen', 'gpa': 7, 'birth': '1995-03-07'}])
    print(get_student(1))
    print(get_students(1))
