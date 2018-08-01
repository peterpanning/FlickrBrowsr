import os
from Image import Image
from Layouts import Thumbnail_layout, Zoomed_layout
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout, QStackedWidget

class Image_Browser(QWidget):

# An ImageBrowser object is a QStackedWidget, and is created when the program is initialized

### CONSTRUCTOR ###

    def __init__(self, width=800, height=600, border=5):
        # TODO: Add a layout, which is initialized to a thumbnail layout

        # The ImageBrowser class is the main window which users interact with. 
        # It can switch between two layouts: thumbnail or zoomed. 

        super().__init__()
        
        self.width = width
        self.height = height
        self.border = border
        self.initXLoc = 300
        self.initYLoc = 300
        self.data_folder = './data'
        self.images = []
        self.focused_image = 0
        self.carousel = []

        # TODO: Exception handling/input validation on image data

        # TODO: Load images from an arbitrary folder

        # Images are all image files in the data folder, as opposed
        # to carousel, which are the images being displayed. 

        for file_name in os.listdir(self.data_folder):	
            # TODO: ensure that we only load image files  
            # print(file_name)
            image = Image(self, self.data_folder + "/" + file_name)
            self.images.append(image)

        self.initUI(width, height)  
        self.show()

    def initUI(self, width, height):

        # The UI has a layout, which can be changed as necessary. Also controls other GUI props

        # TODO: Initialize layout
        self.setWindowTitle('Image Browser')
        self.setGeometry(self.initXLoc, self.initYLoc, width, height)
        self.setAutoFillBackground(True)
        self.setFocusPolicy(Qt.StrongFocus)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.blue)
        self.setPalette(p)

        # StackedWidgets are composed of multiple widgets, each of which can have their own layout
        self.stack = QStackedWidget()

        # Thumbnail widget uses a QHBoxLayout for its multi-widget carousel
        thumbnail_widget = QWidget()
        thumbnail_layout = QHBoxLayout()
        for i in range(self.focused_image, self.focused_image + 5):
            thumbnail_layout.addWidget(self.images[i])
        thumbnail_widget.setLayout(thumbnail_layout)
        self.stack.addWidget(thumbnail_widget)
        
        # Zoomed widget also uses a QHBoxLayout, but has only one widget
        zoomed_widget = QWidget()
        zoomed_layout = QHBoxLayout()
        zoomed_layout.addWidget(self.images[self.focused_image])
        zoomed_widget.setLayout(zoomed_layout)
        self.stack.addWidget(zoomed_widget)

        # Finally, Widgets cannot add widgets, only Layouts can, so our main 
        # window must have a layout in order to be able to contain these 
        # widgets. It is also an HBox, because our window will usually be
        # wider than it is tall. 

        hbox = QHBoxLayout()
        hbox.addWidget(self.stack)

        self.setLayout(hbox)

    def keyPressEvent(self, event):

        # Controls what happens on keyboard input. Users may navigate through images via keyboard
        # or mouse input

        key = event.key()
        if key == Qt.Key_Left or key == Qt.Key_Right:
            if self.selected_image().zoomed:
                self.zoomOut()
                self.update_thumbnail_selection(key)
                self.zoomIn()
            else:
                self.update_thumbnail_selection(key)

        elif key == Qt.Key_Return:
            if self.stack.currentIndex() == 0:
                self.stack.setCurrentIndex(1)
            else:
                self.stack.setCurrentIndex(0)

        elif key == Qt.Key_Escape:
            if self.stack.currentIndex() == 1:
                self.stack.setCurrentIndex(0)

    def update_thumbnail_selection(self, key):

        # TODO: This should update images, not just thumbnails. It should be able to do so 
        # regardless of layout but with respect to the number of images in the thumbnail layout. 
        
        self.selected_image().deactivate()
        if key == Qt.Key_Left:
            if self.image_num == 0:
                # TODO: Is this wrap-around behavior expected?
                self.image_num = len(self.images) - 1
            else:
                self.image_num = self.image_num - 1
        else:
            self.image_num = self.image_num + 1
            # TODO: Is this wrap-around behavior expected?
            if self.image_num == len(self.images):
                self.image_num = 0
        self.selected_image().activate()

    def selected_image(self):
        return self.carousel[self.focused_image]