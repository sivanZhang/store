from django.conf.urls import   url 
from comment.pageviews import PageCommentView 
 
 
urlpatterns = [  
    url(r'^comment/$', PageCommentView.as_view(), name='comment'),             
]