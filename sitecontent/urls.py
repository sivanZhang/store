from django.conf.urls import include, url 
from sitecontent.views import SitecontentView 
from sitecontent import views
 
urlpatterns = [  
    url(r'^sitecontents/$', SitecontentView.as_view(), name='sitecontents'),       
]
