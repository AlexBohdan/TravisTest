from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^complete-auth/', complete_auth, name='complete_auth'),
]
