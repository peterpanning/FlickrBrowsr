from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QSizePolicy
from PyQt5.QtCore import *
from Image import Image


class ThumbnailWidget(QWidget):
    # TODO: This class may as well be called a ThumbnailScreen, because it represents everything
    # visible in the ImageBrowser window when viewing images as thumbnails. 
    # TODO: There are some functions and attributes I would like to use 
    # which must be implemented in subclasses i.e. count
    # TODO: Variable initialization of number of thumbnails
    # Activate sets the stylesheet for the Image, and is not related to the Qt activat() function
    # TODO: Command to set stylesheet which doesn't overlap with existing Qt function names
    def __init__(self, parent):
        # TODO: Split init function into multiple functions
        super().__init__()
        self.setFocusPolicy(Qt.NoFocus)
        # This widget has a QHBoxLayout which allows us to add widgets to the screen. 
        # This layout, at the moment, fills the entire screen. 
        main_layout = QHBoxLayout()

        # We then create a container for the thumbnail images we will later navigate through,
        # which allows us to constrain the size of their QHBoxLayout (otherwise impossible).
        thumbnail_container = QWidget()
        thumbnail_container.move(0, parent.height()/3)
        thumbnail_container.setMaximumHeight(parent.height()/3)
        thumbnail_container.setMaximumWidth(parent.width())
        # We will be viewing multiple ImageLabels in a horizontal row, 
        # and so will use a QHBoxLayout class which seems to be designed 
        # explicitly for this purpose. 
        thumbnails = QHBoxLayout()
        thumbnails.setProperty("max_images", 5)
        thumbnail_container.setLayout(thumbnails)

        #### Move this

        for i in range(0, thumbnails.property("max_images")):
            thumbnail = Image(thumbnail_container, parent.pixmaps[i])
            thumbnails.addWidget(thumbnail)
        # itemAt() returns a WidgetItem, widget() returns the widget that item manages
        # TODO: Command to set stylesheet which doesn't overlap with existing Qt function names

        thumbnails.itemAt(0).widget().activate()

        main_layout.addWidget(thumbnail_container)
        self.setLayout(main_layout)

    def focusOn(self, focusedImage):
        self.layout().itemAt(0).widget().layout().itemAt(focusedImage).widget().setFocus()

    
class ZoomedWidget(QWidget):
    # TODO: Rewrite this as a QStackedWidget which has a different fullscreen 
    # child widget for each image, allowing us to use the builtin
    # focusPreviousChild behavior to change widgets? 
    # Zoomed widget also uses a QHBoxLayout, but has no widgets when we 
    # initialize it. This is because widgets can only exist in one layout
    # at a time. Switching between widgets(and therefore layouts) later 
    # moves the focused Image between widgets as necessary.
    def __init__(self, parent):
        super().__init__()
        self.setFocusPolicy(Qt.NoFocus)
        zoomedLayout = QHBoxLayout()
        self.setLayout(zoomedLayout)
        zoomedLayout.setProperty("max_images", 1)