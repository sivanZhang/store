from django.conf.urls import include, url 
from bill.views import BillView, BillDetailView, RabbitBillDetailView
from bill import views
 
urlpatterns = [  
    url(r'^bills/$', BillView.as_view(), name='bills'),   
    url(r'^bills/(?P<pk>[0-9]+)/$', BillDetailView.as_view(), name='detail'), 
    url(r'^bills/(?P<pk>[0-9]+)/rabbit$', RabbitBillDetailView.as_view(), name='rabbit'),     
]
