import os
from Image import *
from Widgets import *
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

        # Use of QImages allows us to CRUD image file tags. 

        self.qimages = []

        # Storing file names allows us to more easily access them later for 
        # reading/writing. Alternatively, this could be part of the Image 
        # implementation. 

        self.file_names = []

        # TODO: Pixmaps can be generated from QImages

        # TODO: Doesn't really make sense to maintain a list of pixmaps, considering we 
        # can generate them on demand and will more often be interacting with our 
        # Image class anyways. 

        self.pixmaps = []
        self.selected_image_index = 0

        self.initData()
        self.initUI()
        self.show()
    
    def initData(self, data_folder='./data'):

        # TODO: Get valid extensions from QImage documentation, 
        # see if we even need to check these here

        valid_extensions = ["jpeg", "jpg", "png", "bmp"]

        file_names = sorted(os.listdir(data_folder))

        # Creating only QImages and then Images from there
        # could allow us to save only those QImages and Images
        # rather than pixmaps, which makes more sense as those are
        # data representations and custom objects. 

        for file_name in file_names:
            if file_name == ".DS_Store":
                continue
            extension = file_name.split(".")[1]
            if extension in valid_extensions:
                # TODO: Also create images and read tags
                full_path = data_folder + "/" + file_name
                qimage = QImage(full_path)
                pixmap = QPixmap(full_path)
                self.file_names.append(full_path)
                self.qimages.append(qimage)
                self.pixmaps.append(pixmap)
            else:
                print("Invalid file extension for file {}".format(file_name))
        print(self.selectedQImage().text("PyQtBrowserTags"))

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
        self.tag_widget = TagView(self)

        self.addWidget(self.thumbnail_widget)
        self.addWidget(self.tag_widget)

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
            if self.currentWidget() == self.tag_widget:
                self.zoomOut()

    # TODO: Image_browser provides GUI for tag CRUD operations. Operations require
    # CRUD via QImages  

    def addTag(self, tag):
        #selectedQImage = self.qimages[self.selected_image_index]
        #print("Selected Image: {}".format(selectedQImage))
        #print("Tag: {}".format(tag))
        file_name = self.file_names[self.selected_image_index]
        old_tags = self.imageTags()
        if old_tags:
            #print("Old Tags: {}".format(old_tags))
            #old_tags.append(tag)
            old_tags = old_tags + ", {}".format(tag)
            self.selectedQImage().setText("PyQtBrowserTags", old_tags)
        else:

            self.selectedQImage().setText("PyQtBrowserTags", tag)
        self.selectedQImage().save(file_name)
        print("New Tags: {}".format(self.imageTags()))
        
    def zoomOut(self):
        self.setCurrentWidget(self.thumbnail_widget)

    def zoomIn(self):
        self.setCurrentWidget(self.tag_widget)

    def setSelectedImageIndex(self, new_index):
        num_pixmaps = len(self.pixmaps)
        if new_index < 0:
            self.selected_image_index = num_pixmaps + new_index
        elif new_index >= num_pixmaps:
            self.selected_image_index = new_index - num_pixmaps
        else:
            self.selected_image_index = new_index
        self.thumbnail_widget.setSelectedImageIndex(self.selected_image_index)
        self.tag_widget.setSelectedImageIndex(self.selected_image_index)

    def currentImage(self):
        return self.currentWidget().currentImage()
    
    def selectedQImage(self):
        return self.qimages[self.selected_image_index]

    def imageTags(self):
        return self.selectedQImage().text("PyQtBrowserTags")

    def selectNextImage(self):
        self.thumbnail_widget.selectNextImage()
        self.tag_widget.selectNextImage()

    def selectPreviousImage(self):
        self.thumbnail_widget.selectPreviousImage()
        self.tag_widget.selectPreviousImage()