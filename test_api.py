import requests
import json
import logging
from jsonschema import validate
import pytest
from schemas import *
from allure_commons.types import AttachmentType
from allure import step, attach

BASE_URL = "https://reqres.in/"
logger = logging.getLogger(__name__) #Конфигурация логирования


def send_request(method, endpoint, **kwargs):
  """
  Функция для отправки HTTP-запросов.
  :param method: Метод запроса (GET, POST и т.д.)
  :param endpoint: Конечная точка API
  :param kwargs: Дополнительные параметры для requests
  :return: Ответ сервера
  """
  url = f"{BASE_URL}{endpoint}"
  try:
    response = requests.request(method, url, **kwargs)
    response.raise_for_status()  # Проверка HTTP-статуса
    return response
  except requests.exceptions.RequestException as e:
    logger.error(f"Request failed: {e}")
    raise

def log_response(response):
  """Логирование ответа сервера."""
  logger.info(f"Request URL: {response.request.url}")
  logger.info(f"Status Code: {response.status_code}")
  logger.info(f"Response Body: {response.text}")

def attach_to_allure(response):
  """Прикрепление ответа к Allure отчету."""
  with step("Attach Response to Allure"):
      attach(
        body=json.dumps(response.json(), indent=4, ensure_ascii=True),
        name="Response",
        attachment_type=AttachmentType.JSON,
        extension="json"
       )

@pytest.fixture
def get_users():
    """Фикстура для получения данных пользователей."""
    endpoint = "api/users"
    response = send_request("GET", endpoint)
    log_response(response)
    attach_to_allure(response)
    return response



class TestGetApi:

    def test_get_status_code(self, get_users):
        assert get_users.status_code == 200

    def test_get_schema(self, get_users):
        validate(get_users.json(), get_schema)


class TestPostApi:
    path = BASE_URL + 'api/users'
    payload = {
        "name": "Dismo",
        "job": "develop"
    }

    def test_post_status_code(self):
        current_status_code = requests.post(self.path, self.payload).status_code
        assert current_status_code == 201

    def test_post_without_body(self):
        current_status_code = requests.post(self.path).status_code
        current_response_data = requests.post(self.path).json()
        assert current_status_code == 201
        validate(current_response_data, post_schema)

    def test_post_response_schema(self):
        response = requests.post(self.path, self.payload).json()
        missing_keys = [key for key in self.payload if key not in response]
        assert not missing_keys, f"Отсутствующие ключи: {missing_keys}"
        validate(response, post_schema)


class TestPutApi:
    path = BASE_URL + 'api/users/2'
    payload = {
        "name": "morpheus",
        "job": "zion resident"
    }

    def test_put_status_code(self):
        current_status_code = requests.put(self.path, self.payload).status_code
        assert current_status_code == 200

    def test_put_response_schema(self):
        response = requests.put(self.path, data=self.payload).json()
        missing_keys = [key for key in self.payload if key not in response]
        assert not missing_keys, f"Отсутствующие ключи: {missing_keys}"
        validate(response, put_schema)

    def test_put_without_body(self):
        current_status_code = requests.put(self.path).status_code
        current_response_data = requests.put(self.path).json()
        assert current_status_code == 200
        validate(current_response_data, put_schema)


class TestDeleteApi:
    path = BASE_URL + 'api/users/2'

    def test_del_status_code(self):
        current_status_code = requests.delete(self.path).status_code
        assert current_status_code == 204


class TestPostApiRegister:
    path = BASE_URL + 'api/register'
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "testPass"
    }

    def test_post_status_code(self):
        current_status_code = requests.post(self.path, self.payload).status_code
        assert current_status_code == 200

    def test_post_without_email(self):
        new_body = self.payload.copy()
        del new_body['email']
        current_status_code = requests.post(self.path, new_body).status_code
        current_response_data = requests.post(self.path, new_body).json()
        assert current_status_code == 400 and current_response_data['error'] == 'Missing email or username'

    def test_post_without_pass(self):
        new_body = self.payload.copy()
        del new_body['password']
        current_status_code = requests.post(self.path, new_body).status_code
        current_response_data = requests.post(self.path, new_body).json()
        assert current_status_code == 400 and current_response_data['error'] == 'Missing password'

    def test_post_response_schema(self):
        response = requests.post(self.path, self.payload).json()
        validate(response, post_schema_register)