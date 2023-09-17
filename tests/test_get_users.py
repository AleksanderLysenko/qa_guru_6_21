import json
import os

import allure
from jsonschema.validators import validate
from tests.conftest import resources_path, api

base_url = "https://reqres.in"


def test_users_list_users():
    per_page = 8

    with allure.step('Посылаем GET запрос на просмотр списка юзеров'):
        response = api(base_url=base_url,
                       method="get",
                       url="/api/users",
                       params={"per_page": per_page}
                       )

    with allure.step('Осуществляем проверки'):
        assert response.status_code == 200
        assert response.json()['per_page'] == per_page
        assert len(response.json()['data']) == per_page


def test_users_status_code():
    with allure.step('Посылаем GET запрос на проверку статус-кода'):
        response = api(base_url=base_url,
                       method="get",
                       url="/api/users")

    with allure.step('Осуществляем проверку статус кода'):
        assert response.status_code == 200


def test_users_single_user_not_found():
    with allure.step('Посылаем GET запрос на просмотр юзера'):
        response = api(base_url=base_url,
                       method="get",
                       url="/api/users/23")

    with allure.step('Осуществляем проверку статус кода'):
        assert response.status_code == 404


def test_users_create_user():
    name = 'alex'
    job = 'tester'

    with allure.step('Посылаем POST запрос на создание юзера'):
        response = api(base_url=base_url,
                       method="post",
                       url="/api/users",
                       data={"name": name, "job": job}
                       )

    with allure.step('Осуществляем проверки'):
        assert response.status_code == 201
        assert response.json()['name'] == name
        assert response.json()['job'] == job


def test_users_update_user():
    name = 'alex'
    job = 'lead'

    with allure.step('Посылаем PUT запрос на обновление юзера'):
        response = api(base_url=base_url,
                       method="put",
                       url="/api/users/2",
                       data={"name": name, "job": job}
                       )

    with allure.step('Осуществляем проверки'):
        assert response.status_code == 200
        assert response.json()['name'] == name
        assert response.json()['job'] == job


def test_users_delete_user():
    with allure.step('Посылаем DELETE запрос на удаление юзера'):
        response = api(base_url=base_url,
                       method="delete",
                       url="/api/users/2")

    with allure.step('Осуществляем проверку'):
        assert response.status_code == 204


def test_users_register_successful_user():
    email = "eve.holt@reqres.in"
    password = "pistol"

    with allure.step('Посылаем POST запрос на регистрацию юзера'):
        response = api(base_url=base_url,
                       method="post",
                       url="/api/register",
                       data={"email": email, "password": password}
                       )

    with allure.step('Осуществляем проверки'):
        assert response.status_code == 200
        assert response.json()['id'] == 4
        assert response.json()['token'] == 'QpwL5tke4Pnpja7X4'


def test_users_register_unsuccessful_user():
    email = "eve.holt@reqres.in"

    with allure.step('Посылаем POST запрос на регистрацию юзера'):
        response = api(base_url=base_url,
                       method="post",
                       url="/api/register",
                       data={"email": email}
                       )

    with allure.step('Осуществляем проверки'):
        assert response.status_code == 400
        assert response.json()['error'] == 'Missing password'


def test_users_login_successful_user():
    email = "eve.holt@reqres.in"
    password = "cityslicka"

    with allure.step('Посылаем POST запрос на login юзера'):
        response = api(base_url=base_url,
                       method="post",
                       url="/api/login",
                       data={"email": email, "password": password}
                       )

    with allure.step('Осуществляем проверки'):
        assert response.status_code == 200
        assert response.json()['token'] == 'QpwL5tke4Pnpja7X4'


def test_users_login_unsuccessful_user():
    email = "peter@klaven"

    with allure.step('Посылаем POST запрос на login юзера'):
        response = api(base_url=base_url,
                       method="post",
                       url="/api/login",
                       data={"email": email}
                       )

    with allure.step('Осуществляем проверки'):
        assert response.status_code == 400
        assert response.json()['error'] == 'Missing password'


def test_users_delayed_response_users():
    per_page = 6

    with allure.step('Посылаем GET запрос на просмотр списка юзеров'):
        response = api(base_url=base_url,
                       method="get",
                       url="/api/users?delay=4",
                       params={"per_page": per_page}
                       )

    with allure.step('Осуществляем проверки'):
        assert response.status_code == 200
        assert response.json()['page'] == 1
        assert response.json()['per_page'] == per_page


def test_users_schema():
    with allure.step('Открываем файл get_users_schema.json на чтение'):
        with open(os.path.join(resources_path, 'get_users_schema.json')) as file:
            schema = json.loads(file.read())

    with allure.step('Посылаем GET запрос на просмотр списка юзеров'):
        response = api(base_url=base_url,
                       method="get",
                       url="/api/users")

    with allure.step('Валидируем схему'):
        validate(instance=response.json(), schema=schema)


def test_users_create_user_schema():
    name = 'alex'
    job = 'tester'

    with allure.step('Открываем файл get_users_create_user_schema.json на чтение'):
        with open(os.path.join(resources_path, 'get_users_create_user_schema.json')) as file:
            schema = json.loads(file.read())

    with allure.step('Посылаем POST запрос на создание юзера'):
        response = api(base_url=base_url,
                       method="post",
                       url="/api/users",
                       data={"name": name, "job": job}
                       )

    with allure.step('Валидируем схему'):
        validate(instance=response.json(), schema=schema)
