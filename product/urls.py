from django.conf.urls import include, url 
from product.views import ProductView


urlpatterns = [  
    url(r'^products/$', ProductView.as_view(), name='products'),   
]
