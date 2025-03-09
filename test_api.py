import requests
from jsonschema import validate
from schemas import *


base_url = 'https://reqres.in/'
get_route = base_url + 'api/users'


class TestGetApi:

    def test_get_status_code(self):
      response_code = requests.get(get_route).status_code
      assert response_code == 200

    def test_get_schema(self):
      response=requests.get(get_route).json()
      validate(response, get_schema)


class TestPostApi:
  post_route = base_url + 'api/register'

  payload = {
    "email": "eve.holt@reqres.in",
    "password": "testPass"
  }

  def test_post_status_code(self):
    current_status_code = requests.post(self.post_route, self.payload).status_code
    assert  current_status_code == 200

  def test_post_without_email(self):
    new_body = self.payload.copy()
    del new_body['email']

    current_status_code = requests.post(self.post_route, new_body).status_code
    current_response_data = requests.post(self.post_route, new_body).json()

    assert current_status_code == 400 and current_response_data['error'] == 'Missing email or username'

  def test_post_without_pass(self):
    new_body = self.payload.copy()
    del new_body['password']

    current_status_code = requests.post(self.post_route, new_body).status_code
    current_response_data = requests.post(self.post_route, new_body).json()

    assert current_status_code == 400 and current_response_data['error'] == 'Missing password'

  def test_post_response_schema(self):
    response = requests.post(self.post_route, self.payload).json()
    assert validate(response, post_schema2)



# validate - получаю ошибку соответствия схем