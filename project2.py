# Peter Mutch
# CSc 699
# Spring 2018
# Project 1

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Assignment: Add in tags/comments and audio to image browser. Should play a short sound when changing
# by image, and a longer sound when changing by page. 
# Tags should be persistent when you close and reopen the program. 

import sys, os, json
from pathlib import Path 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel


class Window(QWidget):

	def __init__(self, width=600, height=400, border=10):
		super().__init__()
		self.width = width
		self.height = height
		self.border = border
		self.data_folder = './data'		
		self.init_data(self.data_folder)
		self.initUI(width, height, border)

	def init_data(self, data_folder):
		# TODO: Load image tags from json file as dict
		self.images = []
		for file_name in os.listdir(data_folder):	
			self.images.append(QPixmap(data_folder + '/' + file_name))
			print(file_name)

	def initUI(self, width, height, border):
		self.setWindowTitle('Image Viewer')
		self.setGeometry(300, 300, width, height)
		self.setAutoFillBackground(True)
		self.zoomed = False
		self.selected_image = 0
		self.setFocusPolicy(Qt.StrongFocus)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.blue)
		self.setPalette(p)
		self.thumbnail_labels = []
		for _ in self.images:
			self.thumbnail_labels.append(QLabel(self))
		self.zoomed_label = QLabel(self)
		self.zoomed_label.setAlignment(Qt.AlignCenter)
		self.zoomed_label.hide()
		self.show()
		self.displayImages()

	def getBorderActive(self):
		return "border: {}px solid red".format(self.border)

	def getBorderInactive(self):
		return "border: {}px solid gray".format(self.border)

	def displayImages(self):
		if self.zoomed:
			self.displayZoomed()
		else:
			self.displayThumbs()

	def displayImage(self, number, x, y, width, height):
		image = self.images[number].scaled(width - self.border * 2, height - self.border * 2, Qt.KeepAspectRatio)
		label = self.thumbnail_labels[number]
		label.move(x, y)
		label.resize(width, height)
		if number == self.selected_image:
			label.setStyleSheet(self.getBorderActive())
		else:
			label.setStyleSheet(self.getBorderInactive())
		label.setPixmap(image)

	def displayZoomed(self):
		# TODO: Set width/height according to global window variables
		for i in range(len(self.thumbnail_labels)):
			self.thumbnail_labels[i].hide()
		image = self.images[self.selected_image].scaled(800 - self.border * 2, 600 - self.border * 2, Qt.KeepAspectRatio)
		self.border = 20
		self.zoomed_label.resize(800, 600)
		self.zoomed_label.setStyleSheet(self.getBorderActive())
		self.zoomed_label.setAlignment(Qt.AlignCenter)
		self.zoomed_label.setPixmap(image)
		self.zoomed_label.show()

	def displayThumbs(self):
		self.zoomed_label.hide()
		self.border = 5
		num = len(self.images)
		for i in range(0, 5):
			self.displayImage(i, i * self.width / num, self.height / 2, self.width/num, self.height / 4)
			if i == self.selected_image:
				self.thumbnail_labels[i].setStyleSheet(self.getBorderActive())
			else:
				self.thumbnail_labels[i].setStyleSheet(self.getBorderInactive())
			self.thumbnail_labels[i].setAlignment(Qt.AlignCenter)
			self.thumbnail_labels[i].show()

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
		self.displayImages()

if __name__ == '__main__':

	app = QApplication(sys.argv)
	e = Window(800, 600, 5)
	sys.exit(app.exec_())