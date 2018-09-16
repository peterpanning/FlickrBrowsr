import os
from Image import *
from TagWidgets import *
from SearchWidgets import *
import flickrapi
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import xml.etree.ElementTree as ET
from PyQt5.QtMultimedia import QSound
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
        # It can switch between two views: search or tag. 

        super().__init__()

        self.selected_image_index = 0
        self.images = []
        self.allResults = 0
        self.returnedResults = 0
        self.netman = QNetworkAccessManager()
        self.netman.finished.connect(self.requestFinished)
        self.clickedSound = QSound("assets/click.wav")
        self.errorSound = QSound("assets/error.wav")

        self.initData()
        self.initUI()
        self.show()


    def addTag(self, tag):
        self.currentImage().addTag(tag)


    def currentImage(self):
        if self.images:
            return self.images[self.selected_image_index]
        else:
            return None
    

    def handleDelete(self):
        if self.images:
            self.images[self.selected_image_index].delete()
            self.images.remove(self.images[self.selected_image_index])
            if self.selected_image_index == len(self.images) and len(self.images) != 0:
                self.selected_image_index = self.selected_image_index - 1
            self.search_view.loadThumbnails()
            self.tag_view.update()
    

    def initData(self, image_folder='./images'):

        file_names = sorted(os.listdir(image_folder))

        for file_name in file_names:
            if file_name == ".DS_Store":
                continue
            full_path = image_folder + "/" + file_name
            image = Image(self, full_path)
            self.images.append(image)

        xml = ET.parse('secrets.xml')
        # TODO: Read these secrets using keywords or something similar
        root = xml.getroot()
        api_key = root[0][0].text
        api_secret = root[0][1].text

        self.flickr = flickrapi.FlickrAPI(api_key, api_secret)
        

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

        self.search_view = SearchView(self)
        self.tag_view = TagView(self)

        self.addWidget(self.search_view)
        self.addWidget(self.tag_view)


    def keyPressEvent(self, event):

        # Controls what happens on keyboard input. Users may navigate through images via keyboard input

        key = event.key()

        if not self.images:
            return

        if key == Qt.Key_Left:
            self.selectPreviousImage()
            
        elif key == Qt.Key_Right:
            self.selectNextImage()

        elif key == Qt.Key_Return:
            if self.currentWidget() == self.search_view:
                self.setCurrentWidget(self.tag_view)
            else:
                self.setCurrentWidget(self.search_view)

        elif key == Qt.Key_Escape:
            if self.currentWidget() == self.tag_view:
                self.setCurrentWidget(self.search_view)

        elif key == Qt.Key_Comma or key == Qt.Key_PageUp:
            if self.currentWidget() == self.search_view:
                self.selectPreviousPage()
            else:
                self.errorSound.play()
        
        elif key == Qt. Key_Period or key == Qt.Key_PageDown:
            if self.currentWidget() == self.search_view:
                self.selectNextPage()
            else:
                self.errorSound.play()


    def requestFinished(self, reply):
        er = reply.error()
        self.returnedResults += 1
        if er == QNetworkReply.NoError:
            request_url = reply.request().url().toString() 
            # >>> https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg
            request_url = request_url.split('farm')[1] 
            # >>> {farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg
            farm_id = request_url[0:request_url.find('.')]
            request_url = request_url[request_url.find('/'):] 
            # >>> /{server-id}/{id}_{secret}.jpg
            server_id = request_url.split('/')[1]
            request_url = request_url[1:]
            request_url = request_url.split('/')[1] 
            # >>> {id}_{secret}.jpg
            photo_id = request_url[:request_url.find('_')]
            secret = request_url[request_url.find('_'):request_url.find('.')][1:]

            file_name = "./images/" + farm_id + server_id + photo_id + secret + ".jpg"
            img_data = reply.readAll()
            img = Image(self, file_name, img_data)

            self.images.append(img)
            if self.returnedResults == self.allResults:
                new_index = len(self.images) - self.allResults
                self.setSelectedImageIndex(new_index)
                self.search_view.loadThumbnails()
                self.tag_view.update()
        else:
            print("HTTP Error {}".format(er))


    def saveAllTags(self):
        for image in self.images:
            image.saveTags()


    def search(self, terms, max_results):
        xml = self.flickr.photos.search(tags=terms, per_page=max_results)
        farm_id = ""
        server_id = ""
        photo_id = ""
        secret = ""
        self.returnedResults = 0
        self.allResults = max_results

        for photo in xml.iter('photo'):
            # URL must be declared within the loop, or it won't be 
            # able to be formatted in subsequent iterations
            url = "https://farm{}.staticflickr.com/{}/{}_{}.jpg"
            farm_id = photo.get('farm')
            server_id = photo.get('server')
            photo_id = photo.get('id')
            secret = photo.get('secret')
            url = url.format(farm_id, server_id, photo_id, secret)
            self.urlRequest(url)


    def selectNextImage(self):
        self.setSelectedImageIndex(self.selected_image_index + 1)
        self.clickedSound.play()
        self.search_view.selectNextImage()
        self.tag_view.update()


    def selectNextPage(self):
        limit = min(len(self.images), self.max_thumbnails)
        self.setSelectedImageIndex(self.selected_image_index + limit)
        self.clickedSound.play()
        self.search_view.loadThumbnails()
        self.tag_view.update()


    def selectPreviousImage(self):
        self.setSelectedImageIndex(self.selected_image_index - 1)
        self.clickedSound.play()
        self.search_view.selectPreviousImage()
        self.tag_view.update()


    def selectPreviousPage(self):
        limit = min(len(self.images), self.max_thumbnails)
        self.setSelectedImageIndex(self.selected_image_index - limit)
        self.clickedSound.play()
        self.search_view.loadThumbnails()
        self.tag_view.update()


    def setSelectedImageIndex(self, new_index):
        num_images = len(self.images)
        if new_index < 0:
            self.selected_image_index = num_images + new_index
        elif new_index >= num_images:
            self.selected_image_index = new_index - num_images
        else:
            self.selected_image_index = new_index


    def urlRequest(self, url):
        print("Image URL: {}".format(url))
        request = QNetworkRequest(QUrl(url))
        self.netman.get(request)
