from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QSizePolicy, QVBoxLayout, QLineEdit, QLabel, QPushButton
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
        self.selected_thumbnail = 0
        self.images = parent.images

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
            # TODO: List of images as initialization parameter? 
            self.addImage(self.images[i])

        self.currentImage().activate()

    def currentImage(self):
        # TODO: Change this to return the selected thumbnail
        # itemAt() returns a LayoutItem, widget() returns the widget that item manages
        return self.thumbnail_layout().itemAt(self.selected_thumbnail).widget()

    def thumbnail_container(self):
        return self.layout().itemAt(0).widget()

    def thumbnail_layout(self):
        return self.thumbnail_container().layout()

    def addImage(self, image):
        thumbnail = Thumbnail(self.thumbnail_container(), image)
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
        first_index = self.parent().selected_image_index - self.selected_thumbnail
        last_index = self.parent().selected_image_index + (self.thumbnail_layout().property("max_thumbnails") - self.selected_thumbnail)
        for i in range(0, self.thumbnail_layout().property("max_thumbnails")):
            old_image = self.thumbnail_layout().takeAt(0)
            if old_image:
                old_image.widget().deleteLater()
        for i in range(first_index, last_index):
            try:
                self.addImage(self.images[i])
            except IndexError:
                self.addImage(self.images[i - len(self.images)])
        self.currentImage().activate()

    def setSelectedImageIndex(self, index):
        self.selected_image_index = index

class TagListWidget(QWidget):
    # TagLists are widgets which display all of the tags a user has added to an Image. 
    def __init__(self, parent, tags=None):
        
        # Parent is a QWidget
        # tags is a list of strings which describe an associated image. 

        super().__init__(parent)
        self.setFixedWidth(parent.width()/4)
        # TODO: Alignment

        # Widget needs a layout to be able to contain tags
        self.setLayout(QVBoxLayout())
        # Need a container to restrict the size of the tag layout (layouts don't have width)
        tag_container = QWidget(self)
        if parent:
            tag_container.setFixedWidth(parent.width()/4)
        else:
            tag_container.setFixedWidth(200)
        # Need to be able to access the layout later to manipulate tags
        self.tag_layout = QVBoxLayout()
        tag_container.setLayout(self.tag_layout)
        for tag in tags:
            t = QLabel(tag, self)
            self.tag_layout.addWidget(t)
        self.layout().addWidget(tag_container)

    def setTags(self, new_tags=None):
        tag = self.tag_layout.takeAt(0).widget()
        tag.deleteLater()
        for tag in new_tags:
            t = QLabel(tag, self)
            self.tag_layout.addWidget(t)


class TagView(QWidget):
    # TagView is the full-window widget which contains a zoomed image, its tags, and the option
    # to add new tags to that image. 
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(parent.geometry())
        self.setLayout(QGridLayout())
        image = parent.currentImage()
        self.zoomed = ZoomedWidget(self, image)
        self.layout().addWidget(self.zoomed, 0, 0)
        tags = ""
        try:
            tags = image.readTags()
        except AttributeError as e:
            print(e)
        self.tlw = TagListWidget(self, tags) 
        self.layout().addWidget(self.tlw, 0, 3)
        taw = TagAddWidget(self)
        self.layout().addWidget(taw, 1, 0)

    def addTag(self, tag):
        self.parent().currentImage().addTag(tag)
        self.updateTags()

    def setImage(self, image):
        self.zoomed.setImage(image)

    def update(self):
        self.setImage(self.parent().currentImage())
        self.updateTags()

    def updateTags(self):
        new_tags = self.parent().currentImage().readTags()
        self.tlw.setTags(new_tags)
        

class TagAddWidget(QWidget):
    
    # TagAddWidget is a widget composed of a QLineEdit and two buttons
    # which, when clicked, adds a tag to the currently selected QImage and 
    # displayed list of tags and allows the user to choose to save them 

    # TODO: Save All Tags button
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(parent.width()*3/4, 100)
        self.setLayout(QHBoxLayout())

        self.tagLine = QLineEdit(self)
        self.tagLine.setPlaceholderText("Add a tag to this image")

        self.tagButtonAdd = QPushButton("Add Tag", self)
        self.tagButtonAdd.clicked.connect(self.handleButton)

        self.layout().addWidget(self.tagLine)
        self.layout().addWidget(self.tagButtonAdd)

    def handleButton(self):
        tag = self.tagLine.text()
        self.parent().addTag(tag)


class ZoomedWidget(QWidget):

    def __init__(self, parent, image=None):
        # TODO: Case for no image
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setGeometry(parent.geometry())
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setMaximumHeight(parent.height())
        self.setImage(image)

    def setImage(self, image):
        # TODO: Use replaceWidget()?
        old_image = self.layout().takeAt(0)
        if old_image:
            old_image.widget().deleteLater()
        zoomed_image = ZoomedImage(self, image)
        # Have to add the image to the widget's layout, not just the widget
        self.layout().addWidget(zoomed_image)
        self.layout().itemAt(0).widget().activate()