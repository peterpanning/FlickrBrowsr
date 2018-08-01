"""
An class which represents images and their associated metadata as necessary for display within the image browser. 
"""

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget 
# TODO: Isolate necessary dependencies from QtCore
from PyQt5.QtCore import *

class Image(QLabel):
    def __init__(self, parent, image_file = "", tags = []):
        super().__init__(parent )
        self.setParent(parent)
        self.active = False
        self.zoomed = False
        self.setPixmap(QPixmap(image_file))
        self.tags = tags # Will be a list
        self.borderWidthThumbnail = 5
        self.borderWidthZoomed = 10
        self.borderColorActive = "yellow"
        self.borderColorInactive = "grey"
        self.styleActive = "border: {}px solid {}".format(self.borderWidthThumbnail, self.borderColorActive)
        self.styleInactive = "border: {}px solid {}".format(self.borderWidthThumbnail, self.borderColorInactive)
        self.styleZoomed = "border: {}px solid {}".format(self.borderWidthZoomed, self.borderColorActive)
        self.locX = self.x()
        self.locY = self.y()
        # TODO: Use QSize for this
        # TODO: Class variable? 
        self.default_size = (parent.width/5, parent.height/4)
        # TODO: Initial location? 
        self.setPixmap(self.pixmap().scaled(self.default_size[0] - self.borderWidthThumbnail - 2, 
            self.default_size[1] - self.borderWidthThumbnail - 2, Qt.KeepAspectRatio))
        self.setAlignment(Qt.AlignCenter)
        self.deactivate()
        self.show()

    def add_tag(self, tag):
        self.tags.append(tag)

    def resize(self, width, height):
        super().resize(width, height)
        self.setPixmap(self.pixmap().scaled(width, height, Qt.KeepAspectRatio))

    def setGeometry(self, x, y, width, height):
        super().setGeometry(x, y, width, height)
        self.setPixmap(self.pixmap().scaled(width, height, Qt.KeepAspectRatio))

    def activate(self):
        self.setStyleSheet(self.styleActive)

    def deactivate(self):
        self.setStyleSheet(self.styleInactive)

    def zoomIn(self):
        self.locX = self.x()
        self.locY = self.y()
        self.setGeometry(0, 0, self.parent().width, self.parent().height)
        self.setStyleSheet(self.styleZoomed)
        self.zoomed = True

    def zoomOut(self):
        self.setGeometry(self.locX, self.locY, self.default_size[0], self.default_size[1])
        self.setStyleSheet(self.styleActive)
        self.zoomed = False