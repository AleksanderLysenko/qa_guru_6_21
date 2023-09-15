import allure

from tests.conftest import api

base_url = "https://catfact.ninja"


def test_users_status_code():
    with allure.step('Посылаем GET запрос на проверку статус-кода'):
        response = api(base_url=base_url,
                       method="get",
                       url="/breeds")
    with allure.step('Осуществляем проверку статус кода'):
        assert response.status_code == 200