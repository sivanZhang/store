# -*- coding:utf-8 -*-
import json
import pdb
from django.shortcuts import render
from django.http      import HttpResponse
from area.models      import  Area
from django.db.models import Q
def serialize_areas(objs):
    results = []
    for obj in objs:
        result = {}
        result['id']         = obj.pk
        result['short_name'] = obj.short_name
        results.append(result)
    
    return json.dumps(results, ensure_ascii=False).encode('utf8')
        

def get_provice_list(request):
    provinces = Area.objects.filter(Q(level = 1) | Q(name='北京市'))
    return HttpResponse(serialize_areas(provinces), 
                content_type="application/json")

def get_city_list(request):
    provinceid = request.GET['provinceid']
    provinces = Area.objects.filter(parent_id = provinceid, level = 2)
    return HttpResponse(serialize_areas(provinces), 
                content_type="application/json")

def get_county_list(request):
    cityid = request.GET['cityid']
    provinces = Area.objects.filter(parent_id = cityid, level = 3)
    return HttpResponse(serialize_areas(provinces), 
                content_type="application/json")


def set_locate_session(request):
    selectid = request.GET['selectid']
    selectname = request.GET['selectname']
    request.session['locationid'] = selectid
    request.session['locationname'] = selectname
    return HttpResponse( 'ok' )


 