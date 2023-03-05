import json
import requests
import confg

data = {"date": "2023-02-04",
        "short_description": "this is a brief description for a document i am trying to insert",
        "link": "http://google.com",
        "category": "WORLD NEWS",
        "headline": "HABIBI MOHAMED ANNIVERSARY",
        "authors": "habibi mohamed"
        }

data_ = {
        "short_description": "this is a brief description for a document i am trying to update",
        "link": "http://github.com",
        }

headers = {
    "Content-type": "application/json"
}

# response = requests.put(confg.BASE_URL + "news/testing2", data=json.dumps(data), headers=headers)
response = requests.patch(confg.BASE_URL + "news/testing2", data=json.dumps(data_), headers=headers)
# response = requests.delete(confg.BASE_URL + "news/testing2")

print(response.json())
