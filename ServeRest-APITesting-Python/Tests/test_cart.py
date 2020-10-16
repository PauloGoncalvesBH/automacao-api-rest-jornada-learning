import unittest
import requests
import json
import pytest

BASE_URL = "https://api.serverest.dev"


class Products(unittest.TestCase):

    def setUp(self):
        # Do authentication
        # Cart endpoint requires authentication
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

    def test_get_all_cart(self):
        full_url = BASE_URL + "/carrinhos"

        # Send HTTP Request
        response = requests.get(url=full_url)

        # Check the response from ServeRest
        self.assertEqual(response.status_code, 200, "Error in status code to get all carts")

    def test_create_cart_to_user(self):
        full_url = BASE_URL + "/carrinhos"
        body = {
            "produtos": [
                {
                    "idProduto": "K6leHdftCeOJj8BJ",
                    "quantidade": 2
                }
            ]
        }

        header = {"Authorization": self.token}

        # Send HTTP Request
        response = requests.post(url=full_url, headers=header, json=body)

        # Check the response from ServeRest
        self.assertEqual(response.status_code, 201, "Error in status code to create a cart")
        response_json = json.loads(response.text)
        self.assertEqual(response_json["message"], "Cadastro realizado com sucesso")

        # Now we will delete the cart (this is a good practice)
        # Buy the item will delete the cart automatically
        full_url = BASE_URL + "/carrinhos/concluir-compra"
        # The endpoint delete the cart using the Authorization token from the user
        response = requests.delete(url=full_url, headers=header)

        self.assertEqual(response.status_code, 200, "Error in status code to delete a cart")

    def test_get_cart_from_specific_user(self):
        full_url = BASE_URL + "/carrinhos"
        query = {"idUsuario": "K6leHdftCeOJj8BJ"}

        # Send HTTP Request
        response = requests.get(url=full_url, params=query)

        self.assertEqual(response.status_code, 200, "Error in status code to get a cart")

    def test_create_cart_without_authentication(self):
        full_url = BASE_URL + "/carrinhos"
        body = {
            "produtos": [
                {
                    "idProduto": "K6leHdftCeOJj8BJ",
                    "quantidade": 2
                }
            ]
        }

        # Send HTTP Request
        response = requests.post(url=full_url, json=body)

        # Check the response from ServeRest
        self.assertEqual(response.status_code, 401)

        response_json = json.loads(response.text)
        self.assertEqual(response_json["message"], "Token de acesso ausente, inválido, expirado ou usuário "
                                                   "do token não existe mais")

    def test_create_cart_unknown_product(self):
        full_url = BASE_URL + "/carrinhos"
        body = {
            "produtos": [
                {
                    "idProduto": "234",
                    "quantidade": 4
                }
            ]
        }

        header = {"Authorization": self.token}

        # Send HTTP Request
        response = requests.post(url=full_url, headers=header, json=body)

        # Check the response from ServeRest
        self.assertEqual(response.status_code, 400)

        response_json = json.loads(response.text)
        self.assertEqual(response_json["message"], "Produto não encontrado")

