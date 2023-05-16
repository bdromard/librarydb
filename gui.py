from PySide6 import QtCore, QtWidgets, QtGui
import sys
import random
import pandas

import database as db

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("LibraryDB")
        self.group_box = QtWidgets.QGroupBox(title="Box pour l'ajout de références bibliographiques")
        self.setCentralWidget(self.group_box)
        self.create_labels()
        self.create_inputs()
        self.create_buttons()
        self.set_buddies()

    # Widgets creation, usable in GroupBox.
    def create_labels(self):
        self.isbn_label = QtWidgets.QLabel("ISBN du livre", self)
        self.isbn_label.setGeometry(10, 30, 100, 30)
        self.title_label = QtWidgets.QLabel("Titre du livre", self)
        self.title_label.setGeometry(10, 70, 100, 30)

    def create_inputs(self):
        self.isbn_input = QtWidgets.QLineEdit('Ajout par ISBN du livre', self)
        self.isbn_input.setGeometry(105, 30, 200, 30)
        self.isbn_input.mousePressEvent = self._mousePressEvent_isbn
        self.title_input = QtWidgets.QLineEdit('Ajout par titre du livre', self)
        self.title_input.setGeometry(105, 70, 200, 30)
        self.title_input.mousePressEvent = self._mousePressEvent_title
        self.collection_input = QtWidgets.QLineEdit('Créer une nouvelle collection', self)
        self.collection_input.setGeometry(10, 110, 210, 30)
    def create_buttons(self):
        self.add_isbn_btn = QtWidgets.QPushButton("Ajouter ISBN", self)
        self.add_isbn_btn.setGeometry(310, 30, 100, 30)
        self.add_isbn_btn.clicked.connect(self.isbn_button_clicked)
        self.add_title_btn = QtWidgets.QPushButton("Ajouter Titre", self)
        self.add_title_btn.setGeometry(310, 70, 100, 30)
        self.add_title_btn.clicked.connect(self.title_button_clicked)
        self.add_collection_btn = QtWidgets.QPushButton("Créer collection", self)
        self.add_collection_btn.setGeometry(225, 110, 185, 30)
        self.add_collection_btn.clicked.connect(self.collection_button_clicked)
        self.show_titles = QtWidgets.QPushButton("Montrer oeuvres de la collection", self)
        self.show_titles.setGeometry(10, 150, 225, 30)
        self.show_titles.clicked.connect(self.create_data_table)

    def set_buddies(self):
        # Keyboard focus on selected label.
        self.isbn_label.setBuddy(self.isbn_input)
        self.title_label.setBuddy(self.title_input)

    def create_data_table(self):
        collection = db.Database.get_all_collection(db.Database(), 'testCollection')
        # title = db.Database.get_title(db.Database(), "Le port intérieur")
        data_box = QtWidgets.QDialog(self)
        data_box.setGeometry(70, 70, 500, 500)
        data_box.setWindowTitle("Votre collection")
        # Using fixed row and column count but will need to adapt to collection size
        # data_table = QtWidgets.QTableWidget(len(list(collection)), 3, data_box)
        data_table = QtWidgets.QTableView(data_box)
        data_table.setGeometry(50, 50, 400, 400)
        data_frame = pandas.DataFrame(list(collection.find()))
        model = QtCore.QAbstractTableModel(data_frame)
        data_table.setModel(model)
        # data_table.setHorizontalHeaderLabels(["Titre", "Auteur.ice", "ISBN"])
        # for document in collection:
        #     print('coucou')
        #     data_table.setItem(0, 0, QtWidgets.QTableWidgetItem(document.get('dc:title')))
        data_box.show()


    # Slots to clear input when clicked once. Works with every mouse input. Primary function does not return anything,
    # which allows it to work only once.
    def _mousePressEvent_isbn(self, event):
        self.isbn_input.clear()
        self.isbn_input.mousePressEvent = None

    def _mousePressEvent_title(self, event):
        self.title_input.clear()
        self.title_input.mousePressEvent = None

    # Slots to connect to specified buttons.
    def isbn_button_clicked(self):
        isbn = self.isbn_input.text()
        db.Database.add_by_isbn(db.Database(), isbn)

    def title_button_clicked(self):
        title = self.title_input.text()
        db.Database.add_by_title(db.Database(), title)

    def collection_button_clicked(self):
        new_collection = self.collection_input.text()
        print(new_collection)
        db.Database.create_collection(db.Database(), new_collection)

    def show_titles_clicked(self):
        db.Database.show_all_collection(db.Database(), 'testCollection')

    # GUI error and user feedback. Instance creation of MessageBox.
    def raise_error(self, text):
        message = QtWidgets.QMessageBox(self, text=text)
        message.exec()









