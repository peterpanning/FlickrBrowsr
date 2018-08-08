from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy 
from PyQt5.QtCore import *

class Image(QLabel):
    
    borderColorActive = "red"
    borderColorInactive = "grey"
    borderWidth = 4
    styleString = "border: {}px solid {}"
    
    def __init__(self, parent, pixmap, tags = []):
        
        super().__init__(parent)
        
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAlignment(Qt.AlignCenter)
        self.resizeToParent(parent, pixmap)
        self.deactivate()
        self.show()

    def activate(self):
        active = Image.styleString.format(Image.borderWidth, Image.borderColorActive)
        self.setStyleSheet(active)

    def deactivate(self):
        inactive = Image.styleString.format(Image.borderWidth, Image.borderColorInactive)
        self.setStyleSheet(inactive)

    def resizeToParent(self, parent, pixmap):
        
        # Resizing an Image's pixmap scales them based on the larger of their width or height
        pix = pixmap
        layout = parent.layout()
        margins = layout.getContentsMargins() # Is a tuple of (left, top, right, bottom)
        max_images = layout.property("max_images")
        # Each image's new width is a function of the width of its parent widget, 
        # the spacing, maximum number of images, and margins of that widget's layout, 
        # and the width of the image's border. 
        width = ( ( parent.width() - ( layout.spacing() * ( max_images - 1 ) + 
            ( margins[0] * 2 ) ) ) / max_images ) - ( Image.borderWidth * 2 )
        # The height is much simpler in comparison
        height = ( parent.height() - ( margins[1] * 2 ) - ( Image.borderWidth * 2 ) )

        if pix.width() > pix.height():
            pix = pix.scaledToWidth(width)
        else:
            pix = pix.scaledToHeight(height)
        self.setPixmap(pix)
