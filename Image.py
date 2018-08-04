"""
An class which represents images and their associated metadata as necessary for display within the image browser. 
"""

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QSizePolicy 
# TODO: Isolate necessary dependencies from QtCore
from PyQt5.QtCore import *

class Image(QLabel):
    borderColorActive = "red"
    borderColorInactive = "grey"
    styleString = "border: {}px solid {}"
    def __init__(self, parent, pixmap, tags = []):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.borderWidth = 5
        
        # TODO: Accessors for styles
        self.styleActive = self.styleString.format(self.borderWidth, Image.borderColorActive)
        self.styleInactive = self.styleString.format(self.borderWidth, Image.borderColorInactive)
        pix = pixmap

        layout = parent.layout()
        margins = layout.getContentsMargins() # Is a tuple of (left, top, right, bottom)
        max_images = layout.property("max_images")
        if pix.width() > pix.height():
            # Bizarrely, an image's final width can be calculated using only the parent's width,
            # number of images displayed and the spacing between them, without concern for
            # margins or content padding.
            pix = pix.scaledToWidth( 
                ( parent.width() / max_images ) - ((max_images - 1) * layout.spacing())
                )
        else:
            # Final height, on the other hand, needs to know the margins above them. 
            # Because of course it does. 
            pix = pix.scaledToHeight(parent.height() - (margins[1] * 2)) 
        self.deactivate()
        self.show()

        self.setPixmap(pix)
        self.setAlignment(Qt.AlignCenter)

    def styleActive(self):
        return self.styleString.format(self.borderWidth, Image.borderColorActive)

    def styleActive(self):
        return self.styleString.format(self.borderWidth, Image.borderColorInactive)

    def activate(self):
        self.setStyleSheet(self.styleActive)

    def deactivate(self):
        self.setStyleSheet(self.styleInactive)