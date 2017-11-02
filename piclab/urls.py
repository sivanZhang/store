from django.conf.urls import   url 
from piclab.views import PicLabView 
 
 
urlpatterns = [  
    url(r'^pics/$', PicLabView.as_view(), name='pics'),             
]