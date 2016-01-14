from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login/', views.loginuser, name='login'),
    url(r'register/', views.register, name='register'),
    url(r'logout/', views.logoutuser, name='logout'),
    url(r'user/(?P<uid>[0-9]+)$', views.userpage, name='userpage'),
]