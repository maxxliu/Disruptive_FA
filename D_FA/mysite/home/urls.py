from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^info/$', views.info, name='info'),
    url(r'^quick_search/$', views.quick_search, name='quick_search'),
    url(r'^advanced_search/$', views.advanced_search, name='advanced_search')
]
