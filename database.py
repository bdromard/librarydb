import requests as req
import json
from pymongo import *
import xmltodict


API_URL = "http://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query="
# ---------------------------------DATABASE CODE------------------------------------------------------------------------
# Database access

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

# Création de la classe Database.
class Database:

    # __init__ de la classe ; initialise le client MongoDO, utilise la DB de test et deux collections : celle de test
    # et posts.
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.testDB
        self.test_collection = self.db.testCollection
        self.posts = self.db.posts


    # Fonction de requête API et d'ajout dans la BDD par ISBN.
    def add_by_isbn(self, isbn):
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
            # Inscription de la réponse dans un fichier JSON, puis lecture pour pouvoir être insérée dans la BDD MongoDB.
            with open("data.json", "w") as data:
                data.write(pretty_response)
            with open("data.json") as file:
                file_data = json.load(file)
            self.posts.insert_one(file_data)

    # Fonction de requête API et d'ajout dans la DB par nom d'auteur.ice.
    def add_by_title(self, title):
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
            self.posts.insert_one(file_data)

    # Fonctions pour retrouver et mettre en forme des recherches dans la base de données.
    def get_author(self, book):
        search = self.test_collection.find({"$text": {"$search": f"{book}"}})
        title_result = search.distinct("oai_dc:dc.dc:creator")
        value_split = title_result[0].split(" ")
        author_ln = value_split[0].strip(',')
        author_fn = value_split[1]
        author_string = f"{author_fn} {author_ln}"
        return author_string

    def get_book(self, author):
        search = self.test_collection.find({"$text": {"$search": f"{author}"}})
        title_result = search.distinct("oai_dc:dc.dc:title")
        value_book_split = title_result[0].split("/")
        title = value_book_split[0]
        return title

    # Fonction de création d'une nouvelle collection dans la DB.
    def create_collection(self, name):
        self.db.createCollection(f'{name}')

    # Fonction permettant de montrer tous les documents d'une collection.
    def show_all_collection(self, collection_name):
        collection_to_show = self.db[f'{collection_name}']
        collection_cursor = collection_to_show.find({})
        for document in collection_cursor:
            print(document)



