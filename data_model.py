# Following this tutorial to implement data model =>
# https://doc.qt.io/qtforpython-6/tutorials/datavisualize/add_tableview.html
import bnf_database as db
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor

# Model readable by QTableView in gui.py
class CollectionTableModel(QAbstractTableModel):

    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.df = db.Database.get_model(db.Database(), "posts")
        self.titles = self.df['dc:title'].tolist()
        self.authors = self.df['dc:creator'].tolist()
        self.df_data = [self.titles, self.authors]
        self.load_data(data)


    def load_data(self, df_data):
        self.input_titles = self.titles
        self.input_authors = self.authors

        self.column_count = 2
        self.row_count = len(self.input_titles)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return("Titre", "Auteur.ice")[section]
        else:
            return f"{section}"

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 0:
                title = self.input_titles[row]
                return title
            elif column == 1:
                author = self.input_authors[row]
                return author
        elif role == Qt.BackgroundRole:
            return QColor(Qt.black)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None