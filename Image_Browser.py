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
        p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(p)

        # Widgets and Layouts for various views

        # StackedWidget allows us to display and switch between multiple widgets within 
        # the same main window
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

        # TODO: One function shared between left and right, using focusNextPreviousChild? 
        # TODO: Can't change image while zoomed in
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
                # We have to add the image to the actual layout, not just the widget
                self.stack.widget(1).layout().addWidget(img)
                #img.setScaledContents(False)
                img.setPixmap(img.pixmap().scaled(self.stack.widget(1).size(), Qt.KeepAspectRatio))
                self.stack.setCurrentIndex(1)

            # Zoom Out
            else:
                # We want the measurements of the visible QHBoxLayout's container widget 
                # within the item managed by the layout of the thumbnail screen widget
                self.stack.setCurrentIndex(0)
                width = self.stack.widget(0).layout().itemAt(0).widget().width()
                height = self.stack.widget(0).layout().itemAt(0).widget().height()
                #size = self.stack.widget(0).layout().itemAt(0).widget().size()
                img.setPixmap(img.pixmap().scaledToHeight(height))
                self.stack.widget(0).insertWidget(self.focused_image, img)
                print(img.pixmap().width())
                print(img.pixmap().height())
            img.setFocus()
            
        elif key == Qt.Key_Escape:
            if self.stack.currentIndex() == 1:
                img = self.focusWidget()
                self.stack.widget(0).insertWidget(self.focused_image, img)
                img.setPixmap(img.pixmap().scaled(self.stack.widget(0).size(), Qt.KeepAspectRatio))
                self.stack.setCurrentIndex(0)
                img.setFocus()