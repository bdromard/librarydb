from PySide6 import QtCore, QtWidgets, QtGui
import sys
import random
import database as db

# Création des widgets à utiliser dans main.py.

# Code de référence du tutorial
# class MyWidget(QtWidgets.QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.hello = ["Bonjour Monde", "Hallo Welt", "Hola Mundo"]
#         self.button = QtWidgets.QPushButton("Click Me!")
#         self.text = QtWidgets.QLabel("Hello World",
#                                      alignment=QtCore.Qt.AlignCenter)
#         self.layout = QtWidgets.QVBoxLayout(self)
#         self.layout.addWidget(self.text)
#         self.layout.addWidget(self.button)
#         self.button.clicked.connect(self.magic)
#
#     @QtCore.Slot()
#     def magic(self):
#         self.text.setText(random.choice(self.hello))

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("LibraryDB")
        self.group_box = QtWidgets.QGroupBox(title="Box pour l'ajout de références bibliographiques")
        self.setCentralWidget(self.group_box)
        self.create_widgets()

    def create_widgets(self):
        # Création des différents widgets utilisables dans la GroupBox
        self.isbn_label = QtWidgets.QLabel("ISBN du livre", self)
        self.isbn_label.setGeometry(10, 30, 100, 30)
        self.title_label = QtWidgets.QLabel("Titre du livre", self)
        self.title_label.setGeometry(10, 70, 100, 30)
        self.add_isbn_btn = QtWidgets.QPushButton("Ajouter ISBN", self)
        self.add_isbn_btn.setGeometry(310, 30, 100, 30)
        self.add_isbn_btn.clicked.connect(self.isbn_button_clicked)
        self.add_title_btn = QtWidgets.QPushButton("Ajouter Titre", self)
        self.add_title_btn.setGeometry(310, 70, 100, 30)
        self.isbn_input = QtWidgets.QLineEdit('Ajout par ISBN du livre', self)
        self.isbn_input.setGeometry(105, 30, 200, 30)
        self.isbn_input.mousePressEvent = self._mousePressEvent_isbn
        self.title_input = QtWidgets.QLineEdit('Ajout par titre du livre', self)
        self.title_input.setGeometry(105, 70, 200, 30)
        self.title_input.mousePressEvent = self._mousePressEvent_title
        # setBuddy permet de focaliser l'input du clavier sur le label choisi.
        self.isbn_label.setBuddy(self.isbn_input)
        self.title_label.setBuddy(self.title_input)

    # Slots qui permettent de clear les inputs dès qu'ils sont cliqués une seule fois. Marche avec tous les inputs
    # d'une souris (clic gauche, clic droit...) ; comme on spécifie que la fonction de base ne retourne rien, la
    # logique fait qu'elle ne fonctionne qu'une seule fois pour avoir un input vide.
    def _mousePressEvent_isbn(self, event):
        self.isbn_input.clear()
        self.isbn_input.mousePressEvent = None

    def _mousePressEvent_title(self, event):
        self.title_input.clear()
        self.title_input.mousePressEvent = None

    def isbn_button_clicked(self):
        isbn = self.isbn_input.text()
        print(isbn)
        db.Database.add_by_isbn(db.Database(), isbn)

    def title_button_clicked(self):
        title = self.title_input.text()
        print(title)
        db.Database.add_by_title(db.Database(), title)






