from database import *
# from gui import *
import sys
import random
import pymongo
from PySide6 import QtCore, QtWidgets, QtGui


db = Database()
# app = QtWidgets.QApplication([])
# widget = MyWidget()
# widget.resize(800, 600)
# widget.show()
# sys.exit(app.exec())

# Code d'interface

@QtCore.Slot()
def print_isbn():
    print("978200015312")

# Initialisation de l'application, avec un bouton qui appelle la fonction print_isbn, pour voir l'ISBN dans la console.
app = QtWidgets.QApplication(sys.argv)
button = QtWidgets.QPushButton("Print ISBN")
button.clicked.connect(print_isbn)
button.show()
app.exec()
# Appels de fonction de test

# value = db.test_collection.distinct("oai_dc:dc.dc:creator")
# print(db.get_author(value))

# value_book = db.test_collection.distinct("oai_dc:dc.dc:title")

# author_value = input("De quel.le auteur.rice voulez-vous trouver les oeuvres ?")
# print(db.get_book(author_value))
#
# book_value = input("De quel livre voulez-vous retrouver l'auteur.rice ?")
# print(db.get_author(book_value))

# new_user_collection = input("Donnez un nom à votre nouvelle bibliothèque: ")
# db.db["test2"].insert_one({'testKey': 'testValue'})

# print(db.show_collection("testCollection"))