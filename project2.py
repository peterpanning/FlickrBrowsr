# Peter Mutch
# CSc 699
# Spring 2018
# Project 1

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Assignment: Add in tags/comments and audio to image browser. Should play a short sound when changing
# by image, and a longer sound when changing by page. 
# Tags should be persistent when you close and reopen the program. 

import sys
from pathlib import Path 
from PyQt5.QtWidgets import QApplication
from Image_Browser import Image_Browser

if __name__ == '__main__':

	process = QApplication(sys.argv)
	window = Image_Browser()
	sys.exit(process.exec_())