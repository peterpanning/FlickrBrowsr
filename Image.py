"""
An class which represents images and their associated metadata as necessary for display within a simple image browser. 
"""
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget 
from PyQt5.QtCore import *

class Image(QLabel):
	def __init__(self, parent, image_file = "", tags = []):
		super().__init__(parent)
		self.parent = parent
		self.setPixmap(QPixmap(image_file))
		self.tags = tags # Will be a list
		self.thumbActiveStyle = "border: 5px solid blue"
		self.thumbInactiveStyle = "border: 5px solid grey "
		self.zoomedStyle = "border: 10px solid blue"
		self.setAlignment(Qt.AlignCenter)
		self.deactivate()

	def add_tag(self, tag):
		self.tags.append(tag) # TODO: When saving this to file, should write as a JSON array. 

	def resize(self, width, height):
		super().resize(width, height)
		if self.pixmap():
			self.setPixmap(self.pixmap().scaled(width, height, Qt.KeepAspectRatio))

	def activate(self):
		self.setStyleSheet(self.thumbActiveStyle)

	def deactivate(self):
		self.setStyleSheet(self.thumbInactiveStyle)

	def zoom(self):
		self.resize(self.parent.width, self.parent.height)
		self.setStyleSheet(self.zoomedStyle)