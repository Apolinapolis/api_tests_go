import requests
from jsonschema import validate
from schemas import *


base_url = 'https://reqres.in/'


class TestGetApi:
    get_route = base_url + 'api/users'

    def test_get_status_code(self):
      response_code = requests.get(self.get_route).status_code
      assert response_code == 200

    def test_get_schema(self):
      response=requests.get(self.get_route).json()
      validate(response, get_schema)


class TestPostApi:
  path = base_url + 'api/users'
  payload = {
    "name": "Dismo",
    "job": "develop"
}

  def test_post_status_code(self):
    current_status_code = requests.post(self.path, self.payload).status_code
    assert  current_status_code == 201

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
  path = base_url + 'api/users/2'
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
  path = base_url + 'api/users/2'

  def test_del_status_code(self):
    current_status_code = requests.delete(self.path).status_code
    assert current_status_code == 204


class TestPostApiRegister:
  path = base_url + 'api/register'
  payload = {
    "email": "eve.holt@reqres.in",
    "password": "testPass"
  }

  def test_post_status_code(self):
    current_status_code = requests.post(self.path, self.payload).status_code
    assert  current_status_code == 200

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