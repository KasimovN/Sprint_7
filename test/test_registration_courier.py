import allure
import pytest
import requests

from data import Data


class TestRegistrarionCourier:
    success_ans_text = '{"ok":true}'
    dublicate_ans_text = 'Этот логин уже используется'
    false_ans_text = 'Недостаточно данных для создания учетной запис'

    @allure.title('Тест эндпоинта создания курьера')
    @allure.link('https://qa-scooter.praktikum-services.ru/api/v1/courier')
    @allure.description('Все тесты автономны. Все тестовые сущности удаляются после прохождения теста.')
    @allure.step('Тестируем успешное создание курьера')
    def test_success_register(self, create_creds):
        # Проверка, что нет курьера в БД
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=create_creds)
        assert response.status_code == 404

        # Проверка на создание курьера
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER, data=create_creds)
        assert response.status_code == 201 and response.text == self.success_ans_text

        # Проверка, что в БД появился созданный курьер
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=create_creds)
        user_id = str(response.json()['id'])
        assert response.status_code == 200

        # Удаляем созданного курьера
        requests.delete(Data.URL_BASE + Data.URL_REGISTER_COURIER + '/' + user_id)

        # Проверяем, что удалили из БД
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=create_creds)
        assert response.status_code == 404

    @allure.step('Тестируем дублирование курьера')
    def test_dublicate_registration(self, create_creds):
        # Создаем курьера
        requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER, data=create_creds)

        # Проверка, что в БД есть курьер
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=create_creds)
        user_id = str(response.json()['id'])
        assert response.status_code == 200

        # Дублируем регистрацию, ранее созданного курьера
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER, data=create_creds)
        assert response.status_code == 409 and self.dublicate_ans_text in response.text

        # Удаляем созданного курьера
        requests.delete(Data.URL_BASE + Data.URL_REGISTER_COURIER + '/' + user_id)

        # Проверяем, что удалили из БД
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=create_creds)
        assert response.status_code == 404

    @allure.step('Тестируем отработку ошибочного запроса: не все обязательные параметры переданы в запросе')
    @pytest.mark.parametrize('param', ['login', 'password'])
    def test_false_registration(self, param, create_creds):
        payload_modify = {param: create_creds[param]}
        # Проверка, что нет курьера в БД
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER + Data.URL_LOGIN_COURIER, data=create_creds)
        assert response.status_code == 404
        # Проверка ответа при регистрации только с одним обязательным параметром
        response = requests.post(Data.URL_BASE + Data.URL_REGISTER_COURIER, data=payload_modify)
        assert response.status_code == 400 and self.false_ans_text in response.text
