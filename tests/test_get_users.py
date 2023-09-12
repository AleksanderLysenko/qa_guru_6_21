import json
import os

import requests
from jsonschema.validators import validate

from tests.conftest import resources_path


def test_users_list_users():
    per_page = 8

    response = requests.get(
        url="https://reqres.in/api/users",
        params={"per_page": per_page}
    )

    assert response.status_code == 200
    assert response.json()['per_page'] == per_page
    assert len(response.json()['data']) == per_page


def test_users_status_code():
    response = requests.get("https://reqres.in/api/users")

    assert response.status_code == 200


def test_users_single_user_not_found():
    response = requests.get("https://reqres.in/api/users/23")

    assert response.status_code == 404


def test_users_create_user():
    response = requests.post(
        url="https://reqres.in/api/users",
        data={'name': 'alex', 'job': 'tester'}
    )

    assert response.status_code == 201
    assert response.json()['name'] == 'alex'
    assert response.json()['job'] == 'tester'


def test_users_update_user():
    response = requests.put(
        url="https://reqres.in/api/users/2",
        data={'name': 'alex', 'job': 'lead'}
    )

    assert response.status_code == 200
    assert response.json()['name'] == 'alex'
    assert response.json()['job'] == 'lead'


def test_users_delete_user():
    response = requests.delete("https://reqres.in/api/users/2")

    assert response.status_code == 204


def test_users_register_successful_user():
    response = requests.post(
        url="https://reqres.in/api/register",
        data={"email": "eve.holt@reqres.in", "password": "pistol"}
    )

    assert response.status_code == 200
    assert response.json()['id'] == 4
    assert response.json()['token'] == 'QpwL5tke4Pnpja7X4'


def test_users_register_unsuccessful_user():
    response = requests.post(
        url="https://reqres.in/api/register",
        data={"email": "eve.holt@reqres.in"}
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'


def test_users_login_successful_user():
    response = requests.post(
        url="https://reqres.in/api/login",
        data={"email": "eve.holt@reqres.in", "password": "cityslicka"}
    )

    assert response.status_code == 200
    assert response.json()['token'] == 'QpwL5tke4Pnpja7X4'


def test_users_login_unsuccessful_user():
    response = requests.post(
        url="https://reqres.in/api/login",
        data={"email": "peter@klaven"}
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'


def test_users_delayed_response_users():
    response = requests.get("https://reqres.in/api/users?delay=4")

    assert response.status_code == 200
    assert response.json()['page'] == 1
    assert response.json()['per_page'] == 6


def test_users_schema():
    with open(os.path.join(resources_path, 'get_users_schema.json')) as file:
        schema = json.loads(file.read())

    response = requests.get("https://reqres.in/api/users")

    validate(instance=response.json(), schema=schema)


def test_users_create_user_schema():
    with open(os.path.join(resources_path, 'get_users_create_user_schema.json')) as file:
        schema = json.loads(file.read())

    response = requests.post(
        url="https://reqres.in/api/users",
        data={'name': 'alex', 'job': 'tester'}
    )

    validate(instance=response.json(), schema=schema)

