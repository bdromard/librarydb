from database import *
from gui import *
import sys
import random
import pymongo
# from PySide6 import QtCore, QtWidgets, QtGui


db = Database()
app = QtWidgets.QApplication([])
widget = MainWindow()
widget.show()
sys.exit(app.exec())

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

# db.get_title('9782707321213')


