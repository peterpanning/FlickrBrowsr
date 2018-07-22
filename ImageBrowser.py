import os
from Image import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel

class ImageBrowser(QWidget):

# An ImageBrowser object is a QWidget, and is created when the program is initialized

### CONSTRUCTOR ###

	def __init__(self, width=800, height=600, border=5):
		# TODO: Add a layout, which is initialized to a thumbnail layout

		# The ImagBrowser class is the main window which users interact with. 
		# It can switch between two layouts: thumbnail or zoomed. 

		super().__init__()
		self.width = width
		self.height = height
		self.border = border
		self.initXLoc = 300
		self.initYLoc = 300
		self.data_folder = './data'
		self.images = []
		self.image_num = 0
		self.carousel = []

		# TODO: Load image tags from file

		# TODO: Exception handling/input validation on image data

		# TODO: Load images from an arbitrary folder

		# Images are all image files in the data folder, as opposed
		# to carousel, which are the images being displayed. 

		for file_name in os.listdir(self.data_folder):	
			# TODO: ensure that we only load image files  
			print(file_name)
			image = Image(self, self.data_folder + "/" + file_name)
			self.images.append(image)

		self.initUI(width, height)  
		self.show()

	def initUI(self, width, height):

		# The UI has a layout, which can be changed as necessary. Also controls other GUI props

		# TODO: Initialize layout
		self.setWindowTitle('Image Browser')
		self.setGeometry(self.initXLoc, self.initYLoc, width, height)
		self.setAutoFillBackground(True)
		self.setFocusPolicy(Qt.StrongFocus)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.blue)
		self.setPalette(p)

		for i in range(0, 5):
			thumbnail = self.images[i]
			thumbnail.setGeometry(i * self.width / 5, self.height / 2, self.width / 5, self.height / 4)
			self.carousel.append(thumbnail)
		self.selected_image().activate()

	def keyPressEvent(self, event):

		# Controls what happens on keyboard input. Users may navigate through images via keyboard
		# or mouse input

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

	def zoomOut(self):

		# Images know how to zoom out. This function may become deprecated as layouts are added

		for image in self.carousel:
			if image == self.selected_image():
				image.zoomOut()
			else:
				image.show()

	def zoomIn(self):

		# Images know how to zoom in. This function may become deprecated as layouts are added


		for image in self.carousel:
			if image == self.selected_image():
				image.zoomIn()
			else:
				image.hide()

	def update_thumbnail_selection(self, key):

		# TODO: This should update images, not just thumbnails. It should be able to do so 
		# regardless of layout but with respect to the number of images in the thumbnail layout. 
		
		self.selected_image().deactivate()
		if key == Qt.Key_Left:
			if self.image_num == 0:
				# TODO: Is this wrap-around behavior expected?
				self.image_num = len(self.images) - 1
			else:
				self.image_num = self.image_num - 1
		else:
			self.image_num = self.image_num + 1
			# TODO: Is this wrap-around behavior expected?
			if self.image_num == len(self.images):
				self.image_num = 0
		self.selected_image().activate()

	def selected_image(self):
		return self.carousel[self.image_num]