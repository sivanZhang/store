from django.conf.urls import include, url 
from sitecontent.views import BlockContentView, BlockItemContentView
from sitecontent import views
 
urlpatterns = [  
    url(r'^blockcontents/$', BlockContentView.as_view(), name='blockcontents'),       
    url(r'^blockitemcontents/$', BlockItemContentView.as_view(), name='blockitemcontents'),       
]
