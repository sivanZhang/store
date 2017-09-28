from django.conf.urls import include, url 
from bill.views import BillView 
from bill import views

urlpatterns = [  
    url(r'^bills/$', BillView.as_view(), name='bills'),    
]
