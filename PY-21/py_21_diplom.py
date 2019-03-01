import requests
import time
from tqdm import tqdm
import os
import json
import sys


# Задание на дипломный проект «Шпионские игры»
# курса «Python: программирование на каждый день и сверхбыстрое прототипирование»
#
# Задание:
# Вывести список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.
#
# Входные данные:
# Имя пользователя или его id в ВК, для которого мы проводим исследование.
#
# Выходные данные:
# Файл groups.json
#
# Требования к программе:
# + Программа не падает, если один из друзей пользователя помечен как “удалён” или “заблокирован”.
# + Показывает что не зависла: рисует точку или чёрточку на каждое обращение к api.
# + Не падает, если было слишком много обращений к API (Too many requests per second).
# + Код программы удовлетворяет PEP8.
# + Не использовать внешние библиотеки (vk, vkapi).
#
# Дополнительные требования (не обязательны для получения диплома):
# - Использовать execute для ускорения работы.
# + Показывает прогресс: сколько осталось до конца работы.
# + Восстанавливается если случился ReadTimeout.
# + Показывать в том числе группы, в которых есть общие друзья, но не более, чем N человек, где N задается в коде.


class ScriptError(Exception):
    pass


class User:
    def __init__(self):
        self.short_name = ''
        self.id = 0
        self.friends = []
        self.communities = set()
        self.friends_communities = set()
        self.unique_groups = []
        self.max_friends_in_community = 0
        self.friends_communities_with_max = set()
        self.v = '5.92'
        self.token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

    def input_user(self):
        while not self.id:
            try:
                name = input('Введите имя пользователя или его id в ВК: ')
                if not str(name).isdigit():
                    response = self.call_api('utils.resolveScreenName', {'screen_name': name})
                    if response['type'] == 'user':
                        self.id = response['object_id']
                else:
                    self.id = name
            except Exception:
                print('Введены некорректные данные')

    def get_friends(self):
        try:
            self.friends = self.call_api('friends.get', {'user_id': self.id})['items']
        except Exception:
            pass

    def get_communities(self, id_users):
        self.friends_communities_with_max = set()
        if not isinstance(id_users, list):
            id_users = [id_users]
        communities = []
        communities_dict = dict()
        errors = 0
        tqdm.write(f'\nПолучаем список групп', file=sys.stdout)
        for user in tqdm(iterable=id_users, unit='pcs', file=sys.stdout):
            try:
                response = self.call_api('groups.get', {'user_id': user})
                communities.extend(response['items'])

                for id_community in response['items']:

                    if id_community in communities_dict.keys():
                        communities_dict[id_community] += 1
                    else:
                        communities_dict.setdefault(id_community, 1)
            except Exception:
                errors += 1
        if errors:
            tqdm.write(f'Количество ошибок при запросах: {errors}', file=sys.stdout)
        tqdm.write(f'Выполнено успешно. Кол-во групп: {len(set(communities))}', file=sys.stdout)
        for key, value in communities_dict.items():
            if value <= self.max_friends_in_community:
                self.friends_communities_with_max.add(key)
        return set(communities)

    def find_similar_communities(self):
        print('Получаем общие id групп')
        self.unique_groups = (self.communities - self.friends_communities) | \
                             (self.communities & self.friends_communities_with_max)
        print(self.communities & self.friends_communities_with_max)

    def communties_info(self, communities):
        communities_str = ','.join(map(str, communities))
        communities_info = self.call_api('groups.getById', {'fields': 'members_count', 'group_ids': communities_str})
        target_communities_info = list()
        new_community = dict()
        print('Обрабатываем необходимые данные о группах')
        for group in tqdm(communities_info, unit='pcs', file=sys.stdout):
            try:
                new_community['name'] = group['name']
                new_community['gid'] = group['id']
                new_community['members_count'] = group['members_count']
                target_communities_info.append({'name': group['name'], 'gid': group['id'],
                                                'members_count': group['members_count']})
                time.sleep(0.4)
            except Exception:
                pass
        print()
        if self.unique_groups:
            print(f'Количество групп в ВК в которых состоит пользователь(https://vk.com/id{self.id}), '
                  f'но не более {self.max_friends_in_community} его друзей: {len(target_communities_info)}')
            with open(f'unique_groups_id{self.id}.json', 'w') as file:
                try:
                    json.dump(target_communities_info, file, indent=4, ensure_ascii=False)
                except UnicodeEncodeError:
                    pass
                print(f'Данные сохранены в файл:\n{os.getcwd()}\\unique_groups_id{self.id}.json')
        else:
            print('У пользователя нет уникальных сообществ')

    def get_target_communities_info(self):
        self.input_user()
        self.get_friends()
        self.communities = self.get_communities(self.id)
        self.friends_communities = self.get_communities(self.friends)
        self.find_similar_communities()
        self.communties_info(self.unique_groups)

    def call_api(self, method, other_params):
        time.sleep(0.4)
        url = 'https://api.vk.com/method/'
        method = method
        params = {'v': self.v, 'access_token': self.token}
        params.update(other_params)
        try:
            response = requests.get(url + method, params, timeout=20)
            response = response.json()['response']
        except Exception:
            pass
            # with open(f'errors_log.txt', 'a') as file_err:
            #     tqdm.write(f"{time.asctime()} {req}\n", file=file_err)
        return response


if __name__ == '__main__':
    my_user = User()
    my_user.max_friends_in_community = 15
    my_user.get_target_communities_info()
