import unittest
import os
import sys
import json
import requests

sys.path.append("../")

from app import app, db

TEST_DB = "test.sqlite"


class test_pokemon(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
            basedir, TEST_DB
        )
        self.app = app.test_client()
        db.create_all()

    @classmethod
    def tearDownClass(self):
        db.drop_all()

    def test_pokemon_post(self):
        print("_____________test pokemon post________________")
        input_data = {
            "pokemon": {
                "name": "charmander",
                "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
                "cardColours": {"fg": "#eeeeee", "bg": "#3e3e3e", "desc": "#111111"},
            }
        }
        expected_output_data = {
            "pokemon": {
                "id": 1,
                "name": "charmander",
                "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
                "cardColours": {"fg": "#eeeeee", "bg": "#3e3e3e", "desc": "#111111"},
            }
        }
        actual_output_data = self.app.post(
            "http://localhost:8006/api/pokemon",
            data=json.dumps(input_data),
            content_type="application/json",
        )

        json_actual_output_data = json.loads(actual_output_data.data)

        self.assertEqual(
            json.dumps(json_actual_output_data), json.dumps(expected_output_data)
        )
        self.assertEqual(actual_output_data.status_code, 200)
        print("__________test pokemon post succesfull________")

    def test_pokemon_get(self):
        print("_____________test pokemon get_________________")
        expected_output_data = {
            "pokemon": {
                "id": 1,
                "name": "charmander",
                "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
                "cardColours": {"fg": "#eeeeee", "bg": "#3e3e3e", "desc": "#111111"},
            }
        }

        actual_output_data = self.app.get("http://localhost:8006/api/pokemon/1")
        # print(actual_output_data)
        json_actual_output_data = json.loads(actual_output_data.data)
        # print(json_actual_output_data)
        self.assertEqual(
            json.dumps(json_actual_output_data), json.dumps(expected_output_data)
        )
        self.assertEqual(actual_output_data.status_code, 200)
        print("__________test pokemon get succesfull_________")

    def test_pokemon_patch(self):
        print("____________Test pokemon patch_______")
        input_data_to_update = {
            "pokemon": {
                "name": "charmander1",
                "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
                "cardColours": {"fg": "#eeeeee", "bg": "#3e3e3e", "desc": "#111111"},
            }
        }

        expected_output_data_patch = {
            "pokemon": {
                "id": 1,
                "name": "charmander1",
                "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
                "cardColours": {"fg": "#eeeeee", "bg": "#3e3e3e", "desc": "#111111"},
            }
        }

        actual_output_data_patch = self.app.patch(
            "http://localhost:8006/api/pokemo/1n",
            data=json.dumps(input_data_to_update),
            content_type="application/json",
        )

        json_actual_output_data_patch = json.loads(actual_output_data_patch.data)

        self.assertEqual(
            json.dumps(json_actual_output_data_patch),
            json.dumps(expected_output_data_patch),
        )
        self.assertEqual(actual_output_data_patch.status_code, 200)

        print("____________Test pokemon patch succesfull_______")

    def test_pokemon_delete(self):
        print("____________Test pokemon delete_______")
        input_data1 = {
            "pokemon": {
                "name": "charmander1",
                "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
                "cardColours": {"fg": "#eeeeee", "bg": "#3e3e3e", "desc": "#111111"},
            }
        }

        actual_output1 = self.app.delete("http://localhost:8006/api/pokemon/1")
        json_actual1 = json.loads(actual_output_data_patch.data)

        self.assertEqual(json.dumps(input_data1), json.dumps(json_actual1))
        self.assertEqual(actual_output1.status_code, 200)

        print("____________Test pokemon delete succesfull_______")


if __name__ == "__main__":
    unittest.main()

