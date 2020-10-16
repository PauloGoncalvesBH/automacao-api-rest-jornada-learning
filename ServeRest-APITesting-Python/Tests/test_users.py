import unittest
import requests
import json

BASE_URL = "https://api.serverest.dev"


class Users(unittest.TestCase):

    def test_get_all_users(self):
        full_url = BASE_URL + "/usuarios"

        # Send HTTP Request
        response = requests.get(url=full_url)

        # Check the response from ServeRest
        self.assertEqual(response.status_code, 200, "Error in status code to get all user")

    def test_create_common_user(self):
        full_url = BASE_URL + "/usuarios"
        body = {"nome": "Ketlin Pedron",
                 "email": "kpedron@qa.com",
                 "password": "t1234",
                 "administrador": "false"}

        # Send HTTP Request
        response = requests.post(url=full_url, json=body)

        # Check the response from ServeRest
        self.assertEqual(response.status_code, 201, "Error in status code to create an user")

        response_json = json.loads(response.text)
        self.assertEqual(response_json["message"], "Cadastro realizado com sucesso")
        user_id = response_json["_id"]

        # It is necessary to remove this user, this is
        # a good test automation practice :)
        full_url_del = full_url + "/" + user_id
        response = requests.delete(url=full_url_del)
        self.assertEqual(response.status_code, 200, "Error in status code to delete a user")

        response_json = json.loads(response.text)
        self.assertEqual(response_json["message"], "Registro excluído com sucesso")

    def test_update_user_info(self):
        full_url = BASE_URL + "/usuarios"
        body = {"nome": "Ketlin Pedron",
                "email": "kpedron@qa.com",
                "password": "t1234",
                "administrador": "false"}

        # Send HTTP Request
        response = requests.post(url=full_url, json=body)
        response_json = json.loads(response.text)
        user_id = response_json["_id"]

        # Check the response from ServeRest
        self.assertEqual(response.status_code, 201, "Error in status code to create an user")

        # Now we will update information (email + password)
        full_url = BASE_URL + "/usuarios/" + user_id
        new_body = {"nome": "Ketlin Pedron",
                    "email": "newemail@qa.com",
                    "password": "passwd123",
                    "administrador": "false"}

        # Send HTTP Request
        response = requests.put(url=full_url, json=new_body)
        self.assertEqual(response.status_code, 200, "Error in status to update an user information")

        response_json = json.loads(response.text)
        self.assertEqual(response_json["message"],  "Registro alterado com sucesso")

        # It is necessary to remove this user, this is
        # a good test automation practice :)
        full_url_del = BASE_URL + "/usuarios/" + user_id
        response = requests.delete(url=full_url_del)

        self.assertEqual(response.status_code, 200, "Error in status code to delete a user")

    def test_find_unknown_user(self):
        full_url = BASE_URL + "/usuarios"
        query= {"_id": "123"}

        # Send HTTP Request
        response = requests.get(url=full_url, params=query)

        # Check the response from ServeRest
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.text)
        self.assertEqual(response_json["quantidade"], 0, "Quantidade invalida de items para usuario "
                                                         "nao cadastrado")

