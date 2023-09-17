import json
import os

import allure
from jsonschema.validators import validate
from tests.conftest import api, resources_path

base_url = "https://catfact.ninja"


def test_list_of_breeds(setup_browser):
    with allure.step('Посылаем GET запрос на просмотр списка'):
        response = api(base_url=base_url,
                       method="get",
                       url="/breeds")

    with allure.step('Осуществляем проверку статус кода'):
        assert response.status_code == 200


def test_list_of_breeds_schema(setup_browser):
    with allure.step('Открываем файл get_list_of_breads_schema.json на чтение'):
        with open(os.path.join(resources_path, 'get_list_of_breads_schema.json')) as file:
            schema = json.loads(file.read())

    with allure.step('Посылаем GET запрос на просмотр списка'):
        response = api(base_url=base_url,
                       method="get",
                       url="/breads")

    with allure.step('Валидируем схему'):
        validate(instance=response.json(), schema=schema)


def test_get_random_fact(setup_browser):
    with allure.step('Посылаем GET запрос на выдачу рандомного факта'):
        response = api(base_url=base_url,
                       method="get",
                       url="/fact")

    with allure.step('Осуществляем проверку статус кода'):
        assert response.status_code == 200


def test_get_random_fact_schema(setup_browser):
    with allure.step('Открываем файл get_random_fact_schema.json на чтение'):
        with open(os.path.join(resources_path, 'get_random_fact_schema.json')) as file:
            schema = json.loads(file.read())

    with allure.step('Посылаем GET запрос на просмотр списка'):
        response = api(base_url=base_url,
                       method="get",
                       url="/fact")

    with allure.step('Валидируем схему'):
        validate(instance=response.json(), schema=schema)
