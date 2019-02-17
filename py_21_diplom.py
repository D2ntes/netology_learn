import requests
import time
from pprint import pprint
from tqdm import tqdm
import os
import json
import sys


# Задание на дипломный проект «Шпионские игры»
# курса «Python: программирование на каждый день и сверхбыстрое прототипирование»
# Есть вещи, которые объединяют людей, а есть те, которые делают нас индивидуальными.
# Давайте посмотрим, чем пользователи в ВК не делятся со своими друзьями?
#
# Задание:
# Вывести список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.

class ScriptError(Exception):
    pass


class User:
    def __init__(self):
        self.short_name = ''
        self.id = -1
        self.friends = []
        self.communities = set()
        self.friends_communities = set()
        self.unique_groups = []
        self.v = '5.92'
        self.token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

    def input_user(self):
        name = input('Введите имя пользователя или его id в ВК: ')
        if not str(name).isdigit():
            response = self.call_api('utils.resolveScreenName', {'screen_name': name})
            if response['type'] == 'user':
                self.id = response['object_id']
        else:
            self.id = name

    def get_friends(self):
        self.friends = self.call_api('friends.get', {'user_id': self.id})['items']

    def get_communities(self, id_users):
        if not isinstance(id_users, list):
            id_users = [id_users]
        communities = []
        errors = 0
        tqdm.write('Получаем список групп', file=sys.stdout)
        for user in tqdm(iterable=id_users, unit='pcs', file=sys.stdout):
            try:
                response = self.call_api('groups.get', {'user_id': user})
                communities.extend(response['items'])
            except Exception:
                errors += 1
                # with open(f'errors_log.txt', 'a') as f:
                #     tqdm.write(f"{time.asctime()} {req}\n", file=f)
        if errors:
            tqdm.write(f'Количество ошибок при запросах: {errors}', file=sys.stdout)
        tqdm.write(f'Выполнено успешно. Кол-во групп: {len(set(communities))}\n', file=sys.stdout)
        return set(communities)

    def find_similar_communities(self):
        print('Получаем общие id групп')
        self.unique_groups = self.communities - self.friends_communities
        print(f'Кол-во общих групп: {len(self.unique_groups)}\n')

    def communties_info(self, communities):
        communities_str = ','.join(map(str, communities))
        communities_info = self.call_api('groups.getById', {'fields': 'members_count', 'group_ids': communities_str})
        target_communities_info = list()
        new_community = dict()

        print('Обрабатываем необходимые данные о группах')
        for group in tqdm(communities_info, unit='pcs', file=sys.stdout):
            new_community['name'] = group['name']
            new_community['gid'] = group['id']
            new_community['members_count'] = group['members_count']
            target_communities_info.append({'name': group['name'], 'gid': group['id'],
                                            'members_count': group['members_count']})
            time.sleep(0.5)
        print()
        if self.unique_groups:
            print(f'Количество групп в ВК в которых состоит пользователь(https://vk.com/id{self.id}), '
                  f'но не состоит никто из его друзей: {len(target_communities_info)}')
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
        return response


my_user = User()
my_user.get_target_communities_info()
