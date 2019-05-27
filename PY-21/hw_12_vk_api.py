import requests


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.token = ''

    def __str__(self):
        id_prefix = 'https://vk.com/id'
        return (f'{id_prefix}{self.user_id}')

    def set_token(self, token):
        self.token = token

    def __and__(self, other):
        url_get_mutual = 'https://api.vk.com/method/friends.getMutual'

        mutual_friends_list = []

        params = {
            'access_token': self.token,
            'v': '5.92',
            'source_uid': self.user_id,
            'target_uid': other.user_id
        }

        response = requests.get(url_get_mutual, params)
        # print(response.json())

        if str(response.status_code) == '200':
            for friend in response.json()['response']:
                # print(one_friend)
                mutual_friends_list.append(User(friend))
        else:
            print('Ошибка в запросе.')
            # print(response.json())
        return mutual_friends_list


def mutual_friends(token):
    try:

        user1 = User(get_id_user('1'))
        user1.set_token(token)

        user2 = User(get_id_user('2'))
        user2.set_token(token)

        mutual_friends_of_users = user1 & user2

        print(f'Профиль 1го пользователя {str(user1)}')
        print(f'Профиль 2го пользователя {str(user2)}')

        if len(mutual_friends_of_users) > 0:
            print(f'Всего общих друзей: {len(mutual_friends_of_users)}')
            print('Профили общих друзей:')
            for profile in mutual_friends_of_users:
                print(profile)
        else:
            print('Общих друзей нет')

    except KeyError as err:
        print('Возникла ошибка.')
        print(err.__doc__)

    except ValueError as err:
        print('Введено некорректное значение ID')
        print(err.__doc__)


def get_id_user(number_user):
    user_id = int(input(f'Введите ID пользователя {number_user}:\n'))
    return user_id


TOKEN = 'c81d24660f6c2b52dab84a3e4362a05a538e56ed139a0c2209877c0b41f0c42656df5602808ab06911e26'
mutual_friends(TOKEN)
