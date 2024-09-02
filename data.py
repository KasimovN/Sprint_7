class Data:
    LOGIN_LENGTH = 10
    PASSWORD_LENGTH = 10

    URL_BASE = 'https://qa-scooter.praktikum-services.ru/api/v1'
    URL_REGISTER_COURIER = '/courier'
    URL_LOGIN_COURIER = '/login'
    URL_ORDERS = '/orders'

    ORDER_INFO = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha"}

    SCOOTER_COLORS = [['BLACK'], ['GREY'], ['BLACK', 'GREY'], []]
