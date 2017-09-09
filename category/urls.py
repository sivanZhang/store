from django.conf.urls import include, url
from django.conf import settings
from django.contrib.auth.decorators import login_required
from category.views_ui import CategoryView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [  
    url(r'^categories/$', csrf_exempt(login_required(CategoryView.as_view())), name='categories'),   
]
