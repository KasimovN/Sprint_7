import allure
import pytest
import requests

from data import Data


class TestOrder:

    @allure.title('Тестируем эндпоинт заказа')
    @allure.link('https://qa-scooter.praktikum-services.ru/api/v1/orders')
    @allure.step('Тестируем успешное создание заказа')
    @pytest.mark.parametrize('param', Data.SCOOTER_COLORS)
    def test_success_create_order(self, param):
        body = Data.ORDER_INFO.copy()
        body['color'] = param
        response = requests.post(Data.URL_BASE + Data.URL_ORDERS, json=body)
        assert response.status_code == 201 and response.json()['track']
        print(response.json()['track'])
        # print(response.)

    @allure.step('Тестируем список заказов')
    def test_orders_list(self):
        orders = requests.get(Data.URL_BASE + Data.URL_ORDERS)
        assert orders.status_code == 200 and len(orders.json()['orders']) > 0
