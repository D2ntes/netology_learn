# Домашнее задание к лекции 3.2 «Работа с библиотекой requests, http-запросы»
# Исходный код для выполнения домашней работы вы найдете на GitHub.
#
# Задача
# Необходимо расширить функцию переводчика так, чтобы она принимала следующие параметры:
#
# путь к файлу с текстом;
# путь к файлу с результатом;
# язык с которого перевести;
# язык на который перевести (по-умолчанию русский).
# У вас есть 3 файла (DE.txt, ES.txt, FR.txt) с новостями на 3 языках: французском, испанском, немецком. Функция должна
# взять каждый файл с текстом, перевести его на русский и сохранить результат в новом файле.
#
# Для переводов можно пользоваться API Yandex.Переводчик.
import requests
import os


def input_dir(input_text):
    path_file = False
    while not path_file:
        dir_input = input(input_text)
        if len(dir_input) == 0:
            dir_input = os.path.dirname(os.path.abspath(__file__))
        path_file = os.path.exists(dir_input)
        if not path_file:
            print('Такого пути не существует.')
    return dir_input


def input_lang(input_text):
    lang_dict = {0: 'ru', 1: 'de', 2: 'fr', 3: 'es'}
    lang = lang_dict[0]

    while True:
        try:
            lang_input = input(input_text)
            if len(lang_input) == 0:
                lang = lang_dict[0]
            else:
                lang = lang_dict[int(lang_input)]
        except KeyError:
            print("Языка под таким номером нет. Повторите попытку.")
        except ValueError:
            print("Введите номер. Повторите попытку.")
        else:
            break
    return lang


def load_text(dir_name, file_name):
    file = os.path.join(dir_name, file_name)
    if os.path.exists(file):
        with open(file, encoding='utf-8') as f:
            text = f.read()
    else:
        text = f'Файл {file} не найден'
        print(text)
    return text


def save_text(text, dir_name, file_name):
    file = os.path.join(dir_name, file_name)
    with open(file, "w", encoding='utf-8') as f:
        f.write(text)
    print(f'Результат перевода сохранен в файле:{file}')


API_KEY = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def translate_it(text, inlang, outlang):
    """
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param to_lang:
    :return:
    """

    params = {
        'key': API_KEY,
        'text': text,
        'lang': f'{in_lang}-{out_lang}',
    }

    response = requests.get(URL, params=params)
    json_ = response.json()
    return ''.join(json_['text'])


in_dir = input_dir('Введите путь к файлу с текстом(<Enter>, если файл в рабочей директории):')
out_dir = input_dir('Введите путь к файлу с результатом(<Enter>, если файл в рабочей директории):')
in_lang = input_lang('Язык, с которого необходимо перевести.\n<0> - ru(по умолчанию), <1> - de, <2> - fr, <3> - es : ')
out_lang = input_lang('Язык, на который необходимо перевести.\n<0> - ru(по умолчанию), <1> - de, <2> - fr, <3> - es : ')
save_text(translate_it(load_text(in_dir, in_lang + '.txt'), in_lang, out_lang), out_dir,
          in_lang + '-' + out_lang + '.txt')
