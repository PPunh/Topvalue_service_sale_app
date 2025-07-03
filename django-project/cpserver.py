'''
- This script replaces Django's built-in development server with a production-ready CherryPy web server.
- It handles the deployment of a Django application in a production environment.
- It gives the option to serve static files through CherryPy, or WhiteNoise. This template default to WhiteNoise.
'''

import os
from pathlib import Path
import cherrypy
import django
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# tells where to find Django settings, load settings.py in the same dir
os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'

# initializes Django and loads the settings specified by DJANGO_SETTINGS_MODULE above
django.setup()

# Wrap WSGI application with Whitenoise for static file serving
application = WhiteNoise(get_wsgi_application())

# run server using CherryPy as web server
class DjangoApplication(object):
    # Accept connections on all available IPv4 addresses of the host machine
    HOST = "0.0.0.0"

    # web server to listen and respone on port 8000
    PORT = 8000

    def run(self):
        # Configures CherryPy with host, port, SSL certificates, and logging
        cherrypy.config.update({
            'server.socket_host': self.HOST,
            'server.socket_port': self.PORT,
            'server.ssl_module': 'pyopenssl',
            'server.ssl_certificate': '/django-project/certs/cpserver_ssl.cert',
            'server.ssl_private_key': '/django-project/certs/cpserver_ssl.key',
            'engine.autoreload_on': True,
            'log.screen': True,
        })
        # pyopenssl: function of pyOpenSSL lib in requirement file
        # engine.autoreload_on: automatically reloads the server when code changes.
        # log.screen: display in text in console window

        # uncomment below line to serve static file via cherrypy instead of WhiteNoise
        # self.mount_static(settings.STATIC_URL, settings.BASE_DIR)

        cherrypy.log("Loading and serving Django application")

        # Mounts the Django application to CherryPy, allowing it to handle Django requests
        cherrypy.tree.graft(application)

        # Starts the CherryPy server
        cherrypy.engine.start()

        # Keeps the server running
        cherrypy.engine.block()

# that the server starts only when the script is executed directly
if __name__ == "__main__":
    DjangoApplication().run()

'''
you can also use cherrypy to server static files (param url: Relative url,
param root: Path to static files root), in our case, this template, we are
using WhiteNoise middleware to server static files instead. and uncommened the line
self.mount_static(settings.STATIC_URL, settings.BASE_DIR). if you want to
use CherryPy to serve static files, then use code below and disable WhiteNoise.

    def mount_static(self, url, root):
        config = {
            'tools.staticdir.on': True,
            'tools.staticdir.root': root,
            'tools.staticdir.dir': 'static',
            'tools.expires.on': True,
            'tools.expires.secs': 86400,
            'tools.staticdir.debug': True, # should also be false in production
        }
        cherrypy.tree.mount(None, url, {'/': config})
'''
