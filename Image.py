from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy
from PyQt5.QtCore import *
import os

# TODO: Is our Image class a QLabel which has a QImage, pixmap, and file path, 
# or a QWidget which has a QImage, QPixmap, and file path? How easy would this
# be to change? 

class Image(QLabel):

    # TODO: Set initial size and fixed aspect ratio for label, 
    # resize pixmap within those dimensions?

    borderColorActive = "red"
    borderColorInactive = "grey"
    styleString = "border: {}px solid {}"

    def __init__(self, parent=None, image_file_path=None, image_data=None):
        
        super().__init__(parent)

        if image_file_path:
            self.file_path = image_file_path
        
        if image_data == None:
            if image_file_path:
                self.qimage = QImage(self.file_path)
                self.setPixmap(QPixmap(self.file_path))
        else:
            self.qimage = QImage()
            self.qimage.loadFromData(image_data)
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.setPixmap(pixmap)

        self.setFocusPolicy(Qt.NoFocus)
        self.setAlignment(Qt.AlignCenter)
        self.borderWidth = 3
        self.deactivate()
        self.hide()

    # Images can have tags as part of their metadata

    def activate(self):
        active = Image.styleString.format(self.borderWidth, Image.borderColorActive)
        self.setStyleSheet(active)

    def addTag(self, tag):
        old_tags = self.qimage.text("PyQtBrowserTags")
        if old_tags:
            new_tags = old_tags + ", " + tag
            self.qimage.setText("PyQtBrowserTags", new_tags)
        else:
            self.qimage.setText("PyQtBrowserTags", tag)

    def deactivate(self):
        inactive = Image.styleString.format(self.borderWidth, Image.borderColorInactive)
        self.setStyleSheet(inactive)

    def delete(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def readTags(self):
        # Returns tags as a list of strings
        return self.qimage.text("PyQtBrowserTags").split(", ")
    
    def saveTags(self):
        if self.qimage.text("PyQtBrowserTags"):
            self.qimage.save(self.file_path) 

    def save(self):
        self.qimage.save(self.file_path)


class Thumbnail(Image):

    def __init__(self, parent, image, num_thumbs=1):
        
        super().__init__(parent)
        self.file_path = image.file_path
        self.qimage = image.qimage
        self.setPixmap(image.pixmap())
        self.resizeToParent(num_thumbs)
        self.show()

    def resizeToParent(self, num_thumbs=1):

        width = (self.parent().width() / num_thumbs) - (self.borderWidth * 2)
        height = self.parent().height() - ( self.borderWidth * 2 )

        # Which dimension we scale to depends on the smaller dimension of the new label

        if width < height:
            self.setPixmap(self.pixmap().scaledToWidth(width))
        elif height < width:
            self.setPixmap(self.pixmap().scaledToHeight(height))
        else:
            self.setPixmap(self.pixmap().scaled(width, height, Qt.KeepAspectRatio))
        
class ZoomedImage(Image):
    def __init__(self, parent, image):
        super().__init__(parent) 
        self.file_path = image.file_path
        self.qimage = image.qimage
        self.setPixmap(image.pixmap())
        self.borderWidth = 10
        self.resizeToParent()
        self.show()
    
    def resizeToParent(self):
        
        margins = self.parent().layout().getContentsMargins() # A tuple of [left, top, right, bottom]
        width = self.parent().width() - (self.borderWidth * 2) - (margins[0] * 2)
        height = self.parent().height() - (self.borderWidth * 2) - (margins[1] * 2)

        # ZoomedImages are always just scaled to the new label's width & height

        self.setPixmap(self.pixmap().scaled(width, height, Qt.KeepAspectRatio))