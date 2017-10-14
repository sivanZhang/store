from django.conf.urls import include, url 
from shopcar.views import ShopcarView   
from shopcar import views

urlpatterns = [     
    url(r'^shopcars/$', ShopcarView.as_view(), name='shopcar_detail'),     
]
