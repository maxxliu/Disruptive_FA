# url patterns for the quick search app include the index page, results page, 
# advanced search results page, and the thanks page

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results/$', views.results, name='results'),
    url(r'^advanced/$', views.advanced, name='advanced'),
    url(r'^thanks/$', views.thanks, name='thanks')
]