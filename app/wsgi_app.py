from application.middleware import middlewares
from application.main import Application
from urls import urlpatterns
import os

settings = {
    'BASE_DIR': os.path.dirname(os.path.abspath(__file__)),
    'TEMPLATES_DIR_NAME': 'templates'
}

app = Application(
    urls  = urlpatterns,
    settings =  settings,
    middlewares=middlewares
)