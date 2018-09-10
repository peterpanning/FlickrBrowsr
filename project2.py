# Peter Mutch
# CSc 699
# Spring 2018

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TODO: More elegant handling of cases where there are few or no images

import sys
from pathlib import Path 
from PyQt5.QtWidgets import QApplication
from Image_Browser import Image_Browser

if __name__ == '__main__':

	process = QApplication(sys.argv)
	window = Image_Browser()
	sys.exit(process.exec_())