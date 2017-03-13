# url patterns for the risk survey app include index page, scored page, and 
# reset page

from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^scored/$', views.scored, name='scored'),
	url(r'^reset/$', views.reset, name='reset')
]

