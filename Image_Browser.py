import os
from Image import Image
from Widgets import *
#from Layouts import Thumbnail_layout, Zoomed_layout
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout, QStackedWidget, QSizePolicy

class Image_Browser(QWidget):

# An ImageBrowser widget is our main widget, created when the program is initialized

### CONSTRUCTOR ###

    def __init__(self, width=800, height=600, border=5):
        # TODO: Add a layout, which is initialized to a thumbnail layout

        # The ImageBrowser class is the main window which users interact with. 
        # It can switch between two layouts: thumbnail or zoomed. 

        super().__init__()

        # TODO: Ensure I'm not overriding existing functionality i.e. with width and height
        
        self.width = width
        self.height = height
        self.border = border
        self.data_folder = './data'
        self.pixmaps = []
        self.focused_image = 0

        # TODO: Exception handling/input validation on image data
        # TODO: ensure that we only load image files
        # TODO: Load images from an arbitrary folder
        # TODO: Split file loading into its own function

        for file_name in os.listdir(self.data_folder):	
            pixmap = QPixmap(self.data_folder + "/" + file_name)
            self.pixmaps.append(pixmap)
        self.initUI(width, height)  
        self.show()

    ### UI INITIALIZATION ###

    def initUI(self, width, height):

        # Various window properties

        self.setWindowTitle('Image Browser')
        self.setGeometry(300, 300, width, height)
        self.setAutoFillBackground(True)
        self.setFocusPolicy(Qt.NoFocus)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(p)

        # TODO: Split stack and widget initialization into its own function

        # Widgets and Layouts for various views

        # StackedWidget allows us to display and switch between multiple widgets within 
        # the same main window

        # TODO: Subclass StackedWidget so as to be able to write convenience functions
        # for accessing Images, particulary when contained within qhboxlayouts

        self.stack = QStackedWidget()
        thumbnail_widget = ThumbnailWidget(self)
        zoomed_widget = ZoomedWidget(self)

        self.stack.addWidget(thumbnail_widget)
        self.stack.addWidget(zoomed_widget)

        # Finally, we want our main window to have a layout, to be more easily
        # able to modify it later.
        hbox = QHBoxLayout()
        hbox.addWidget(self.stack)

        self.setLayout(hbox)

    ### KEYBOARD INPUT ###
    
    def keyPressEvent(self, event):

        # Controls what happens on keyboard input. Users may navigate through images via keyboard input

        key = event.key()

        # TODO: Change image while zoomed in
        # TODO: Break into many smaller functions
        # TODO: Support navigating through an arbitrary number of images
        if key == Qt.Key_Left:
            if self.focused_image != 0:
                # TODO: Change function name, use Qt focus loss events?
                self.focusWidget().deactivate()
                self.focused_image -= 1 
                self.stack.currentWidget().focusPreviousChild()
                self.focusWidget().activate()
            
        elif key == Qt.Key_Right:
            if self.focused_image != 4:
                self.focusWidget().deactivate()
                self.focused_image += 1
                self.focusWidget().focusNextChild()
                self.focusWidget().activate()

        # TODO: Return from Zoomed and Escape are identical, should probably just call another function
        elif key == Qt.Key_Return:

            # It looks like we have to manually give focus to the new image each time we 
            # change zoom levels. Might be worth looking at later. 

            # Zoom In
            if self.stack.currentIndex() == 0:
                # TODO: Weird bug with zooming, doesn't zoom to truly full window on the first zoom
                # TODO: Might have to do with the way the widget is initialized? 
                zoomed_image = Image(self.stack.widget(1), self.pixmaps[self.focused_image])
                # We have to add the image to the actual layout, not just the widget
                self.stack.widget(1).layout().addWidget(zoomed_image)
                self.stack.setCurrentIndex(1)
                self.stack.widget(1).layout().itemAt(0).widget().setFocus()

            # Zoom Out
            else:
                old_image = self.stack.widget(1).layout().takeAt(0)
                old_image.widget().deleteLater()
                self.stack.setCurrentIndex(0)
                self.stack.widget(0).layout().itemAt(0).widget().layout().itemAt(self.focused_image).widget().setFocus()

        elif key == Qt.Key_Escape:
            if self.stack.currentIndex() == 1:
                old_image = self.stack.widget(1).layout().takeAt(0)
                old_image.widget().deleteLater()
                self.stack.setCurrentIndex(0)
                self.stack.widget(0).layout().itemAt(0).widget().layout().itemAt(self.focused_image).widget().setFocus()
