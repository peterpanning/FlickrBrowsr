"""
An class which represents images and their associated metadata as necessary for display within the image browser. 
"""

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy 
# TODO: Isolate necessary dependencies from QtCore
from PyQt5.QtCore import *

class Image(QLabel):
    def __init__(self, parent, image_file = "", tags = []):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        #self.setScaledContents(False)
        self.borderWidthThumbnail = 5
        self.borderWidthZoomed = 10
        self.borderColorActive = "red"
        self.borderColorInactive = "grey"
        self.styleString = "border: {}px solid {}"
        # TODO: Accessors for styles
        self.styleActive = self.styleString.format(self.borderWidthThumbnail, self.borderColorActive)
        self.styleInactive = self.styleString.format(self.borderWidthThumbnail, self.borderColorInactive)
        self.styleZoomed = self.styleString.format(self.borderWidthZoomed, self.borderColorActive)
        
        pix = QPixmap(image_file)
        pix = pix.scaled(default_size[0] - self.borderWidthThumbnail * 2, 
            default_size[1] - self.borderWidthThumbnail * 2, Qt.KeepAspectRatio)
        #pix = pix.scaledToWidth(200)
        #self.setPixmap(pix)
        # TODO: Use QSize for this
        # TODO: Class variable? 
        
        # TODO: Initial location? 
        #self.setPixmap(self.pixmap().scaled(self.default_size[0] - self.borderWidthThumbnail * 2, 
        #    self.default_size[1] - self.borderWidthThumbnail * 2, Qt.KeepAspectRatio))
        self.setPixmap(pix)
        self.setAlignment(Qt.AlignCenter)
        self.deactivate()
        self.show()

    def activate(self):
        self.setStyleSheet(self.styleActive)

    def deactivate(self):
        self.setStyleSheet(self.styleInactive)

    """
    def resize(self, QSize):
        super().resize(QSize)
        self.setPixmap(self.pixmap().scaled(QSize, Qt.KeepAspectRatio))

    def setPixmap(self, pix):
        self.pix = pix
        super().setPixmap(self.scaledPixmap())
    
    def pixmap(self):
        return self.pix

    def heightForWidth(self, width):
        if not self.pixmap():
            return self.height()
        else:
            return ((self.pixmap().height()*width)/self.pixmap().width())

    def sizeHint(self):
        width = self.width()
        return QSize(width, self.heightForWidth(width))

    def scaledPixmap(self):
        return self.pix.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def resizeEvent(self, event):
        if self.pix:
            super().setPixmap(self.scaledPixmap())

    def resize(self, width, height):
        super().resize(width, height)
        self.setPixmap(self.pixmap().scaled(width - self.borderWidthThumbnail * 2, 
            height - self.borderWidthThumbnail * 2, Qt.KeepAspectRatio))
"""

    
