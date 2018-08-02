import os
from Image import Image
#from Layouts import Thumbnail_layout, Zoomed_layout
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
        self.data_folder = './data'
        self.images = []
        self.focused_image = 0

        # TODO: Exception handling/input validation on image data

        # TODO: Load images from an arbitrary folder

        for file_name in os.listdir(self.data_folder):	
            # TODO: ensure that we only load image files  
            # print(file_name)
            image = Image(self, self.data_folder + "/" + file_name)
            self.images.append(image)

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
        p.setColor(self.backgroundRole(), Qt.blue)
        self.setPalette(p)

        # Widgets and Layouts for various views

        # We can't change the layout of our main ImageBrowser widget once we've 
        # chosen it, because the Python wrapper doesn't allow us to delete the 
        # old layout on demand.
        # We can, however have multiple widgets, each of which can have
        # its own layout, which can again contain widgets and/or layouts. 

        # StackedWidget allows us to do this and only display one widget at a time
        self.stack = QStackedWidget()

        # TODO: Split this into two additional functions

        # The thumbnail widget uses a QHBoxLayout to display multiple images at once
        # TODO: There are some functions and attributes I would like to use 
        # which must be implemented in subclasses i.e. count
        thumbnail_widget = QWidget()
        thumbnail_layout = QHBoxLayout()
        # TODO: Variable initialization of number of thumbnails
        for i in range(self.focused_image, self.focused_image + 5):
            thumbnail_layout.addWidget(self.images[i])
        # itemAt() returns a WidgetItem, widget() returns the widget that item manages
        # Activate sets the stylesheet for the Image, and is not related to the Qt activat() function
        # TODO: Command to set stylesheet which doesn't overlap with existing Qt function names
        thumbnail_layout.itemAt(0).widget().activate()
        thumbnail_widget.setLayout(thumbnail_layout)
        self.stack.addWidget(thumbnail_widget)
        
        # Zoomed widget also uses a QHBoxLayout, but has no widgets when we 
        # initialize it. This is because widgets can only exist in one layout
        # at a time. Switching between widgets(and therefore layouts) later 
        # moves the focused Image between widgets as necessary.
        zoomed_widget = QWidget()
        zoomed_layout = QHBoxLayout()
        zoomed_widget.setLayout(zoomed_layout)
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

        # TODO: One function shared between left and right, using focusNextPreviousChild? 
        if key == Qt.Key_Left:
            # TODO: Use global variable? QHBox property? 
            if self.focused_image != 0:
                # Sets the style sheet of the widget we are leaving. 
                # TODO: Change function name, find Qt focus loss events
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
            # Setting the index on the stack appears to shift focus to that 
            # stack element. By naming the focused image here, we can 
            # explicitly focus it later after changing widgets/layouts.
            img = self.focusWidget()
            # Zoom In
            if self.stack.currentIndex() == 0:
                self.stack.setCurrentIndex(1)
                # We have to add the image to the actual layout, not just the widget
                self.stack.currentWidget().layout().addWidget(img)
            else:
            # Zoom Out
                self.stack.setCurrentIndex(0)
                self.stack.currentWidget().layout().insertWidget(self.focused_image, img)
            img.setFocus()
            
        elif key == Qt.Key_Escape:
            if self.stack.currentIndex() == 1:
                img = self.focusWidget()
                self.stack.setCurrentIndex(0)
                self.stack.currentWidget().layout().insertWidget(self.focused_image, img)
                img.setFocus()