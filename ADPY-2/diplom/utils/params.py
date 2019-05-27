from config import FIELDS


def ask_params():
    user_id = input('Введите ID пользователя: ')
    age_from = input('Возраст от: ')
    age_to = input('Возраст до: ')
    sex = input('Пол (1 — женский, 2 - мужской, 0 - оба): ')
    return user_id, sex, age_from, age_to


def ask_missing_params(user):
    updated_data = dict()
    for item in FIELDS.split(', ')[1:3]:
        if item not in user.user_data:
            updated_data[item] = input(f'{item.capitalize()} ID: ')
    for item in FIELDS.split(', ')[4:]:
        if item not in user.user_data or user.user_data[item] is '':
            if item == 'tv':
                updated_data[item] = input(f'Введите {item} show: ')
            else:
                updated_data[item] = input(f'Введите {item}: ')
    return updated_data


def update_params(user):
    missing_params = ask_missing_params(user)
    if missing_params:
        user.update_user_data(missing_params)
