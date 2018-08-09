from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QSizePolicy
from PyQt5.QtCore import *
from Image import Image


class ThumbnailWidget(QWidget):

    # Activate sets the stylesheet for the Image, and is not related to the Qt activate() function
    # TODO: Command to set stylesheet which doesn't overlap with existing Qt function names

    def __init__(self, parent):
        # TODO: Split init function into multiple functions
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.selected_image_index = 0
        self.selected_thumbnail = 0

        main_layout = QHBoxLayout()

        # Create a container for the thumbnail images to constrain the height 
        # of the layout
        thumbnail_container = QWidget()
        thumbnail_container.move(0, parent.height()/3)
        thumbnail_container.setMaximumHeight(parent.height()/3)
        thumbnail_container.setMaximumWidth(parent.width())
        thumbnail_container.setLayout(QHBoxLayout())
        thumbnail_container.layout().setProperty("max_thumbnails", 5)

        main_layout.addWidget(thumbnail_container)
        self.setLayout(main_layout)

        for i in range(0, thumbnail_container.layout().property("max_thumbnails")):
            self.addImage(parent.pixmaps[i])

        # itemAt() returns a WidgetItem, widget() returns the widget that item manages
        # TODO: Command to set stylesheet which doesn't overlap with existing Qt function names

        self.currentImage().activate()

    def currentImage(self):
        return self.thumbnail_layout().itemAt(self.selected_image_index).widget()

    def thumbnail_container(self):
        return self.layout().itemAt(0).widget()

    def thumbnail_layout(self):
        return self.thumbnail_container().layout()

    def addImage(self, pixmap):
        thumbnail = Image(self.thumbnail_container(), pixmap)
        self.thumbnail_layout().addWidget(thumbnail)

    def selectNextImage(self):
        return
    def selectPreviousImage(self):
        return
    def nextPage(self):
        return 
    def previousPage(self):
        return

    # TODO: setImage function similar to that in ZoomedWidget



    
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
        self.selected_image_index = 0
        self.setFocusPolicy(Qt.StrongFocus)
        zoomedLayout = QHBoxLayout()
        self.setLayout(zoomedLayout)

    def setImage(self, pixmap):
        old_image = self.layout().takeAt(0)
        if old_image:
            old_image.widget().deleteLater()
        # TODO: Weird bug with zooming, doesn't zoom to truly full window on the first zoom
        # Might have to do with the way the widget is initialized? 
        zoomed_image = Image(self, pixmap)
        # Have to add the image to the widget's layout, not just the widget
        self.layout().addWidget(zoomed_image)
        self.layout().itemAt(0).widget().setFocus()

    def currentImage(self):
        return self.layout().itemAt(0).widget()

    def setSelectedImageIndex(self, new_index):
        self.selected_image_index = new_index

    def selectNextImage(self):
        return
    def selectPreviousImage(self):
        return