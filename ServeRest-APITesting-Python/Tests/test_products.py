import unittest
import requests
import json
import pytest

BASE_URL = "https://api.serverest.dev"


class Products(unittest.TestCase):

    def setUp(self):
        # Do authentication
        # Produto endpoint requires authentication
        full_url = BASE_URL + "/login"
        body = {
            "email": "fulano@qa.com",
            "password": "teste"
        }

        response = requests.post(url=full_url, json=body)
        if response.status_code != 200:
            pytest.fail("Some problem to get authorization token \n", False)

        response_json = json.loads(response.text)
        self.token = response_json["authorization"]

    def test_get_all_products(self):
        full_url = BASE_URL + "/produtos"

        # Send HTTP Request
        response = requests.get(url=full_url)

        # Check the response from ServeRest
        self.assertEqual(response.status_code, 200, "Error in status code to get all products")

    def test_add_product(self):
        full_url = BASE_URL + "/produtos"
        body = {
            "nome": "Monitor TV Acer",
            "preco": "830.00",
            "descricao": "Assista TV a noite, durante o dia use para trabalhar",
            "quantidade": "3"
        }

        header = {"Authorization": self.token}

        # Send HTTP Request
        response = requests.post(url=full_url, headers=header, json=body)
        response_json = json.loads(response.text)

        # Check the response from ServeRest
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json["message"], "Cadastro realizado com sucesso")
        product_id = response_json["_id"]

        # Now we need to remove the product that was created
        # This is a good test automation practice :)
        full_url_del = BASE_URL + "/produtos/" + product_id
        response = requests.delete(url=full_url_del, headers=header)

        self.assertEqual(response.status_code, 200, "Error in status code to delete a product")

    def test_update_product_info(self):
        full_url = BASE_URL + "/produtos"
        body = {
            "nome": "Monitor TV Acer",
            "preco": "830.00",
            "descricao": "Assista TV a noite, durante o dia use para trabalhar",
            "quantidade": "3"
        }

        header = {"Authorization": self.token}

        # Send HTTP Request
        response = requests.post(url=full_url, headers=header, json=body)
        response_json = json.loads(response.text)

        # Check the response from ServeRest
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_json["message"], "Cadastro realizado com sucesso")
        product_id = response_json["_id"]

        ## UPDATE PRODUCT INFO ##
        full_url_update = BASE_URL + "/produtos/" + product_id
        new_body = {
            "nome": "Monitor TV Acer",
            "preco": "630",
            "descricao": "Assista TV ou ligue em um computador",
            "quantidade": "3"
        }

        response = requests.put(url=full_url_update, headers=header, json=body)
        response_json = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json["message"], "Registro alterado com sucesso")

        # Now we need to remove the product that was created
        # This is a good test automation practice :)
        full_url_del = BASE_URL + "/produtos/" + product_id
        response = requests.delete(url=full_url_del, headers=header)

        self.assertEqual(response.status_code, 200, "Error in status code to delete a product")

    def test_delete_unknown_product(self):
        product_id = "12345678"
        full_url_del = BASE_URL + "/produtos/" + product_id

        header = {"Authorization": self.token}

        response = requests.delete(url=full_url_del, headers=header)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.text)
        self.assertEqual(response_json["message"], "Nenhum registro excluído")

    def test_delete_product_without_authentication(self):
        product_id = "12345678"
        full_url_del = BASE_URL + "/produtos/" + product_id

        response = requests.delete(url=full_url_del)
        self.assertEqual(response.status_code, 401)

        response_json = json.loads(response.text)
        self.assertEqual(response_json["message"], "Token de acesso ausente, inválido, "
                                                   "expirado ou usuário do token não existe mais")