from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QSizePolicy, QVBoxLayout, QLineEdit, QLabel, QPushButton, QSpacerItem, QComboBox
from PyQt5.QtCore import *
from Image import Thumbnail
from MyButton import MyButton


class SearchView(QWidget):

    def __init__(self, parent): 
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setGeometry(parent.geometry())
        self.selected_thumbnail = 0

        ####### LAYOUT INITIALIZATION #######

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.layout().setAlignment(Qt.AlignVCenter)

        ####### THUMBNAILS #######

        # Create a container for the thumbnail images to constrain the height 
        # of the layout
        
        thumbnail_container = QWidget(self)
        thumbnail_container.setLayout(QHBoxLayout())
        thumbnail_container.setGeometry(0, parent.height()/3, parent.width(), parent.height()/3)
        thumbnail_container.setFixedHeight(parent.height()/3)
        thumbnail_container.setFixedWidth(parent.width())
        
        # Setting this as a layout property makes it easier to access in the Image class
        thumbnail_container.layout().setProperty("max_thumbnails", parent.max_thumbnails)

        self.layout().addWidget(thumbnail_container)

        ####### IMAGES #######

        total_images = len(parent.images)
        lesser = min(total_images, parent.max_thumbnails)
        
        for i in range(0, lesser):
            self.loadThumbnail(parent.images[i])

        if self.currentImage():
            self.currentImage().activate()

        ####### DELETE BUTTON #######

        self.layout().addLayout(QHBoxLayout())
        deleteButton = MyButton("Delete", self)
        deleteButton.clicked.connect(self.handleDelete)
        self.layout().itemAt(1).addWidget(deleteButton)

        self.layout().addItem(QSpacerItem(self.width(), 50))

        ####### SEARCH BUTTONS #######

        searchPanel = SearchPanel(self)
        self.layout().addWidget(searchPanel)

    def currentImage(self):
        # itemAt() returns a LayoutItem, widget() returns the widget that item manages
        item = self.thumbnail_layout().itemAt(self.selected_thumbnail)
        if item:
            return item.widget()
        else: 
            return None

    def thumbnail_container(self):
        return self.layout().itemAt(0).widget()

    def thumbnail_layout(self):
        return self.thumbnail_container().layout()

    def loadThumbnail(self, image):
        thumbnail = Thumbnail(self.thumbnail_container(), image)
        self.thumbnail_layout().addWidget(thumbnail)

    def selectNextImage(self):
        limit = min(len(self.parent().images), self.parent().max_thumbnails) - 1
        try:
            if self.selected_thumbnail == limit:
                self.selected_thumbnail = 0
                self.loadThumbnails()
            else:
                self.currentImage().deactivate()
                self.selected_thumbnail += 1
            self.currentImage().activate()
        except AttributeError as e:
            pass
    
    def selectPreviousImage(self):
        limit = min(len(self.parent().images), self.parent().max_thumbnails) - 1
        try:
            if self.selected_thumbnail == 0:
                self.selected_thumbnail = limit
                self.loadThumbnails()
            else:
                self.currentImage().deactivate()
                self.selected_thumbnail -= 1
            self.currentImage().activate()
        except AttributeError as e:
            pass

    def loadThumbnails(self):
        total_images = len(self.parent().images)
        lesser = min(total_images, self.parent().max_thumbnails)
        # load pixmaps around selected thumbnail
        first_index = self.parent().selected_image_index - self.selected_thumbnail
        last_index = self.parent().selected_image_index + (lesser - self.selected_thumbnail)
        for i in range(0, lesser):
            old_image = self.thumbnail_layout().takeAt(0)
            if old_image:
                old_image.widget().deleteLater()
        for i in range(first_index, last_index):
            try:
                self.loadThumbnail(self.parent().images[i])
            except IndexError:
                self.loadThumbnail(self.parent().images[i - lesser])
        try:
            self.currentImage().activate()
        except AttributeError as e:
            pass

    def search(self, terms, max_results):
        self.parent().search(terms, max_results)

    def handleDelete(self):
        self.parent().handleDelete()

    def handleSave(self):
        for image in self.parent().images:
            image.save()

class SearchPanel(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        # The SearchPanel itself does not accept focus. 
        # It stretches the full width of the bottom quarter of the screen. 
        # It has a GridLayout which contains all of its buttons and fields. 
        self.setFocusPolicy(Qt.NoFocus)
        self.setFixedSize(parent.width(), parent.height()/4)
        self.setLayout(QVBoxLayout())

        ####### SEARCH FIELD INIT #######

        self.searchField = QLineEdit()
        self.searchField.setPlaceholderText("Search for images")
        self.searchField.setFixedWidth(parent.width()/3)

        ####### SEARCH BUTTONS INIT #######

        self.searchButton = MyButton("Search", self)
        self.searchButton.clicked.connect(self.search)
        self.saveButton = MyButton("Save", self)
        self.saveButton.clicked.connect(self.handleSave)
        self.exitButton = MyButton("Exit", self)
        self.exitButton.clicked.connect(self.handleExit)
        self.maxResultsLabel = QLabel("Max Results: ", self)
        self.maxResultsLabel.setFixedWidth(80)

        ####### COMBO BOX INIT ####### 

        self.maxResultsBox = QComboBox()
        self.maxResultsBox.setFixedWidth(50)
        for i in range(1, 11):
            self.maxResultsBox.addItem('{}'.format(i))
        self.maxResultsBox.addItem('20')
        self.maxResultsBox.addItem('50')

        ####### ADDING WIDGETS #######

        # Search and maxResults are in the same layout
        self.layout().addLayout(QHBoxLayout())
        self.layout().itemAt(0).setAlignment(Qt.AlignHCenter)

        self.layout().itemAt(0).addWidget(self.searchField)
        self.layout().itemAt(0).addWidget(self.searchButton)

        self.layout().itemAt(0).addWidget(self.maxResultsLabel)
        self.layout().itemAt(0).addWidget(self.maxResultsBox)

        # Save and Exit get another layout

        self.layout().addLayout(QHBoxLayout())
        self.layout().itemAt(1).setAlignment(Qt.AlignCenter)

        self.layout().itemAt(1).addWidget(self.saveButton)
        self.layout().itemAt(1).addWidget(self.exitButton)

    def search(self):
        terms = self.searchField.text()
        max_results = int(self.maxResultsBox.currentText())
        self.parent().search(terms, max_results)

    def handleExit(self):
        exit()

    def handleSave(self):
        self.parent().handleSave()