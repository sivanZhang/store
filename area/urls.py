from django.conf.urls import include, url
from area import views
urlpatterns = [
    url(r'^get_provice_list/$', views.get_provice_list, name="get_provice_list"),
    url(r'^get_city_list/$', views.get_city_list, name="get_city_list"),
    url(r'^get_county_list/$', views.get_county_list, name="get_county_list"),
    url(r'^set_locate_session/$', views.set_locate_session, name="set_locate_session"),
]