import requests as req
import json
from pymongo import *
import datetime


# Database access
client = MongoClient()
db = client.testDB
test_collection = db.testCollection
posts = db.posts

# first_book = {"author": "Joseph Conrad",
#               "title": "Heart of Darkness",
#               "tags": ["literature", "english"],
#               "date": datetime.datetime.utcnow()}
#
# post_book = posts.insert_one(first_book)

# API request and insert to database

try:
    response = req.get("https://openlibrary.org/isbn/9780140328721.json")
    response.raise_for_status()
    response_as_json = response.json()
    # Méthode de la librairie json pour mettre en forme le fichier JSON ; type => string.
    pretty_json = json.dumps(response_as_json, sort_keys=True, indent=4)
except Exception as err:
    print(f'An Exception has occurred: {err}')
except TypeError as type_err:
    print(f'Incorrect type file: {type_err}')
else:
    with open("data.json", "w") as data:
        data_to_write = data.write(pretty_json)
    with open("data.json") as file:
        file_data = json.load(file)
    posts.insert_one(file_data)