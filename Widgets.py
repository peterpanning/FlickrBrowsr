from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QSizePolicy


class ThumbnailWidget(QWidget):
    # TODO: This class may as well be called a ThumbnailScreen, because it represents everything
    # visible in the ImageBrowser window when viewing images as thumbnails. 
    # TODO: There are some functions and attributes I would like to use 
    # which must be implemented in subclasses i.e. count
    # TODO: Variable initialization of number of thumbnails
    # Activate sets the stylesheet for the Image, and is not related to the Qt activat() function
    # TODO: Command to set stylesheet which doesn't overlap with existing Qt function names
    def __init__(self, parent):
        super().__init__()
        # This widget has a QHBoxLayout which allows us to add widgets to the screen. 
        # This layout, at the moment, fills the entire screen. 
        view_layout = QHBoxLayout()
        self.setStyleSheet("border: 5px solid red")

        # We then create a container for the thumbnail images we will later navigate through,
        # which allows us to constrain the size of their QHBoxLayout (otherwise impossible).
        thumbnail_container = QWidget()
        thumbnail_container.move(0, parent.height/3)
        thumbnail_container.setMaximumHeight(parent.height/3)
        thumbnail_container.setMaximumWidth(parent.width)
        thumbnail_container.setStyleSheet("border: 5px solid orange")
        # We will be viewing multiple ImageLabels in a horizontal row, 
        # and so will use a QHBoxLayout class which seems to be designed 
        # explicitly for this purpose. 
        thumbnails = QHBoxLayout()

        # *****************************************************************************************************************************
        # TODO: CREATE IMAGELABELS HERE 
        #******************************************************************************************************************************
        for i in range(parent.focused_image, parent.focused_image + 5):
            thumbnails.addWidget(parent.images[i])

        # itemAt() returns a WidgetItem, widget() returns the widget that item manages
        # TODO: Command to set stylesheet which doesn't overlap with existing Qt function names
        thumbnails.itemAt(0).widget().activate()
        thumbnail_container.setLayout(thumbnails)

        view_layout.addWidget(thumbnail_container)
        self.setLayout(view_layout)
        
    def insertWidget(self, index, widget):
        #    View     item      container thumbnails insertion
        self.layout().itemAt(0).widget().layout().insertWidget(index, widget)
    
    # TODO: Override sizeHint()?

class ZoomedWidget(QWidget):
        # Zoomed widget also uses a QHBoxLayout, but has no widgets when we 
        # initialize it. This is because widgets can only exist in one layout
        # at a time. Switching between widgets(and therefore layouts) later 
        # moves the focused Image between widgets as necessary.
    def __init__(self, parent):
        super().__init__()
        #self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)  
        zoomed = QHBoxLayout()
        self.setLayout(zoomed)
        self.setStyleSheet("border: 5px solid green")