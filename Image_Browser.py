import os
from Image import *
from Widgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout, QStackedWidget, QSizePolicy

class Image_Browser(QStackedWidget):

# TODO: Make Image_Browser a QStackedWidget subclass? 

# An ImageBrowser widget is our main widget, created when the program is initialized

### CONSTRUCTOR ###

    def __init__(self):

        # The ImageBrowser class is the main window which users interact with. 
        # It can switch between two views: thumbnail or zoomed. 

        super().__init__()

        self.pixmaps = []
        self.selected_image_index = 0

        # StackedWidget allows us to display and switch between multiple widgets within 
        # the same main window

        self.initData()
        self.initUI()
        self.show()
    
    def initData(self, data_folder='./data'):

        # TODO: Load images from an arbitrary folder

        valid_extensions = ["jpeg", "jpg", "png", "bmp"]

        for file_name in sorted(os.listdir(data_folder)):
            if file_name == ".DS_Store":
                continue
            extension = file_name.split(".")[1]
            if extension in valid_extensions:
                pixmap = QPixmap(data_folder + "/" + file_name)
                self.pixmaps.append(pixmap)
            else:
                print("Invalid file extension for file {}".format(file_name))

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

        self.thumbnail_widget = ThumbnailWidget(self)
        self.zoomed_widget = ZoomedWidget(self)

        self.addWidget(self.thumbnail_widget)
        self.addWidget(self.zoomed_widget)

    ### KEYBOARD INPUT ###
    
    def keyPressEvent(self, event):

        # Controls what happens on keyboard input. Users may navigate through images via keyboard input

        key = event.key()

        if key == Qt.Key_Left:
            self.setSelectedImageIndex(self.selected_image_index - 1)
            self.selectPreviousImage()
            
        elif key == Qt.Key_Right:
            self.setSelectedImageIndex(self.selected_image_index + 1)
            self.selectNextImage()

        elif key == Qt.Key_Return:
            if self.currentWidget() == self.thumbnail_widget:
                self.zoomIn()
            else:
                self.zoomOut()

        elif key == Qt.Key_Escape:
            if self.currentWidget() == self.zoomed_widget:
                self.zoomOut()
                
    
    def zoomOut(self):
        self.setCurrentWidget(self.thumbnail_widget)

    def zoomIn(self):
        self.setCurrentWidget(self.zoomed_widget)

    def setSelectedImageIndex(self, new_index):
        num_pixmaps = len(self.pixmaps)
        if new_index < 0:
            self.selected_image_index = num_pixmaps + new_index
        elif new_index >= num_pixmaps:
            self.selected_image_index = new_index - num_pixmaps
        else:
            self.selected_image_index = new_index
        self.thumbnail_widget.setSelectedImageIndex(self.selected_image_index)
        self.zoomed_widget.setSelectedImageIndex(self.selected_image_index)

    def currentImage(self):
        return self.currentWidget().currentImage()

    def selectNextImage(self):
        self.thumbnail_widget.selectNextImage()
        self.zoomed_widget.selectNextImage()

    def selectPreviousImage(self):
        self.thumbnail_widget.selectPreviousImage()
        self.zoomed_widget.selectPreviousImage()