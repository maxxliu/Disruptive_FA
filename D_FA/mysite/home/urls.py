from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^quick_search/$', views.quick_search, name='quick_search')
]
