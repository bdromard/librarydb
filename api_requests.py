import requests as req
import json
from pymongo import *
import xmltodict
import tkinter

isbn = "%229782707321213%22&"

# ---------------------------------DATABASE CODE------------------------------------------------------------------------
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
    # Requête vers OpenLibrary
    # response = req.get("https://openlibrary.org/isbn/9780140328721.json")

    # Requête vers le catalogue général de la BNF
    response = req.get(
        f"http://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.isbn%20any%20{isbn}&recordSchema=dublincore")
    response.raise_for_status()
    response_xml = xmltodict.parse(response.content)

    # Méthode de la librairie json pour mettre en forme le fichier JSON ; type => string.
    pretty_response = json.dumps(
        response_xml["srw:searchRetrieveResponse"]["srw:records"]["srw:record"]["srw:recordData"],
        sort_keys=True,
        indent=4)
except Exception as err:
    print(f'An Exception has occurred: {err}')
else:
    # Inscription de la réponse dans un fichier JSON, puis lecture pour pouvoir être inséré dans la BDD MongoDB.
    with open("data.json", "w") as data:
        data_to_write = data.write(pretty_response)
    with open("data.json") as file:
        file_data = json.load(file)
    test_collection.insert_one(file_data)

# ---------------------------------------------------INTERFACE CODE-----------------------------------------------------
