import requests as req
import json
from pymongo import *
import xmltodict
import tkinter

API_URL = "http://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query="
# ---------------------------------DATABASE CODE------------------------------------------------------------------------
# Database access
client = MongoClient()
db = client.testDB
test_collection = db.testCollection
posts = db.posts

# Fonction pour vérifier le format de l'ISBN, si incorrect ou comportant un tiret ;
# l'API de la BNF n'accepte pas de tiret.
def check_isbn(isbn):
    if not isbn.startswith("978"):
        print("Veuillez insérer un ISBN correct.")
        exit()
    elif isbn.startswith("978-"):
        isbn_split = isbn.split('-')
        isbn_join = ''.join(isbn_split)
        return isbn_join

# Fonction de requête API et d'ajout dans la BDD par ISBN.
def add_by_isbn(isbn):
    # API request and insert to database
    isbn = check_isbn(isbn)
    try:
        # Requête vers le catalogue général de la BNF
        response = req.get(
            f'{API_URL}bib.isbn%20any%20"{isbn}"&recordSchema=dublincore')
        response.raise_for_status()
        response_xml = xmltodict.parse(response.content)
        # Méthode de la librairie json pour mettre en forme le fichier JSON ; type => string.
        if response_xml["srw:searchRetrieveResponse"]["srw:numberOfRecords"] == "0":
            print("La recherche n'a pas renvoyé de résultat, essayez d'autres critères.")
            exit()
    except Exception as err:
        print(f'An Exception has occurred: {err}')
        print("L'ISBN ne renvoie pas de données exploitables. Essayez un autre type de recherche.")
    else:
        pretty_response = json.dumps(
            response_xml["srw:searchRetrieveResponse"]["srw:records"]["srw:record"]["srw:recordData"],
            sort_keys=True,
            indent=4)
        # Inscription de la réponse dans un fichier JSON, puis lecture pour pouvoir être inséré dans la BDD MongoDB.
        with open("data.json", "w") as data:
            data.write(pretty_response)
        with open("data.json") as file:
            file_data = json.load(file)
        posts.insert_one(file_data)

def add_by_title(title):
    try:
        response = req.get(
            f'{API_URL}bib.title%20any%20"{title}"&recordSchema=dublincore&maximumRecords=1')
        response.raise_for_status()
        response_xml = xmltodict.parse(response.content)
        pretty_response = json.dumps(
            response_xml["srw:searchRetrieveResponse"]["srw:records"]["srw:record"]["srw:recordData"]["oai_dc:dc"],
            sort_keys=True,
            indent=4)
    except Exception as err:
        print(f'An Exception has occurred: {err}')
    else:
        with open("data.json", "w") as data:
            data.write(pretty_response)
        with open("data.json") as file:
            file_data = json.load(file)
        posts.insert_one(file_data)

def get_book():
    pass