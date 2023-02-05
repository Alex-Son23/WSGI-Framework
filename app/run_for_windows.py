from application.middleware import middlewares
from application.main import Application
from urls import urlpatterns
import os
from wsgiref.simple_server import make_server
from application.main import Application

settings = {
    'BASE_DIR': os.path.dirname(os.path.abspath(__file__)),
    'TEMPLATES_DIR_NAME': 'templates'
}

app = Application(
    urls  = urlpatterns,
    settings =  settings,
    middlewares=middlewares
)

with make_server('', 8080, app) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
