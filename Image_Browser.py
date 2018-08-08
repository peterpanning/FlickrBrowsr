import os
from Image import *
from Widgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout, QStackedWidget, QSizePolicy

class Image_Browser(QWidget):

# An ImageBrowser widget is our main widget, created when the program is initialized

### CONSTRUCTOR ###

    def __init__(self):

        # The ImageBrowser class is the main window which users interact with. 
        # It can switch between two layouts: thumbnail or zoomed. 

        super().__init__()

        self.pixmaps = []
        self.focused_image = 0

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

        # TODO: Change image while zoomed in
        # TODO: Support navigating through an arbitrary number of images

        if key == Qt.Key_Left:
            self.arrowAction("Left")
            
        elif key == Qt.Key_Right:
            self.arrowAction("Right")

        elif key == Qt.Key_Return:
            if self.viewer.currentWidget() == self.thumbnail_widget:
                self.zoomIn()
            else:
                self.zoomOut()

        elif key == Qt.Key_Escape:
            if self.viewer.currentWidget() == self.zoomed_widget:
                self.zoomOut()

    def arrowAction(self, direction):
        self.focusWidget().deactivate()
        if direction == "Left":
            if self.focused_image != 0:
                self.focused_image -= 1 
                self.viewer.currentWidget().focusPreviousChild()
        elif direction == "Right":
            if self.focused_image != 4:
                self.focused_image += 1
                self.focusWidget().focusNextChild()
        self.focusWidget().activate()
        
    def zoomOut(self):
        self.viewer.setCurrentWidget(self.thumbnail_widget)
        # See ThumbnailWidget class for implementation of focusOn()
        self.viewer.currentWidget().focusOn(self.focused_image)

    def zoomIn(self):
        old_image = self.zoomed_widget.layout().takeAt(0)
        if old_image:
            old_image.widget().deleteLater()
        # TODO: Weird bug with zooming, doesn't zoom to truly full window on the first zoom
        # Might have to do with the way the widget is initialized? 
        zoomed_image = Image(self.zoomed_widget, self.pixmaps[self.focused_image])
        # Have to add the image to the widget's layout, not just the widget
        self.viewer.setCurrentWidget(self.zoomed_widget)
        self.viewer.currentWidget().layout().addWidget(zoomed_image)
        self.viewer.currentWidget().layout().itemAt(0).widget().setFocus()
