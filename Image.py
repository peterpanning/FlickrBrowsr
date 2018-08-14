from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy 
from PyQt5.QtCore import *

class Image(QLabel):

    # TODO: Subclass into Thumbnails and ZoomedImages
    
    borderColorActive = "red"
    borderColorInactive = "grey"
    borderWidth = 4
    styleString = "border: {}px solid {}"
    
    def __init__(self, parent, pixmap, tags = []):
        
        super().__init__(parent)
        self.pixmap = pixmap
        self.setFocusPolicy(Qt.NoFocus)
        self.setAlignment(Qt.AlignCenter)
        self.resizeToParent()
        self.deactivate()
        self.show()

    def activate(self):
        active = Image.styleString.format(Image.borderWidth, Image.borderColorActive)
        self.setStyleSheet(active)

    def deactivate(self):
        inactive = Image.styleString.format(Image.borderWidth, Image.borderColorInactive)
        self.setStyleSheet(inactive)
    
    # TODO: Call this function whenever layout might change, i.e. when loading thumbnails
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
            ( margins[0] * 2 ) ) ) / max_thumbnails ) - ( Image.borderWidth * 2 )
        # The height is much simpler in comparison
        height = ( parent.height() - ( margins[1] * 2 ) - ( Image.borderWidth * 2 ) )

        if self.pixmap.height() > self.pixmap.width():
            self.pixmap = self.pixmap.scaledToHeight(height)
        elif self.pixmap.width() > self.pixmap.height():
            self.pixmap = self.pixmap.scaledToWidth(width)
        else:
            lesser = min(width, height)
            self.pixmap = self.pixmap.scaled(lesser, lesser, Qt.KeepAspectRatio)
        self.setPixmap(self.pixmap)
