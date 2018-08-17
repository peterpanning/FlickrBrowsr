from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QSizePolicy
from PyQt5.QtCore import *
from Image import Image, Thumbnail, ZoomedImage


class ThumbnailWidget(QWidget):

    # Activate sets the stylesheet for the Image, and is not related to the Qt activate() function
    # TODO: Command to set stylesheet which doesn't overlap with existing Qt function names

    # TODO: Should have a list of Images in order to more easily manipulate them

    def __init__(self, parent):
        # TODO: Split init function into multiple functions
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setGeometry(parent.geometry())
        self.selected_image_index = 0
        self.selected_thumbnail = 0
        # Pixmaps are for offscreen processing anyways, copying them here shouldn't make a huge
        # difference and allows us to create new Images lazily 
        self.pixmaps = parent.pixmaps  

        main_layout = QHBoxLayout()

        # Create a container for the thumbnail images to constrain the height 
        # of the layout
        thumbnail_container = QWidget(self)
        thumbnail_container.setGeometry(0, parent.height()/3, parent.width(), parent.height()/3)
        thumbnail_container.setMaximumHeight(parent.height()/3)
        thumbnail_container.setMaximumWidth(parent.width())
        thumbnail_container.setLayout(QHBoxLayout())
        # TODO: Set this with a global variable/read from file?
        thumbnail_container.layout().setProperty("max_thumbnails", 5)

        main_layout.addWidget(thumbnail_container)
        self.setLayout(main_layout)

        for i in range(0, thumbnail_container.layout().property("max_thumbnails")):
            self.addImage(self.pixmaps[i])

        # itemAt() returns a LayoutItem, widget() returns the widget that item manages
        self.currentImage().activate()

    def currentImage(self):
        # TODO: Change this to return the selected thumbnail
        return self.thumbnail_layout().itemAt(self.selected_thumbnail).widget()

    def thumbnail_container(self):
        return self.layout().itemAt(0).widget()

    def thumbnail_layout(self):
        return self.thumbnail_container().layout()

    def addImage(self, pixmap):
        thumbnail = Thumbnail(self.thumbnail_container(), pixmap)
        self.thumbnail_layout().addWidget(thumbnail)

    def selectNextImage(self):
        if self.selected_thumbnail == 4:
            self.selected_thumbnail = 0
            self.loadThumbnails()
        else:
            self.currentImage().deactivate()
            self.selected_thumbnail += 1
        self.currentImage().activate()
    
    def selectPreviousImage(self):
        if self.selected_thumbnail == 0:
            self.selected_thumbnail = 4
            self.loadThumbnails()
        else:
            self.currentImage().deactivate()
            self.selected_thumbnail -= 1
        self.currentImage().activate()
        
    def nextPage(self):
        self.loadThumbnails() 
    def previousPage(self):
        self.loadThumbnails()

    def loadThumbnails(self):
        # load pixmaps around selected thumbnail
        first_index = self.selected_image_index - self.selected_thumbnail
        last_index = self.selected_image_index + (self.thumbnail_layout().property("max_thumbnails") - self.selected_thumbnail)
        for i in range(0, self.thumbnail_layout().property("max_thumbnails")):
            old_image = self.thumbnail_layout().takeAt(0)
            if old_image:
                old_image.widget().deleteLater()
        for i in range(first_index, last_index):
            try:
                self.addImage(self.pixmaps[i])
            except IndexError:
                self.addImage(self.pixmaps[i - len(self.pixmaps)])
        self.currentImage().activate()

    def setSelectedImageIndex(self, index):
        self.selected_image_index = index

    
class TaggingWidget(QWidget):
    def __init__(self, parent):
        super().init(parent)

class ZoomedWidget(QWidget):
    # TODO: Rewrite this as a QStackedWidget which has a different fullscreen 
    # child widget for each image, allowing us to use the builtin
    # focusPreviousChild behavior to change widgets? 

    # Zoomed widget also uses a QHBoxLayout, but has no widgets when we 
    # initialize it. This is because widgets can only exist in one layout
    # at a time. Switching between widgets(and therefore layouts) later 
    # moves the focused Image between widgets as necessary.

    def __init__(self, parent):
        super().__init__(parent)
        self.selected_image_index = 0
        self.setFocusPolicy(Qt.StrongFocus)
        self.setGeometry(parent.geometry())
        zoomedLayout = QGridLayout()
        self.setLayout(zoomedLayout)
        self.pixmaps = parent.pixmaps
        self.setMaximumSize(parent.width(), parent.height())
        self.setImage(self.pixmaps[0])

    def setImage(self, pixmap):
        old_image = self.layout().takeAt(0)
        if old_image:
            old_image.widget().deleteLater()
        zoomed_image = ZoomedImage(self, pixmap)
        # Have to add the image to the widget's layout, not just the widget
        self.layout().addWidget(zoomed_image)
        self.layout().itemAt(0).widget().activate()

    def currentImage(self):
        return self.layout().itemAt(0).widget()

    def setSelectedImageIndex(self, index):
        self.selected_image_index = index

    def selectNextImage(self):
        self.setImage(self.pixmaps[self.selected_image_index])
    def selectPreviousImage(self):
        self.setImage(self.pixmaps[self.selected_image_index])