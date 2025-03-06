import requests
from jsonschema import validate


GET = "?page=2"



post_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "job": {
      "type": "string"
    },
    "updatedAt": {
      "type": "string"
    }
  },
  "required": [
    "name",
    "job",
    "updatedAt"
  ]
}

def test_api_post():

  base_url = 'https://reqres.in/api/users'
  payload = {
    "name": "morpheus",
    "job": "leader"
  }

  response = requests.post(base_url, data=payload)
  assert response.status_code == 201



def test_api_put():
  base_url = "https://reqres.in/api/users/2"
  new_payload = {
    "name": "morpheus",
    "job": "zion developer"
}

  response = requests.put(base_url, data = new_payload)
  body = response.json()

  assert response.status_code == 200
  assert body['job'] == "zion developer"

  validate(body,schema=post_schema)


