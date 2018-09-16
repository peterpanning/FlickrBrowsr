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
        thumbnail_container.layout().setSpacing(0)
        thumbnail_container.layout().setContentsMargins(0, 0, 0, 0)
        thumbnail_container.setGeometry(0, parent.height()/3, parent.width(), parent.height()/3)
        thumbnail_container.setFixedHeight(parent.height()/3)
        thumbnail_container.setFixedWidth(parent.width())

        self.layout().addWidget(thumbnail_container)

        ####### IMAGES #######

        total_images = len(parent.images)
        lesser = min(total_images, parent.max_thumbnails)
        
        for i in range(0, lesser):
            self.loadThumbnail(parent.images[i])

        if self.currentImage():
            self.currentImage().activate()

        self.layout().addItem(QSpacerItem(self.width(), self.height()/4))

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


    def handleDelete(self):
        if len(self.parent().images) <= 5:
            item = self.thumbnail_layout().takeAt(self.selected_thumbnail)
            if item:
                item.widget().deleteLater()
        self.parent().handleDelete()


    def handleSave(self):
        for image in self.parent().images:
            image.save()


    def loadThumbnail(self, image):
        thumbnail = Thumbnail(self.thumbnail_container(), image)
        self.thumbnail_layout().addWidget(thumbnail)


    def loadThumbnails(self):
        total_images = len(self.parent().images)
        lesser = min(total_images, self.parent().max_thumbnails)
        # load pixmaps around selected thumbnail
        first_index = self.parent().selected_image_index - self.selected_thumbnail
        j = 0
        for i in range(0, lesser):
            old_image = self.thumbnail_layout().takeAt(0)
            if old_image:
                old_image.widget().deleteLater()
            try:
                self.loadThumbnail(self.parent().images[first_index + i])
            except IndexError:
                self.loadThumbnail(self.parent().images[0 + j])
                j += 1
        try:
            self.currentImage().activate()
        except AttributeError as e:
            pass


    def search(self, terms, max_results):
        self.parent().search(terms, max_results)


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


    def thumbnail_container(self):
        return self.layout().itemAt(0).widget()


    def thumbnail_layout(self):
        return self.thumbnail_container().layout()


    def urlRequest(self, url):
        self.parent().urlRequest(url)


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

        # TODO: Gray out delete button if there are no images

        self.searchButton = MyButton("Search", self)
        self.searchButton.clicked.connect(self.search)
        self.testButton = MyButton("Test", self)
        self.testButton.clicked.connect(self.test)
        self.deleteButton = MyButton("Delete", self)
        self.deleteButton.clicked.connect(self.handleDelete)
        self.saveButton = MyButton("Save", self)
        self.saveButton.clicked.connect(self.handleSave)
        self.exitButton = MyButton("Exit", self)
        self.exitButton.clicked.connect(self.handleExit)
        self.maxResultsLabel = QLabel("Max Results: ", self)
        self.maxResultsLabel.setFixedWidth(80)

        ####### COMBO BOX INIT ####### 

        self.maxResultsBox = QComboBox()
        self.maxResultsBox.setFixedWidth(60)
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

        self.layout().itemAt(0).addWidget(self.testButton)

        self.layout().itemAt(0).addWidget(self.maxResultsLabel)
        self.layout().itemAt(0).addWidget(self.maxResultsBox)

        # Save and Exit get another layout

        self.layout().addLayout(QHBoxLayout())
        self.layout().itemAt(1).setAlignment(Qt.AlignCenter)

        self.layout().itemAt(1).addWidget(self.saveButton)
        self.layout().itemAt(1).addWidget(self.deleteButton)
        self.layout().itemAt(1).addWidget(self.exitButton)


    def handleDelete(self):
        self.parent().handleDelete()


    def handleExit(self):
        exit()


    def handleSave(self):
        self.parent().handleSave()


    def search(self):
        terms = self.searchField.text()
        max_results = int(self.maxResultsBox.currentText())
        self.searchField.setText("")
        self.parent().search(terms, max_results)


    def test(self):
        url = self.searchField.text()
        max_results = int(self.maxResultsBox.currentText())
        self.searchField.setText("")
        self.parent().urlRequest(url)