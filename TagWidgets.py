from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QSizePolicy, QVBoxLayout, QLineEdit, QLabel, QPushButton, QSpacerItem
from PyQt5.QtCore import *
from Image import ZoomedImage

class TagView(QWidget):
    # TagView is the full-window widget which contains a zoomed image, its tags, and the option
    # to add new tags to that image. 

    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(parent.geometry())
        tags = []

        ####### LAYOUT INITIALIZATION #######

        self.setLayout(QGridLayout())
        image = parent.currentImage()
        self.zoomed = ZoomedWidget(self, image)
        self.layout().addWidget(self.zoomed, 0, 0)
        try:
            tags = image.readTags()
        except:
            pass
        self.tlw = TagListWidget(self, tags) 
        self.layout().addWidget(self.tlw, 0, 3)
        taw = TagAddWidget(self)
        self.layout().addWidget(taw, 1, 0)


    def addTag(self, tag):
        self.parent().addTag(tag)
        self.tlw.addTag(tag)


    def saveAllTags(self):
        self.parent().saveAllTags()


    def setImage(self, image):
        self.zoomed.setImage(image)


    def update(self):
        currentImage = self.parent().currentImage()
        if currentImage:
            self.setImage(currentImage)
            self.updateTags()
        else:
            return


    def updateTags(self):
        new_tags = self.parent().currentImage().readTags()
        self.tlw.updateTags(new_tags)
    
    

class TagListWidget(QWidget):

    # TagLists are widgets which display all of the tags a user has added to an Image. 

    def __init__(self, parent, tags=None):
        
        # Parent is a QWidget, tags is a list of strings 

        super().__init__(parent)
        self.setFixedWidth(parent.width()/8)

        ####### LAYOUT INITIALIZATION #######

        # Widget needs a layout to be able to contain tags
        self.setLayout(QVBoxLayout())
        # Need a container to restrict the size of the tag layout (layouts don't have width)
        tag_container = QWidget(self)
        tag_container.setFixedWidth(parent.width()/8)
        # Need to be able to access the layout later to manipulate tags
        self.tag_layout = QVBoxLayout()
        self.tag_layout.setAlignment(Qt.AlignTop)
        tag_container.setLayout(self.tag_layout)

        # Add tags to widget as qlabels
        if tags:
            for tag in tags:
                t = QLabel(tag, self)
                self.tag_layout.addWidget(t)
        self.layout().addWidget(tag_container)

    
    def addTag(self, tag):
        t = QLabel(tag, self)
        self.tag_layout.addWidget(t)
        

    def updateTags(self, new_tags=None):
        while self.tag_layout.itemAt(0):
            tag = self.tag_layout.takeAt(0).widget()
            tag.deleteLater()
        for tag in new_tags:
            t = QLabel(tag, self)
            self.tag_layout.addWidget(t)
    
    

class TagAddWidget(QWidget):
    
    # TagAddWidget is a widget composed of a QLineEdit and two buttons
    # which, when clicked, adds a tag to the currently selected QImage and 
    # displayed list of tags and allows the user to choose to save them 
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(parent.width()*3/4, 100)
        self.setLayout(QHBoxLayout())

        self.tagLine = QLineEdit(self)
        self.tagLine.setPlaceholderText("Add a tag to this image")

        self.tagButtonAdd = QPushButton("Add Tag", self)
        self.tagButtonAdd.setFocusPolicy(Qt.NoFocus)
        self.tagButtonAdd.clicked.connect(self.handleButtonAdd)

        self.tagButtonSave = QPushButton("Save All Tags", self)
        self.tagButtonSave.setFocusPolicy(Qt.NoFocus)
        self.tagButtonSave.clicked.connect(self.handleButtonSave)

        self.layout().addWidget(self.tagLine)
        self.layout().addWidget(self.tagButtonAdd)
        self.layout().addWidget(self.tagButtonSave)

    def handleButtonAdd(self):
        tag = self.tagLine.text()
        self.parent().addTag(tag)
        self.tagLine.setText("")

    def handleButtonSave(self):
        self.parent().saveAllTags()

class ZoomedWidget(QWidget):

    def __init__(self, parent, image=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setGeometry(parent.geometry())
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setFixedSize(parent.width()*3/4, parent.height())
        if image:
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