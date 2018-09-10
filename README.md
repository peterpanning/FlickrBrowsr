A simple image browser built using PyQt5, a set of Python bindings for v5 of the Qt application framework from The Qt Company.

Uses Python3, the PyQt5 library, and the [flickrapi](https://stuvel.eu/flickrapi-doc/1-intro.html) python module, which requires Requests and Six. 

If necessary, install pip3 as appropriate for your package manager. 

May need pyopenssl to connect to flickr, use `pip install pyopenssl`. 

Install PyQt5 and the flickrapi using pip3, as in `pip install [package]`.

I found it unnecessarily difficult to develop this on Ubuntu as soon as it became necessary to make network calls. It appears that the version of OpenSSL which ships with Ubuntu is incompatible with the version required by Qt's Network Manager, and fixing this proved to be more trouble than it was worth. Therefore, although this was intended to be a cross-platform application, it must unfortunately come with the exception "except for Ubuntu." 