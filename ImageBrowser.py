import os
from Image import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel

class ImageBrowser(QWidget):

# An ImageBrowser object is a QWidget, and is created when our program opens a new window

### CONSTRUCTOR ###

	def __init__(self, width=800, height=600, border=5):

		# TODO: Add QStyle for each operating system
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
		self.display()

	def initUI(self, width, height):
		self.setWindowTitle('Image Browser')
		self.setGeometry(self.initXLoc, self.initYLoc, width, height)
		self.setAutoFillBackground(True)
		self.setFocusPolicy(Qt.StrongFocus)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.blue)
		self.setPalette(p)

		self.zoomed = False
		self.selected_image = 0

		self.zoomed_image = self.images[self.selected_image]

		# As will the image thumbnails

		self.thumbnails = []
		for i in range(0, 5):
			thumbnail = self.images[i]
			thumbnail.move(i * self.width / 5, self.height / 2)
			thumbnail.resize(self.width / 5, self.height / 4)
			thumbnail.deactivate()
			thumbnail.setAlignment(Qt.AlignCenter)
			self.thumbnails.append(thumbnail)
			thumbnail.show()
		self.thumbnails[self.selected_image].activate()

	def display(self):
		if self.zoomed:
			self.displayZoomed()
		else:
			self.displayThumbs()

	def displayZoomed(self):
		# Hide all other images
		for i in range(len(self.thumbnails)):
			self.thumbnails[i].hide()
		# Scale up the selected image
		self.thumbnails[self.selected_image].resize(self.width - self.border * 2, self.height - self.border * 2)
		self.thumbnails[self.selected_image].show()

	def displayThumbs(self):
		# In thumbnail view, hide the zoomed image
		self.zoomed_image.hide()
		for i in range(0, 5):
			self.thumbnails[i].show()

	# TODO: This is effectively the controller section, and should be in either its own class or
	# in the main function. 

	def keyPressEvent(self, event):
		key = event.key()
		if key == Qt.Key_Left:
			if self.selected_image == 0:
				self.selected_image = len(self.images) - 1
			else:
				self.selected_image = self.selected_image - 1

		elif key == Qt.Key_Right: 
			self.selected_image = self.selected_image + 1
			if self.selected_image == len(self.images):
				self.selected_image = 0

		elif key == Qt.Key_Return:
			if self.zoomed: 
				self.displayThumbs()
			else: 
				self.displayZoomed()
			self.zoomed = not self.zoomed

		elif key == Qt.Key_Escape:
			if self.zoomed:
				self.displayThumbs()
				self.zoomed = not self.zoomed
		self.display()