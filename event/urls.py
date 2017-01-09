from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^list/', event_list, name='event_list'),
    url(r'^ajax_event/', ajax_event, name='ajax_event'),
    url(r'^map/', map, name='event_map'),
    url(r'^get_create_form/', get_create_form, name='get_create_form'),
    url(r'^add_event/', add_event, name='add_event'),
    url(r'^all-markers/', all_markers, name='all_markers'),
    url(r'^get_marker_content/', get_marker_content, name='get_marker_content'),
]
