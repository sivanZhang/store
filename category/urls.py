from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
  
from category import views_ui

urlpatterns = [ 
    url(r'^manage/$', views_ui.manage, name='manage'), 
    url(r'^categories/$', views_ui.manage, name='manage'),   
]
