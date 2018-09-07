from Image_Browser import *
import flickrapi
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
import xml.etree.ElementTree as ET

class FlickrEngine:

    def __init__(self):
        
        # Read api key and secret from xml file

        xml = ET.parse('secrets.xml')
        root = xml.getroot()
        
        api_key = root[0][0].text
        api_secret = root[0][1].text

        self.flickr = flickrapi.FlickrAPI(api_key, api_secret)
        self.netman = QNetworkAccessManager()


    def search(self, terms, max):
        url = "https://farm{}.staticflickr.com/{}/{}_{}.jpg"
        xml = self.flickr.photos.search(tags=terms, per_page=max)
        farm_id = ""
        server_id = ""
        photo_id = ""
        secret = ""
        results = []

        for photo in xml.iter('photo'):
            photo_id = photo.get('id')
            server_id = photo.get('server')
            farm_id = str(photo.get('farm'))
            secret = photo.get('secret')
            url = url.format(farm_id, server_id, photo_id, secret)
            qurl = QUrl(url)
            request = QNetworkRequest(qurl)
            response = self.netman.get(request)
            # TODO: Open and read the response, expand Image implementation for reading from an I/O device
            results.append(response)
        print(results)

    def download(self, urls):
        pass
        