import os
from django.core.wsgi import get_wsgi_application
import django.core.handlers.wsgi
from cheroot.wsgi import Server as CherryPyWSGIServer

os.environ['DJANGO_SETTINGS_MODULE'] = 'configs.settings'

django.setup()
application = get_wsgi_application()

if __name__ == "__main__":
    server = CherryPyWSGIServer(
            ('0.0.0.0', 8000),
            application,
            #django.core.handlers.wsgi.WSGIHandler(),
            # server_name='www.django.example',
            numthreads=20,
    )
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
