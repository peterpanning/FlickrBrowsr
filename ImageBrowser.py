import os
from Image import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel

class ImageBrowser(QWidget):

# An ImageBrowser object is a QWidget, and is created when our program opens a new window

### CONSTRUCTOR ###

	def __init__(self, width=800, height=600, border=5):
		super().__init__()
		self.width = width
		self.height = height
		self.border = border
		self.initXLoc = 300
		self.initYLoc = 300
		self.data_folder = './data'
		self.images = []

		# TODO: Load image tags from json file as dict

		# TODO: Exception handling 

		for file_name in os.listdir(self.data_folder):	
			print(file_name)
			image = Image(self, self.data_folder + "/" + file_name)
			self.images.append(image)

		self.initUI(width, height)  
		self.show()

	def initUI(self, width, height):
		self.setWindowTitle('Image Browser')
		self.setGeometry(self.initXLoc, self.initYLoc, width, height)
		self.setAutoFillBackground(True)
		self.setFocusPolicy(Qt.StrongFocus)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.blue)
		self.setPalette(p)
		self.image_num = 0
		self.thumbnails = []
		for i in range(0, 5):
			thumbnail = self.images[i]
			thumbnail.setGeometry(i * self.width / 5, self.height / 2, self.width / 5, self.height / 4)
			self.thumbnails.append(thumbnail)
		self.selected_image().activate()

	def keyPressEvent(self, event):
		key = event.key()
		
		if key == Qt.Key_Left or key == Qt.Key_Right:
			if self.selected_image().zoomed:
				self.zoomOut()
				self.update_thumbnail_selection(key)
				self.zoomIn()
			else:
				self.update_thumbnail_selection(key)

		elif key == Qt.Key_Return:   
			if self.selected_image().zoomed:
				self.zoomOut()
			else:
				self.zoomIn()

		elif key == Qt.Key_Escape:
			if self.selected_image().zoomed:
				self.zoomOut()

	def selected_image(self):
		return self.thumbnails[self.image_num]

	def zoomOut(self):
		for image in self.thumbnails:
			if image == self.selected_image():
				image.zoomOut()
			else:
				image.show()

	def zoomIn(self):
		for image in self.thumbnails:
			if image == self.selected_image():
				image.zoomIn()
			else:
				image.hide()

	def update_thumbnail_selection(self, key):
		self.selected_image().deactivate()
		if key == Qt.Key_Left:
			if self.image_num == 0:
				self.image_num = len(self.images) - 1
			else:
				self.image_num = self.image_num - 1
		else:
			self.image_num = self.image_num + 1
			if self.image_num == len(self.images):
				self.image_num = 0
		self.selected_image().activate()
