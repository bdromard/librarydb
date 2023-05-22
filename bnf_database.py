import requests as req
import json
import pandas
from pymongo import *
import xmltodict
import errors
import gui



API_URL = "http://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query="
# ---------------------------------DATABASE CODE------------------------------------------------------------------------
# Database access

# Checking ISBN format: BNF API does not allow hyphen.
def check_isbn(isbn):
    if not isbn.startswith("978"):
        gui.MainWindow.raise_error(gui.MainWindow(), 'Veuillez insérer un ISBN au bon format.')
        raise errors.IncorrectISBNFormat
    elif isbn.startswith("978-"):
        isbn_split = isbn.split('-')
        isbn_join = ''.join(isbn_split)
        return isbn_join
    else:
        return isbn

# Database class creation.
class Database:

    # class __init__ ; MongoDB client init, using test DB and two test collections.
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.testDB
        self.test_collection = self.db.testCollection
        self.posts = self.db.posts

    def get_collection(self):
        return self.posts

    # Fonction de requête API et d'ajout dans la BDD par ISBN.
    def add_by_isbn(self, isbn):
        # API request and insert to database.
        # ISBN verification : ISBN format and whether the reference already exists in collection.
        # check_isbn will return an error for the user if the reference is already present in collection ;
        # otherwise, it will execute the API request.
        correct_isbn = check_isbn(isbn)
        self.get_isbn(correct_isbn)
        # if correct_isbn == verified_isbn:
        #     gui.MainWindow.raise_error(gui.MainWindow(), 'Cette référence est déjà présente dans votre collection')
        #     raise errors.ExistingReference()
        try:
            # BNF API request.
            response = req.get(
                f'{API_URL}bib.isbn%20any%20"{correct_isbn}"&recordSchema=dublincore')
            response.raise_for_status()
            response_xml = xmltodict.parse(response.content)
            # Search is the number of results through the BNF API request. If there are no results, then exception raised.
            # Except is used for GUI error and user feedback.
            search = response_xml["srw:searchRetrieveResponse"]["srw:numberOfRecords"]
            if search == "0":
                raise errors.ResultError(search)
        except Exception as err:
            gui.MainWindow.raise_error(gui.MainWindow(), "L'ISBN ne renvoie pas de données exploitables. "
                                                         "Essayez un autre type de recherche.")
        else:
            # JSON method to prettify JSON file. Returns string.
            pretty_response = json.dumps(
                response_xml["srw:searchRetrieveResponse"]["srw:records"]["srw:record"]["srw:recordData"],
                sort_keys=True,
                indent=4)
            print(pretty_response)
            # File open and write JSON data, accepted by MongoDB. Collection insert.
            with open("data.json", "w") as data:
                data.write(pretty_response)
            with open("data.json") as file:
                file_data = json.load(file)
            self.posts.insert_one(file_data)

    # Function for API request and adding reference in collection.
    def add_by_title(self, title):
        # Check if title reference is already present in the collection.
        verified_title = self.get_title(title)
        # if title == verified_title:
        #     gui.MainWindow.raise_error(gui.MainWindow(), 'Cette référence est déjà présente dans votre collection')
        #     raise errors.ExistingReference()
        try:
            response = req.get(
                f'{API_URL}bib.title%20any%20"{verified_title}"&recordSchema=dublincore&maximumRecords=1')
            response.raise_for_status()
            response_xml = xmltodict.parse(response.content)
            search = response_xml["srw:searchRetrieveResponse"]["srw:numberOfRecords"]
            if search == "0":
                raise errors.ResultError(search)
        except Exception as err:
            gui.MainWindow.raise_error(gui.MainWindow(), 'Ce titre ne renvoie pas de données exploitables. '
                                                         'Essayez un autre titre ou un autre type de recherche.')
        else:
            pretty_response = json.dumps(
                response_xml["srw:searchRetrieveResponse"]["srw:records"]["srw:record"]["srw:recordData"]["oai_dc:dc"],
                sort_keys=True,
                indent=4)
            print(pretty_response)
            with open("data.json", "w") as data:
                data.write(pretty_response)
            with open("data.json") as file:
                file_data = json.load(file)
            self.posts.insert_one(file_data)

    # Functions to find and correct query format.
    def get_author(self, query):
        search = self.test_collection.find({"$text": {"$search": f"{query}"}})
        title_result = search.distinct("oai_dc:dc.dc:creator")
        value_split = title_result[0].split(" ")
        author_ln = value_split[0].strip(',')
        author_fn = value_split[1]
        author_string = f"{author_fn} {author_ln}"
        return author_string

    def get_title(self, query):
        search = self.test_collection.find({"$text": {"$search": f"{query}"}})
        try:
            title_result = search.distinct("oai_dc:dc.dc:title")
            value_book_split = title_result[0].split("/")
        except IndexError:
            return query
        else:
            title = value_book_split[0].strip()
            return title

    # Function to check if ISBN reference is present in collection.
    # If index error, then reference is absent from collection. Otherwise, reference added to collection.
    def get_isbn(self, isbn):
        search = self.test_collection.find({"$text": {"$search": f"{isbn}"}})
        try:
            search.distinct("oai_dc:dc.dc:identifier")[0].replace('ISBN ', '')
        except IndexError:
            return isbn
        else:
            gui.MainWindow.raise_error(gui.MainWindow(), 'Cette référence est déjà présente dans votre collection')
            raise errors.ExistingReference()

    # Creation of new collection in DB.
    def create_collection(self, name: str):
        # First, check if collection already exists in DB.
        try:
            collection_search = self.db.list_collection_names().index(f'{name}')
        # If ValueError is raised, the collection does not exist: create collection.
        except ValueError:
            self.db.create_collection(f'{name}')
        else:
            gui.MainWindow.raise_error(gui.MainWindow(), 'Cette collection existe déjà.')
            raise errors.ExistingCollection()

    # Show all documents in selected collection. Console print at the moment => create data visualization in software.
    # Create a model readable by QTableView in Qt.
    def get_model(self, collection_name: str):
        collection_to_show = self.db[f'{collection_name}']
        collection_cursor = collection_to_show.find()
        df = pandas.DataFrame(data=collection_cursor)
        return df


