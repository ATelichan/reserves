from django.conf.urls import url

from . import views
app_name = 'event'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #event page
    url(r'^(?P<eid>[0-9]+)/$', views.eventpage, name='eventpage'),
    url(r'^(?P<eid>[0-9]+)/eventpage/$', views.eventpage, name='eventpage'),
    url(r'^(?P<eid>[0-9]+)/edit/$', views.editevent, name='editevent'),
    url(r'^(?P<eid>[0-9]+)/deletereservation/$', views.deletereservation, name='deletereservation'),
    url(r'^(?P<eid>[0-9]+)/deleteevent/$', views.deleteevent, name='deleteevent'),
    url(r'^(?P<eid>[0-9]+)/rss/$', views.rss, name='rss'),
    url(r'^create/$', views.createevent, name='createevent'),
    url(r'^tags/(?P<tag>.*)', views.tags, name='tags'),
]
