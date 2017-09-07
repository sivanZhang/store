from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from basedatas import views

urlpatterns = [
    # Examples:
    url(r'^guide_l1$', views.guide_L1, name='guide_L1'),
    url(r'^guide_l2$', views.guide_L2, name='guide_L2'),
    url(r'^contact_us$', views.contact_us, name='contact_us'),  
    url(r'^user_register$', views.user_register, name='user_register'),  
    url(r'^find_password$', views.find_password, name='find_password'), 
    url(r'^reset_password$', views.reset_password, name='reset_password'), #reset password 
    url(r'^save_user$', views.save_user, name='save_user'),  
    url(r'^validate_username$', views.validate_username, name='validate_username'),
    url(r'^validate_uniqueness_email$', views.validate_uniqueness_email, name='validate_uniqueness_email'),
    url(r'^get_email_verify_code$', views.get_email_verify_code, name='get_email_verify_code'),
    url(r'^get_reset_pwd_verify_code$', views.get_reset_pwd_verify_code, name='get_reset_pwd_verify_code'),
    url(r'^new_day_words$', views.new_day_words, name='new_day_words'),
    url(r'^save_day_words/$', views.save_day_words, name='save_day_words'), #save
    url(r'^index_day_words/$', views.index_day_words, name='index_day_words'), #index_day_words 
    
    #add comment for day words.
    url(r'^add_comment/$', views.add_comment, name='add_comment'),
    url(r'^(?P<day_word_id>\d+)/go_comment/$', views.go_comment, name='go_comment'),
    url(r'^applications/$', views.applications, name='applications'),
]
