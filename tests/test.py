import json
from app import app
import unittest
import confg


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()

    def test_put_data(self):
        data = {"date": "2023-02-04",
                "short_description": "this is a brief description for a document i am trying to insert",
                "link": "http://google.com",
                "category": "WORLD NEWS",
                "headline": "HABIBI MOHAMED ANNIVERSARY",
                "authors": "habibi mohamed"
                }
        headers = {
            "Content-type": "application/json"
        }
        response = self.app.put(confg.BASE_URL + "news/putting2", data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_data(self):
        data = {"date": "2023-02-04",
                "short_description": "this is a brief description for a document i am trying to insert",
                "link": "http://google.com",
                "category": "WORLD NEWS",
                "headline": "HABIBI MOHAMED ANNIVERSARY",
                "authors": "habibi mohamed"
                }
        response = self.app.get(confg.BASE_URL + "news/putting2")
        self.assertEqual(response.get_json(), data)

    def test_delete_data(self):
        response = self.app.delete(confg.BASE_URL + "news/putting2")
        self.assertEqual(response.json, "the document putting2 is deleted = OK..")


if __name__ == '__main__':
    unittest.main()
