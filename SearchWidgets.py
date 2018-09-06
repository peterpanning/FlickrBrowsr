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
        thumbnail_container.setMaximumHeight(parent.height()/3)
        thumbnail_container.setMaximumWidth(parent.width())
        
        # Setting this as a layout property makes it easier to access in the Image class
        thumbnail_container.layout().setProperty("max_thumbnails", parent.max_thumbnails)

        self.layout().addWidget(thumbnail_container)

        ####### IMAGES #######
        
        for i in range(0, parent.max_thumbnails):
            self.loadThumbnail(parent.images[i])

        self.currentImage().activate()

        ####### SAVE/DELETE BUTTONS #######

        saveButton = MyButton("Save", self)
        deleteButton = MyButton("Delete", self)
        self.layout().addLayout(QHBoxLayout())
        self.layout().itemAt(1).setAlignment(Qt.AlignCenter)
        self.layout().itemAt(1).addWidget(saveButton)
        self.layout().itemAt(1).addWidget(deleteButton)

        self.layout().addItem(QSpacerItem(self.width(), 50))

        ####### SEARCH BUTTONS #######

        searchPanel = SearchPanel(self)
        self.layout().addWidget(searchPanel)

    def currentImage(self):
        # itemAt() returns a LayoutItem, widget() returns the widget that item manages
        return self.thumbnail_layout().itemAt(self.selected_thumbnail).widget()

    def thumbnail_container(self):
        return self.layout().itemAt(0).widget()

    def thumbnail_layout(self):
        return self.thumbnail_container().layout()

    def loadThumbnail(self, image):
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

    def loadThumbnails(self):
        # load pixmaps around selected thumbnail
        first_index = self.parent().selected_image_index - self.selected_thumbnail
        last_index = self.parent().selected_image_index + (self.parent().max_thumbnails - self.selected_thumbnail)
        for i in range(0, self.parent().max_thumbnails):
            old_image = self.thumbnail_layout().takeAt(0)
            if old_image:
                old_image.widget().deleteLater()
        for i in range(first_index, last_index):
            try:
                self.loadThumbnail(self.parent().images[i])
            except IndexError:
                self.loadThumbnail(self.parent().images[i - len(self.parent().images)])
        self.currentImage().activate()

class SearchPanel(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        # The SearchPanel itself does not accept focus. 
        # It stretches the full width of the bottom quarter of the screen. 
        # It has a GridLayout which contains all of its buttons and fields. 
        self.setFocusPolicy(Qt.NoFocus)
        self.setFixedSize(parent.width(), parent.height()/4)
        self.setLayout(QVBoxLayout())

        # Panel Components

        searchField = QLineEdit()
        searchField.setPlaceholderText("Search for images")
        searchField.setFixedWidth(parent.width()/3)
        searchButton = MyButton("Search", self)
        exitButton = MyButton("Exit", self)
        maxResultsLabel = QLabel("Max Results: ", self)
        maxResultsLabel.setFixedWidth(80)

        # Combo Box Initialization 

        maxResultsBox = QComboBox()
        maxResultsBox.setFixedWidth(50)
        for i in range(1, 11):
            maxResultsBox.addItem('{}'.format(i))
        maxResultsBox.addItem('20')
        maxResultsBox.addItem('50')

        # Add Widgets to layout

        # Buttons below the thumbnails their own layout
        self.layout().addLayout(QHBoxLayout())
        self.layout().itemAt(0).setAlignment(Qt.AlignHCenter)

        # Followed by the SearchField widgets

        self.layout().itemAt(0).addWidget(searchField)
        self.layout().itemAt(0).addWidget(searchButton)

        # So do Max Results widgets

        self.layout().itemAt(0).addWidget(maxResultsLabel)
        self.layout().itemAt(0).addWidget(maxResultsBox)

        self.layout().addWidget(exitButton)
        self.layout().itemAt(1).setAlignment(Qt.AlignHCenter)
