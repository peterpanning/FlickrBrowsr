import os
from Image import *
from TagWidgets import *
from SearchWidgets import *
from Flickr import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout, QStackedWidget, QSizePolicy

class Image_Browser(QStackedWidget):

# An ImageBrowser widget is our main widget, created when the program is initialized

# StackedWidget allows us to display and switch between multiple widgets within 
# the same main window


### CONSTRUCTOR ###

    def __init__(self):

        # The ImageBrowser class is the main window which users interact with. 
        # It can switch between two views: thumbnail or zoomed. 

        super().__init__()

        self.selected_image_index = 0
        self.images = []

        self.initData()
        self.initUI()
        self.show()
    
    def initData(self, data_folder='./data'):

        file_names = sorted(os.listdir(data_folder))

        for file_name in file_names:
            if file_name == ".DS_Store":
                continue
            full_path = data_folder + "/" + file_name
            image = Image(self, full_path)
            self.images.append(image)
        
        flickr = Flickr()

    ### UI INITIALIZATION ###

    def initUI(self, x=300, y=300, width=800, height=600):

        # Various window properties

        self.setWindowTitle('Image Browser')
        self.setGeometry(x, y, width, height)
        self.setAutoFillBackground(True)
        self.setFocusPolicy(Qt.StrongFocus)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(p)
        self.setMaximumSize(1920, 1080)
        self.max_thumbnails = 5

        self.thumbnail_widget = SearchView(self)
        self.tag_widget = TagView(self)

        self.addWidget(self.thumbnail_widget)
        self.addWidget(self.tag_widget)

    ### KEYBOARD INPUT ###
    
    def keyPressEvent(self, event):

        # Controls what happens on keyboard input. Users may navigate through images via keyboard input

        key = event.key()

        if key == Qt.Key_Left:
            self.selectPreviousImage()
            
        elif key == Qt.Key_Right:
            self.selectNextImage()

        elif key == Qt.Key_Return:
            if self.currentWidget() == self.thumbnail_widget:
                self.zoomIn()
            else:
                self.zoomOut()

        elif key == Qt.Key_Escape:
            if self.currentWidget() == self.tag_widget:
                self.zoomOut()

        elif key == Qt.Key_Comma or key == Qt.Key_PageUp:
            if self.currentWidget() == self.thumbnail_widget:
                self.selectPreviousPage()
            else:
                pass
                # Play error sound
        
        elif key == Qt. Key_Period or key == Qt.Key_PageDown:
            if self.currentWidget() == self.thumbnail_widget:
                self.selectNextPage()
            else:
                pass
                # Play error sound

        
    def zoomOut(self):
        self.setCurrentWidget(self.thumbnail_widget)

    def zoomIn(self):
        self.setCurrentWidget(self.tag_widget)

    def setSelectedImageIndex(self, new_index):
        num_images = len(self.images)
        if new_index < 0:
            self.selected_image_index = num_images + new_index
        elif new_index >= num_images:
            self.selected_image_index = new_index - num_images
        else:
            self.selected_image_index = new_index

    def currentImage(self):
        return self.images[self.selected_image_index]

    def selectNextImage(self):
        self.setSelectedImageIndex(self.selected_image_index + 1)
        self.thumbnail_widget.selectNextImage()
        self.tag_widget.update()

    def selectPreviousImage(self):
        self.setSelectedImageIndex(self.selected_image_index - 1)
        self.thumbnail_widget.selectPreviousImage()
        self.tag_widget.update()

    def selectNextPage(self):
        self.setSelectedImageIndex(self.selected_image_index + self.max_thumbnails)
        self.thumbnail_widget.loadThumbnails()
        self.tag_widget.update()
    
    def selectPreviousPage(self):
        self.setSelectedImageIndex(self.selected_image_index - self.max_thumbnails)
        self.thumbnail_widget.loadThumbnails()
        self.tag_widget.update()

    def addTag(self, tag):
        self.currentImage().addTag(tag)

    def saveAllTags(self):
        for image in self.images:
            image.saveTags()