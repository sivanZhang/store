"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('appuser.urls', namespace="users")),
    url(r'^category/', include('category.urls', namespace="category")),
    url(r'^product/', include('product.urls', namespace="product")),
    url(r'^shopcar/', include('shopcar.urls', namespace="shopcar")),
    url(r'^bill/', include('bill.urls', namespace="bill")),
    url(r'^sitecontent/', include('sitecontent.urls', namespace="sitecontent")),
    url(r'^address/', include('address.urls', namespace="address")),
    url(r'^area/', include('area.urls', namespace="area")),
    url(r'^comment/', include('comment.urls', namespace="comment")),
    url(r'^pic/', include('piclab.urls', namespace="piclab")),
    url(r'^apis/', include('apis.urls', namespace="apis")),
    
    url(r'^$', views.home, name='home'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
