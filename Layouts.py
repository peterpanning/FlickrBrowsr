from PyQt5.QtWidgets import QHBoxLayout, QGridLayout
from Image import Image

class Thumbnail_layout(QHBoxLayout):
    num_images = 5
    def __init__(self, parent):
        super().__init__(parent)

class Zoomed_layout(QGridLayout):
    def __init__(self, parent):
        super().__init__(parent)