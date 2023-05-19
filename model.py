# Following this tutorial to implement data model =>
# https://doc.qt.io/qtforpython-6/tutorials/datavisualize/add_tableview.html

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor

class CollectionTableModel(QAbstractTableModel):

    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.load_data(data)

    def load_data(self, data):
        self.input_titles = data[0].values
        self.input_authors = data[1].values
        self.input_isbn = data[2].values

        self.column_count = 3
        self.row_count = 3

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return("Title", "Author", "ISBN")[section]
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
            elif column == 2:
                isbn = self.input_isbn[row]
                return isbn
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None