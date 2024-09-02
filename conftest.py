import pytest
from data import Data
from helper import Helper


@pytest.fixture()
def create_creds():
    # генерируем логин, пароль и имя курьера
    login = Helper.generate_random_string(Data.LOGIN_LENGTH)
    password = Helper.generate_random_string(Data.PASSWORD_LENGTH)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
    }

    # возвращаем список
    return payload
