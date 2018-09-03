from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy 
from PyQt5.QtCore import *

class Image(QLabel):

    # TODO: Images do not need QImages, they only need their list of tags

    # TODO: Set initial size and fixed aspect ratio for label, 
    # resize pixmap within those dimensions?

    borderColorActive = "red"
    borderColorInactive = "grey"
    styleString = "border: {}px solid {}"
    # TODO: Parameter order should match QLabel parameter order
    def __init__(self, parent=None, pixmap=None):
        
        super().__init__(parent)
        # TODO: QLabels have a pixmap() function, is this really necessary?
        self.pixmap = pixmap
        self.setFocusPolicy(Qt.NoFocus)
        self.setAlignment(Qt.AlignCenter)
        self.borderWidth = 3
        self.tags = []
        self.deactivate()
        self.show()

    # TODO: Most recent ideation of tags does not use this implementation.

    # Images can have tags as part of their metadata. Interacting with these tags occurs through CRUD operations. 

    def readTags(self):
        pass
    
    def updateTags(self):
        pass

    def deleteTags(self):
        pass

    def createTags(self):
        pass

    def activate(self):
        active = Image.styleString.format(self.borderWidth, Image.borderColorActive)
        self.setStyleSheet(active)

    def deactivate(self):
        inactive = Image.styleString.format(self.borderWidth, Image.borderColorInactive)
        self.setStyleSheet(inactive)

class Thumbnail(Image):
    def __init__(self, parent, pixmap):
        super().__init__(parent, pixmap)
        self.resizeToParent()
    def resizeToParent(self):
        
        # Resizing an Image's pixmap scales them based on the larger of their width or height
        parent = self.parent()
        layout = parent.layout()
        margins = layout.getContentsMargins() # Is a tuple of (left, top, right, bottom)
        # TODO: Rename max_thumbnails prop to max_images and add to zoomed layout
        max_thumbnails = layout.property("max_thumbnails")
        if not max_thumbnails:
            max_thumbnails = 1
            
        # Each image's new width is a function of the width of its parent widget, 
        # the spacing, maximum number of images, and margins of that widget's layout, 
        # and the width of the image's border. 

        width = ( ( parent.width() - ( layout.spacing() * ( max_thumbnails - 1 ) + 
            ( margins[0] * 2 ) ) ) / max_thumbnails ) - ( self.borderWidth * 2 )
        # The height is much simpler in comparison
        height = ( parent.height() - ( margins[1] * 2 ) - ( self.borderWidth * 2 ) )

        if self.pixmap.height() > self.pixmap.width():
            self.pixmap = self.pixmap.scaledToHeight(height)
        elif self.pixmap.width() > self.pixmap.height():
            self.pixmap = self.pixmap.scaledToWidth(width)
        else:
            lesser = min(width, height)
            self.pixmap = self.pixmap.scaled(lesser, lesser, Qt.KeepAspectRatio)
        self.setPixmap(self.pixmap)
        
class ZoomedImage(Image):
    def __init__(self, parent, pixmap):
        super().__init__(parent, pixmap) 
        self.borderWidth = 10
        self.resizeToParent()
    
    def resizeToParent(self):
        # Resizing an Image's pixmap scales them based on the larger of their width or height
        
        margins = self.parent().layout().getContentsMargins() # A tuple of [left, top, right, bottom]
        width = self.parent().width() - (self.borderWidth * 2) - (margins[0] * 2)
        height = self.parent().height() - (self.borderWidth * 2) - (margins[1] * 2)

        if self.pixmap.height() > self.pixmap.width():
            self.pixmap = self.pixmap.scaledToHeight(height)
        elif self.pixmap.width() > self.pixmap.height():
            self.pixmap = self.pixmap.scaledToWidth(width)
        else:
            lesser = min(width, height)
            self.pixmap = self.pixmap.scaled(lesser, lesser, Qt.KeepAspectRatio)
        self.setPixmap(self.pixmap)