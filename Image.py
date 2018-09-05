from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy
from PyQt5.QtCore import *

# TODO: Is our Image class a QLabel which has a QImage, pixmap, and file path, 
# or a QWidget which has a QImage, QPixmap, and file path? How easy would this
# be to change? 

class Image(QLabel):

    # TODO: Set initial size and fixed aspect ratio for label, 
    # resize pixmap within those dimensions?

    borderColorActive = "red"
    borderColorInactive = "grey"
    styleString = "border: {}px solid {}"

    def __init__(self, parent=None, image_file_path=None):
        
        super().__init__(parent)
        self.file_path = image_file_path
        self.qimage = QImage(self.file_path)
        self.setPixmap(QPixmap(self.file_path))
        self.setFocusPolicy(Qt.NoFocus)
        self.setAlignment(Qt.AlignCenter)
        self.borderWidth = 3
        self.deactivate()
        self.hide()

    # Images can have tags as part of their metadata

    def readTags(self):
        # Returns tags as a list of strings
        return self.qimage.text("PyQtBrowserTags").split(", ")
    
    def saveAllTags(self, tags):
        t = ""
        for tag in tags:
            t = t + tag + ", "
            self.qimage.setText("PyQtBrowserTags", t)
        self.qimage.save(self.file_path)

    def deleteTags(self):
        pass

    def activate(self):
        active = Image.styleString.format(self.borderWidth, Image.borderColorActive)
        self.setStyleSheet(active)

    def deactivate(self):
        inactive = Image.styleString.format(self.borderWidth, Image.borderColorInactive)
        self.setStyleSheet(inactive)

class Thumbnail(Image):
    def __init__(self, parent, image):
        
        # Weird thing: Because we're initializing Images with file paths,
        # We now need to get that path from any Image we pass in to create
        # subclasses. We could fix this by checking Image's class
        
        super().__init__(parent, image.file_path)
        self.resizeToParent()
        self.show()

    def resizeToParent(self):
                
        parent = self.parent()
        layout = parent.layout()
        margins = layout.getContentsMargins() # Is a tuple of (left, top, right, bottom)
        max_thumbnails = layout.property("max_thumbnails")
        if not max_thumbnails:
            max_thumbnails = 1
            
        # A Thumbnail's new width is a function of its parent widget's width, 
        # spacing, maximum number of thumbnails and layout margins, 
        # and the width of the thumbnail's border. 

        width = ( ( parent.width() - ( layout.spacing() * ( max_thumbnails - 1 ) + 
            ( margins[0] * 2 ) ) ) / max_thumbnails ) - ( self.borderWidth * 2 )
        
        # The new height is much easier to calculate
        height = ( parent.height() - ( margins[1] * 2 ) - ( self.borderWidth * 2 ) )

        # Which dimension we scale to depends on which was larger in the original pixmap

        if self.pixmap().height() > self.pixmap().width():
            self.setPixmap(self.pixmap().scaledToHeight(height))
        elif self.pixmap().width() > self.pixmap().height():
            self.setPixmap(self.pixmap().scaledToWidth(width))
        else:
            lesser = min(width, height)
            self.setPixmap(self.pixmap().scaled(lesser, lesser, Qt.KeepAspectRatio))
        
class ZoomedImage(Image):
    def __init__(self, parent, image):
        super().__init__(parent, image.file_path) 
        self.borderWidth = 10
        self.resizeToParent()
        self.show()
    
    def resizeToParent(self):
        
        margins = self.parent().layout().getContentsMargins() # A tuple of [left, top, right, bottom]
        width = self.parent().width() - (self.borderWidth * 2) - (margins[0] * 2)
        height = self.parent().height() - (self.borderWidth * 2) - (margins[1] * 2)

        # Resizing an ZoomedImage's pixmap scales it based on the larger of its width or height

        if self.pixmap().height() > self.pixmap().width():
            self.setPixmap(self.pixmap().scaledToHeight(height))
        elif self.pixmap().width() > self.pixmap().height():
            self.setPixmap(self.pixmap().scaledToWidth(width))
        else:
            lesser = min(width, height)
            self.setPixmap(self.pixmap().scaled(lesser, lesser, Qt.KeepAspectRatio))