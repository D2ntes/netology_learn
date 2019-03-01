import requests


class UserVk:
    def __init__(self, user_id):
        self.vk_user_id = user_id
        self.token = ''

    def __str__(self):
        loc_user_id_prefix = 'https://vk.com/id'
        return (f'{loc_user_id_prefix}{self.vk_user_id}')

    def set_token(self, iv_str_token):
        self.token = iv_str_token

    def __and__(self, other):
        lv_url_com_mutual_fr = 'https://api.vk.com/method/friends.getMutual'
        list_common_friends = []
        params = {
            'access_token': self.token,
            'v': '5.92',
            'source_uid': self.vk_user_id,
            'target_uid': other.vk_user_id
        }
        response = requests.get(lv_url_com_mutual_fr, params)
        print(response.json())
        if str(response.status_code) == '200':
            for one_friend in response.json()['response']:
                print(one_friend)
                loc_vk_user = UserVk(one_friend)
                list_common_friends.append(loc_vk_user)
        else:
            print('Что-то пошло не так. Нужно Детальнее смотреть ответ')
            print(response.json())
        return list_common_friends