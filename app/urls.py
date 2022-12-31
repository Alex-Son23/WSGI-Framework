from application.urls import Url
from view import Homepage, EpicMath, Hello, Contacts

urlpatterns = [
    Url('^$', Homepage),
    Url('^/math$', EpicMath),
    Url('^/hello$', Hello),
    Url('^/contacts', Contacts)
]