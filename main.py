from gui import *
import sys
from PySide6 import QtWidgets


app = QtWidgets.QApplication([])
widget = MainWindow()
widget.show()
sys.exit(app.exec())



