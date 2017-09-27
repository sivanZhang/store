from django.conf.urls import include, url 
from shopcar.views import ShopcarView 
from shopcar.views import ShopcarDetailView 
from shopcar import views

urlpatterns = [     
    url(r'^shopcars/$', ShopcarDetailView.as_view(), name='shopcar_detail'),     
]
