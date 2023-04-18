
from database import *
import tkinter

db = Database()
# Code d'interface

# Appels de fonction de test

# value = db.test_collection.distinct("oai_dc:dc.dc:creator")
# print(db.get_author(value))

# value_book = db.test_collection.distinct("oai_dc:dc.dc:title")

author_value = input("De quel.le auteur.rice voulez-vous trouver les oeuvres ?")
print(db.get_book(author_value))

book_value = input("De quel livre voulez-vous retrouver l'auteur.rice ?")
print(db.get_author(book_value))