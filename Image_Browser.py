import os
from Image import *
from TagWidgets import *
from SearchWidgets import *
import flickrapi
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import xml.etree.ElementTree as ET
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout, QStackedWidget, QSizePolicy

class Image_Browser(QStackedWidget):

# An ImageBrowser widget is our main widget, created when the program is initialized

# StackedWidget allows us to display and switch between multiple widgets within 
# the same main window


### CONSTRUCTOR ###

    def __init__(self):

        # The ImageBrowser class is the main window which users interact with. 
        # It can switch between two views: thumbnail or zoomed. 

        super().__init__()

        self.selected_image_index = 0
        self.images = []
        self.netman = QNetworkAccessManager()
        self.netman.finished.connect(self.requestFinished)

        self.initData()
        self.initUI()
        self.show()
    
    def initData(self, data_folder='./data'):

        file_names = sorted(os.listdir(data_folder))

        for file_name in file_names:
            if file_name == ".DS_Store":
                continue
            full_path = data_folder + "/" + file_name
            image = Image(self, full_path)
            self.images.append(image)

        xml = ET.parse('secrets.xml')
        # TODO: Read these secrets using keywords or something similar
        root = xml.getroot()
        api_key = root[0][0].text
        api_secret = root[0][1].text

        self.flickr = flickrapi.FlickrAPI(api_key, api_secret)
        
    ### UI INITIALIZATION ###

    def initUI(self, x=300, y=300, width=800, height=600):

        # Various window properties

        self.setWindowTitle('Image Browser')
        self.setGeometry(x, y, width, height)
        self.setAutoFillBackground(True)
        self.setFocusPolicy(Qt.StrongFocus)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(p)
        self.setMaximumSize(1920, 1080)
        self.max_thumbnails = 5

        self.thumbnail_widget = SearchView(self)
        self.tag_widget = TagView(self)

        self.addWidget(self.thumbnail_widget)
        self.addWidget(self.tag_widget)

    ### KEYBOARD INPUT ###
    
    def keyPressEvent(self, event):

        # Controls what happens on keyboard input. Users may navigate through images via keyboard input

        key = event.key()

        if key == Qt.Key_Left:
            self.selectPreviousImage()
            
        elif key == Qt.Key_Right:
            self.selectNextImage()

        elif key == Qt.Key_Return:
            if self.currentWidget() == self.thumbnail_widget:
                self.zoomIn()
            else:
                self.zoomOut()

        elif key == Qt.Key_Escape:
            if self.currentWidget() == self.tag_widget:
                self.zoomOut()

        elif key == Qt.Key_Comma or key == Qt.Key_PageUp:
            if self.currentWidget() == self.thumbnail_widget:
                self.selectPreviousPage()
            else:
                pass
                # Play error sound
        
        elif key == Qt. Key_Period or key == Qt.Key_PageDown:
            if self.currentWidget() == self.thumbnail_widget:
                self.selectNextPage()
            else:
                pass
                # Play error sound

        
    def zoomOut(self):
        self.setCurrentWidget(self.thumbnail_widget)

    def zoomIn(self):
        self.setCurrentWidget(self.tag_widget)

    def setSelectedImageIndex(self, new_index):
        num_images = len(self.images)
        if new_index < 0:
            self.selected_image_index = num_images + new_index
        elif new_index >= num_images:
            self.selected_image_index = new_index - num_images
        else:
            self.selected_image_index = new_index

    def currentImage(self):
        return self.images[self.selected_image_index]

    def selectNextImage(self):
        self.setSelectedImageIndex(self.selected_image_index + 1)
        self.thumbnail_widget.selectNextImage()
        self.tag_widget.update()

    def selectPreviousImage(self):
        self.setSelectedImageIndex(self.selected_image_index - 1)
        self.thumbnail_widget.selectPreviousImage()
        self.tag_widget.update()

    def selectNextPage(self):
        self.setSelectedImageIndex(self.selected_image_index + self.max_thumbnails)
        self.thumbnail_widget.loadThumbnails()
        self.tag_widget.update()
    
    def selectPreviousPage(self):
        self.setSelectedImageIndex(self.selected_image_index - self.max_thumbnails)
        self.thumbnail_widget.loadThumbnails()
        self.tag_widget.update()

    def addTag(self, tag):
        self.currentImage().addTag(tag)

    def saveAllTags(self):
        for image in self.images:
            image.saveTags()

    def search(self, terms, max_results):

        # TODO: Replace _ with %20

        print("Starting Search")
        xml = self.flickr.photos.search(tags=terms, per_page=max_results)
        print("Returned from Flickr API")

        url = "https://farm{}.staticflickr.com/{}/{}_{}.jpg"
        farm_id = ""
        server_id = ""
        photo_id = ""
        secret = ""

        for photo in xml.iter('photo'):
            # TODO: Returns multiple copies of the same image. 
            # Maybe it's not iterating across photos correctly?
            farm_id = photo.get('farm')
            server_id = photo.get('server')
            photo_id = photo.get('id')
            secret = photo.get('secret')
            url = url.format(farm_id, server_id, photo_id, secret)
            print("Starting Network Request")
            request = QNetworkRequest(QUrl(url))
            self.netman.get(request)

    def requestFinished(self, reply):
        print("Network Request Finished")
        er = reply.error()
        if er == QNetworkReply.NoError:
            # TODO: Separate function to parse reply
            request_url = reply.request().url().toString() # => https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg
            # Farm id is between "farm" and .
            request_url = request_url.split('farm')[1] # => {farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg
            farm_id = request_url[0:request_url.find('.')]
            # Server id is then between / and /
            request_url = request_url[request_url.find('/'):] # => /{server-id}/{id}_{secret}.jpg
            server_id = request_url.split('/')[1]
            # Photo id is then between / and _
            # Trim leading / => {server-id}/{id}_{secret}.jpg
            request_url = request_url[1:]
            # Select after next /
            request_url = request_url.split('/')[1] # => {id}_{secret}.jpg
            photo_id = request_url[:request_url.find('_')]
            # Secret is then between _ and .
            secret = request_url[request_url.find('_'):request_url.find('.')][1:]

            file_name = "data/flickr_image_" + farm_id + server_id + photo_id + secret
            img_data = reply.readAll()
            img = Image(self, file_name, img_data)

            self.images.insert(self.selected_image_index, img)
            self.thumbnail_widget.loadThumbnails()
            self.tag_widget.update()
        else:
            print("HTTP Error {}".format(er))
