"""
An class which represents images and their associated metadata as necessary for display in a simple multimedia image browser. 
"""
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget 

class MyImage:
	def __init__(self, parent, image_file, tags):
		self.parent = parent # Save access to the window to later resize width/height dynamically
		self.label = QLabel(parent_window) # Label needs its parent
		self.img = QPixmap(image_file)
		self.tags = parent.tags[image_file] # Will be a list
		self.status = "Inactive"
		self.styles = dict(parent_window.styles) # TODO: CSS? 

	def setImg(self, image_file):
		self.img = QPixmap(image_file)
		self.label.setPixmap(self.img)

	def add_tag(self, tag):
		self.tags.append(tag) # TODO: When saving this to file, should write as a JSON array. 

	"""

	def resize(self, width, height):
		self.label.resize(width, height)
		self.img = self.img.scaled(width, height, Qt.KeepAspectRatio)

	def move(self, x, y): 
		self.label.move(x, y)

	"""

	def setStatus(status):
		self.status = status

	def setStyle(style):
		self.label.setStyleSheet(self.styles[style])