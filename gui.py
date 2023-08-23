import bnf_database as db
from PySide6.QtWidgets import (
    QMainWindow,
    QGroupBox,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QWidget,
    QTableView,
    QHeaderView,
    QSizePolicy,
    QDialog,
)

from data_model import CollectionTableModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("LibraryDB")
        self.group_box = QGroupBox(title="Ajout de références bibliographiques")
        self.setCentralWidget(self.group_box)
        self.create_labels()
        self.create_inputs()
        self.create_buttons()
        self.set_buddies()

    # Widgets creation, usable in GroupBox.
    def create_labels(self):
        self.isbn_label = QLabel("ISBN du livre", self)
        self.isbn_label.setGeometry(10, 30, 100, 30)
        self.title_label = QLabel("Titre du livre", self)
        self.title_label.setGeometry(10, 70, 100, 30)

    def create_inputs(self):
        self.isbn_input = QLineEdit("Ajout par ISBN du livre", self)
        self.isbn_input.setGeometry(105, 30, 200, 30)
        self.isbn_input.mousePressEvent = self._mousePressEvent_isbn
        self.title_input = QLineEdit("Ajout par titre du livre", self)
        self.title_input.setGeometry(105, 70, 200, 30)
        self.title_input.mousePressEvent = self._mousePressEvent_title
        self.collection_input = QLineEdit("Créer une nouvelle collection", self)
        self.collection_input.setGeometry(10, 110, 210, 30)

    def create_buttons(self):
        self.add_isbn_btn = QPushButton("Ajouter ISBN", self)
        self.add_isbn_btn.setGeometry(310, 30, 100, 30)
        self.add_isbn_btn.clicked.connect(self.isbn_button_clicked)
        self.add_title_btn = QPushButton("Ajouter Titre", self)
        self.add_title_btn.setGeometry(310, 70, 100, 30)
        self.add_title_btn.clicked.connect(self.title_button_clicked)
        self.add_collection_btn = QPushButton("Créer collection", self)
        self.add_collection_btn.setGeometry(225, 110, 185, 30)
        self.add_collection_btn.clicked.connect(self.collection_button_clicked)
        self.show_titles = QPushButton("Montrer oeuvres de la collection", self)
        self.show_titles.setGeometry(10, 150, 225, 30)
        self.show_titles.clicked.connect(self.create_data_table)

    def set_buddies(self):
        # Keyboard focus on selected label.
        self.isbn_label.setBuddy(self.isbn_input)
        self.title_label.setBuddy(self.title_input)

    def create_data_table(self):
        self.data_table = DataTable(self)
        self.data_table.show()

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

    # GUI error and user feedback. Instance creation of MessageBox.
    def raise_error(self, text):
        message = QMessageBox(self, text=text)
        message.exec()


# Creating DataTable class to show data
class DataTable(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)
        self.model = CollectionTableModel(data)
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.horizontal_header = self.table_view.horizontalHeader()
        self.vertical_header = self.table_view.verticalHeader()
        self.horizontal_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.vertical_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontal_header.setStretchLastSection(True)
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size.setHorizontalStretch(1)
        self.main_layout.addWidget(self.table_view)
        self.setLayout(self.main_layout)
