from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from appuser import views_api   
from appuser import views_ui

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^usernames/(?P<username>\w{1,1024})$', views_api.usernames, name='usernames'),
    url(r'^emails/(?P<email>[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', views_api.email, name='email'),
    url(r'^emailscode/(?P<email>[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', views_api.emailscode, name='emailscode'),
    url(r'^emailscode/(?P<email>[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<code>[A-Z0-9a-z]{3,5})$', views_api.verify, name='verify'),
    url(r'^portrait/$', views_api.portrait, name='portrait'),
    url(r'^newgroup/$', views_api.newgroup, name='newgroup'),
    url(r'^grouplist/$', views_api.grouplist, name='grouplist'),
    url(r'^(?P<groupid>\d+)/modify_group/$', views_api.modify_group, name='modify_group'),
    #url(r'^modify_user/$', views_api.modify_user, name='modify_user'),
    url(r'^(?P<userid>\d+)/modify_user/$', views_api.modify_user, name='modify_user'),
    url(r'^list_users/$', views_api.list_users, name='list_users'),
    url(r'^admin_list_users/$', views_api.admin_list_users, name='admin_list_users'),
    url(r'^upload_fake_portrait/$', views_api.upload_fake_portrait, name='upload_fake_portrait'), 


    url(r'^login/$', views_ui.login, name='login'),  
    url(r'^register/$', views_ui.register, name='register'),  
    #url(r'^save_portrait/$', views.save_portrait, name='save_portrait'),#save portrait
]
