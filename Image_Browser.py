import os
from Image import *
from Widgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout, QStackedWidget, QSizePolicy

class Image_Browser(QWidget):

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

        self.viewer = QStackedWidget()

        self.initData()
        self.initUI()
        self.show()
    
    def initData(self, data_folder='./data'):

        # TODO: Exception handling/input validation on image data
        # TODO: ensure that we only load image files
        # TODO: Load images from an arbitrary folder

        for file_name in os.listdir(data_folder):	
            pixmap = QPixmap(data_folder + "/" + file_name)
            self.pixmaps.append(pixmap)

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

        self.thumbnail_widget = ThumbnailWidget(self)
        self.zoomed_widget = ZoomedWidget(self)

        self.viewer.addWidget(self.thumbnail_widget)
        self.viewer.addWidget(self.zoomed_widget)

        # Finally, we want our main window to have a layout, to be more easily
        # able to modify it later.
        hbox = QHBoxLayout()
        
        self.setLayout(hbox)
        hbox.addWidget(self.viewer)


    ### KEYBOARD INPUT ###
    
    def keyPressEvent(self, event):

        # Controls what happens on keyboard input. Users may navigate through images via keyboard input

        key = event.key()

        # TODO: Support navigating through an arbitrary number of images

        if key == Qt.Key_Left:
            # TODO: Make this self.viewer.currentWidget().selectPreviousImage()
            self.leftArrowAction()
            
        elif key == Qt.Key_Right:
            # TODO: Make this self.viewer.currentWidget().selectNextImage()
            self.rightArrowAction()

        elif key == Qt.Key_Return:
            if self.viewer.currentWidget() == self.thumbnail_widget:
                self.zoomIn()
            else:
                self.zoomOut()

        elif key == Qt.Key_Escape:
            if self.viewer.currentWidget() == self.zoomed_widget:
                self.zoomOut()
                

    # TODO: selectImage function which has one implementation in each widget

    def leftArrowAction(self):
        if self.viewer.currentWidget() == self.thumbnail_widget:
            self.currentImage().deactivate()
            self.setSelectedImageIndex(self.selected_image_index - 1)
            self.currentImage().activate()
        else:
            self.setSelectedImageIndex(self.selected_image_index - 1)
            self.viewer.currentWidget().setImage(self.pixmaps[self.selected_image_index])

    def rightArrowAction(self):
        if self.viewer.currentWidget() == self.thumbnail_widget:
            self.currentImage().deactivate()
            self.setSelectedImageIndex(self.selected_image_index + 1)
            self.currentImage().activate()
        else:
            self.setSelectedImageIndex(self.selected_image_index + 1)
            self.viewer.currentWidget().setImage(self.pixmaps[self.selected_image_index])
    
    def zoomOut(self):
        self.viewer.setCurrentWidget(self.thumbnail_widget)

    def zoomIn(self):
        self.viewer.setCurrentWidget(self.zoomed_widget)
        # See Zoomed_Widget class for implementation of setImage
        self.viewer.currentWidget().setImage(self.pixmaps[self.selected_image_index])

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
        return self.viewer.currentWidget().currentImage()