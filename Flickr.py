from Image_Browser import *
import flickrapi
import xml.etree.ElementTree as ET

class Flickr:

    def __init__(self):
        
        # Read api key and secret from xml file

        xml = ET.parse('secrets.xml')
        root = xml.getroot()
        
        api_key = root[0][0].text
        api_secret = root[0][1].text

        flickr = flickrapi.FlickrAPI(api_key, api_secret)

    def search(self, terms, max):   
        return flickrapi.photos.search(tags=terms, per_page=max)
        