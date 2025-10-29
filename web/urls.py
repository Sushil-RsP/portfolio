# contact/urls.py

'''
from django.urls import path
from .views import contact_view

urlpatterns = [
    path('contact', contact_view, name='contact'),
]'''

from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_view, name='contact'),  # Homepage points to contact view
    path('projects', views.projects_view, name='projects'),  # All projects page
]