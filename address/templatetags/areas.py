#! -*- coding:utf-8 -*-
import pdb
from django import template
from area.models import Area

register = template.Library()
 
@register.filter
def areas(area):  
     
    city = Area.objects.get(id = area.parent_id)
    province = Area.objects.get(id = city.parent_id)
    string = province.short_name + '省 '+ city.short_name + '市 ' 
    return string
     