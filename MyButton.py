from PyQt5.QtWidgets import QPushButton, QSizePolicy
#from PyQt5.QtGui import QSizePolicy

class MyButton(QPushButton):
    def __init__(self, text=None, parent=None):
        super().__init__(text, parent)
        self.setFixedWidth(60)