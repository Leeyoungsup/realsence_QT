import sys 
from PyQt5.QtWidgets import *

from PyQt5 import uic

from_class=uic.loadUiType("./hello_pyqt.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
app=QApplication(sys.argv)
main_dialog=WindowClass()
main_dialog.show()
app.exec_()
