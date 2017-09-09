#! -*- coding:utf-8 -*-
import pdb
from django import template

register = template.Library()

def assitant(obj):
    string = ''
    childs = obj.category_set.all()
    if childs.count() == 0:
        string = '<li>{}</li>'.format(obj)
    else:
        string += hierarchy(obj)

    return string


@register.filter
def hierarchy(unit): 
    childs = unit.category_set.all()
    if childs.count() == 0:
        string = '<li categoryid="{0}" level="{1}">{2}</li>'.format(unit.id, unit.level, unit)
    else:
        string = '<li categoryid="{0}" level="{1}">{2}<ul>'.format(unit.id, unit.level, unit)
        for child in childs:
            string += hierarchy(child)
        string += '</ul></li>'
    return string