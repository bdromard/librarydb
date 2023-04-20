from PySide6 import QtCore, QtWidgets, QtGui
import sys
import random

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
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("LibraryDB")
        self.group_box = QtWidgets.QGroupBox(title="Box pour l'ajout de références bibliographiques")
        self.setCentralWidget(self.group_box)
        self.isbn_label = QtWidgets.QLabel(text="ISBN du livre")
        self.title_label = QtWidgets.QLabel(text="Titre du livre")
        self.isbn_input = QtWidgets.QLineEdit(placeholderText="Ajout par ISBN du livre")
        self.title_input = QtWidgets.QLineEdit(placeholderText="Ajout par titre du livre")





