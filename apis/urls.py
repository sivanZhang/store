from django.conf.urls import include, url 
from apis.views import ApisView 
 
 
urlpatterns = [  
    url(r'^apis/$', ApisView.as_view(), name='apis'),      
]
