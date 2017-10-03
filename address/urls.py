from django.conf.urls import include, url
from django.conf import settings
from django.contrib.auth.decorators import login_required
from address.views import AddressView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [  
    url(r'^addresses/$', csrf_exempt(login_required(AddressView.as_view())), name='addresses'),   
]
