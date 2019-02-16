import requests
import time
from pprint import pprint
from tqdm import tqdm
import os
import json
import sys

v = '5.92'
TOKEN = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'


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

    def input_user(self):
        name = input('Введите имя пользователя или его id в ВК: ')
        if not str(name).isdigit():
            params = {
                'v': v,
                'access_token': TOKEN,
                'screen_name': name
            }
            response = requests.get('https://api.vk.com/method/utils.resolveScreenName', params=params).json()[
                'response']
            if response['type'] == 'user':
                self.id = response['object_id']
        else:
            self.id = name

    def get_friends(self):
        self.friends = requests.get('https://api.vk.com/method/friends.get', params={
            'v': v,
            'user_id': self.id,
            'access_token': TOKEN
        }).json()['response']['items']

    def get_communities(self, id_users):

        if not isinstance(id_users, list):
            id_users = [id_users]
        communities = []
        errors = 0

        tqdm.write('Получаем список групп', file=sys.stdout)
        for user in tqdm(iterable=id_users, unit='pcs', file=sys.stdout):
            try:
                req = requests.get('https://api.vk.com/method/groups.get', params={
                    'v': v,
                    'user_id': user,
                    'access_token': TOKEN
                }).json()
                communities.extend(req['response']['items'])

                time.sleep(0.5)

            except Exception:
                errors += 1
                with open(f'errors_log.txt', 'a') as f:
                    tqdm.write(f"{time.asctime()} {req}\n", file=f)

        tqdm.write(f'Выполнено успешно. Кол-во групп: {len(set(communities))}', file=sys.stdout)
        if errors:
            tqdm.write(f'Данные от {errors} пользователей не получены.\n', file=sys.stdout)


        return set(communities)


    def find_similar_communities(self):
        print('Получаем общие id групп')
        self.unique_groups = self.communities - self.friends_communities
        print(f'Кол-во общих групп: {len(self.unique_groups)}')

    def communties_info(self, communities):

        communities_str = ','.join(map(str, communities))

        response = requests.get('https://api.vk.com/method/groups.getById', params={
            'group_ids': communities_str,
            'v': v,
            'access_token': TOKEN,
            'fields': 'members_count'
        })

        communities_info = response.json()['response']
        target_communities_info = list()
        new_community = dict()

        print('Обрабатываем необходимые данные о группах')
        for group in tqdm(communities_info, unit='pcs', file=sys.stdout):
            new_community['name'] = group['name']
            new_community['gid'] = group['id']
            new_community['members_count'] = group['members_count']
            target_communities_info.append({'name': group['name'], 'gid': group['id'],
                                            'members_count': group['members_count']})

        print('Выполнено')

        if self.unique_groups:
            with open(f'unique_groups_id{self.id}.json', 'w') as file:
                json.dump(target_communities_info, file, indent=4, ensure_ascii=False)
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


my_user = User()
my_user.get_target_communities_info()