from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^info/$', views.info, name='info'),
    url(r'^step_1/$', views.step_1, name='step_1'),
    url(r'^step_2/$', views.step_2, name='step_2'),
    url(r'^step_3/$', views.step_3, name='step_3'),
    url(r'^step_4/$', views.step_4, name='step_4'),
    url(r'^step_5/$', views.step_5, name='step_5'),
    url(r'^step_6/$', views.step_6, name='step_6'),
    url(r'^step_7/$', views.step_7, name='step_7'),
    url(r'^step_8/$', views.step_8, name='step_8'),
    url(r'^quick_search/$', views.quick_search, name='quick_search'),
    url(r'^advanced_search/$', views.advanced_search, name='advanced_search')
]
