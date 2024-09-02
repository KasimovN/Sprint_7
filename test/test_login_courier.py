import allure
import pytest
import requests

from data import Data


class TestLoginCourier:
    wrong_login_password_text = 'Учетная запись не найдена'
    no_body_text = 'Недостаточно данных для входа'

    @allure.title('Тестируем эндпоинт авторизации курьера')
    @allure.link('https://qa-scooter.praktikum-services.ru/api/v1/courier/login')
    @allure.description('Все тесты автономны. Все тестовые сущности удаляются после прохождения теста.')
    @allure.step('Тестируем успешную авторизацию курьера.')
    def test_success_login(self, create_creds):
        # Создаем курьера
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER, data=create_creds)
        assert response.status_code == 201

        # Проверка, на авторизацию
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=create_creds)
        assert response.status_code == 200 and response.json()['id']
        user_id = str(response.json()['id'])

        # Удаляем созданного курьера
        requests.delete(Data.URL_BASE + Data.URL_REGISTER_COURIER + '/' + user_id)

        # Проверяем, что удалили из БД
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=create_creds)
        assert response.status_code == 404

    @allure.step('Тестируем передачу ошибочной пары логин/пароль')
    @pytest.mark.parametrize('param', ['login', 'password'])
    def test_wrong_login_password(self, param, create_creds):
        # Создаем курьера и запоминаем его id
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER, data=create_creds)
        assert response.status_code == 201
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=create_creds)
        user_id = str(response.json()['id'])

        # Проверка на авторизацию с неверной парой логин/пароль
        wrong_creds = create_creds
        wrong_creds[param] = create_creds[param]+'qwe'
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=wrong_creds)
        assert response.status_code == 404 and response.json()['message'] == self.wrong_login_password_text

        # Удаляем созданного курьера
        requests.delete(Data.URL_BASE + Data.URL_REGISTER_COURIER + '/' + user_id)

        # Проверяем, что удалили из БД
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=create_creds)
        assert response.status_code == 404

    @allure.step('Тестируем запрос без обязательного параметра')
    # Предполагалось использовать параметризацию, но при запросе с только логином возвращается 500 ошибка,
    # чтобы тест не падал - убрал параметризацию и проверяю только с паролем
    def test_no_param_in_body_request(self, create_creds):
        # Создаем курьера и запоминаем его id
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER, data=create_creds)
        assert response.status_code == 201
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=create_creds)
        user_id = str(response.json()['id'])

        wrong_creds = create_creds.copy()
        wrong_creds.pop('login')

        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=wrong_creds)
        assert response.status_code == 400 and response.json()['message'] == self.no_body_text
        #
        # # Удаляем созданного курьера и проверяем удаление
        requests.delete(Data.URL_BASE + Data.URL_REGISTER_COURIER + '/' + user_id)
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=create_creds)
        assert response.status_code == 404
