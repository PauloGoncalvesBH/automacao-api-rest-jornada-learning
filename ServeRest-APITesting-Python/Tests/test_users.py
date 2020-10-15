import unittest
import requests
import json

BASE_URL = "http://localhost:3000"


class Users(unittest.TestCase):

    def test_get_all_users(self):
        full_url = BASE_URL + "/usuarios"

        # Send HTTP Request
        response = requests.get(url=full_url)

        # Check the response from ServeRest
        assert response.status_code == 200

    def test_create_common_user(self):
        full_url = BASE_URL + "/usuarios"
        body = {"nome": "Ketlin Pedron",
                 "email": "kpedron@qa.com",
                 "password": "t1234",
                 "administrador": "false"}

        # Send HTTP Request
        response = requests.post(url=full_url, json=body)

        # Check the response from ServeRest
        assert response.status_code == 201

        response_json = json.loads(response.text)
        assert response_json["message"] == "Cadastro realizado com sucesso"
        user_id = response_json["_id"]

        # It is necessary to remove this user, this is
        # a good test automation practice :)
        full_url_del = full_url + "/" + user_id
        response = requests.delete(url=full_url_del)

        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert response_json["message"] == "Registro excluído com sucesso"


