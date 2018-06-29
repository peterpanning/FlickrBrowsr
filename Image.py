"""
An class which represents images and their associated metadata as necessary for display within a simple image browser. 
"""
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget 
from PyQt5.QtCore import *

class Image:
	def __init__(self, parent, image_file = "", tags = []):
		self.label = QLabel(parent) # Label needs its parent
		self.label.setPixmap(QPixmap(image_file))
		self.tags = tags # Will be a list
		self.thumbActiveStyle = "border: 5px solid blue"
		self.thumbInactiveStyle = "border: 5px solid grey "
		self.zoomedStyle = "border: 10px solid blue"
		self.setStyle(self.thumbInactiveStyle)

	def add_tag(self, tag):
		self.tags.append(tag) # TODO: When saving this to file, should write as a JSON array. 

	def resize(self, width, height):
		self.label.resize(width, height)
		if self.label.pixmap():
			self.label.setPixmap(self.label.pixmap().scaled(width, height, Qt.KeepAspectRatio))

	def move(self, x, y): 
		self.label.move(x, y)

	def hide(self):
		self.label.hide()

	def show(self):
		self.label.show()

	def setStyle(self, style):
		# Style is a string composed of the styles rules this label should follow
		if style == "Zoomed":
			self.label.setStyleSheet(self.zoomedStyle)
		elif style == "Inactive":
			self.label.setStyleSheet(self.thumbInactiveStyle)
		else:
			self.label.setStyleSheet(self.thumbActiveStyle)
		return