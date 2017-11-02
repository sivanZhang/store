#! -*- coding:utf-8 -*-
import pdb
from django import template
from django.utils.timezone import localtime
from datetime import datetime 

register = template.Library()

def assitant(obj):
    pdb.set_trace()
    tag_string = ''
    childs = obj.adaptorpagecomment_set.all()
    if childs.count() == 0:
        tag_string = '<li>{}</li>'.format(obj)
    else:
        tag_string += comment_hierarchy(obj)

    return tag_string

"""
 <ul class="reply_list">
        <li><span class="user-name">{{comment.user.username}}</span>回复<span class="user-name">{{comment.id}}</span>:</li>
        <li class="reply_text">{% if comment.adaptorpagecomment_set.all %} {% endif %}</li>
        <li class="grey_font"> {{comment.date| date:"Y-m-d"}}</li>
</ul>
"""
@register.filter
def comment_hierarchy(comment): 
    childs = comment.adaptorpagecomment_set.all()
     
    if childs.count() == 0:
        tag_string = '<ul class="reply_list" data-com-id="{0}">'.format(comment.id)
        tag_string += """<li><span class="user-name">{0}</span>回复
                     <span class="user-name">{1}</span>:</li>""".format(comment.user.username, comment.parent.user.username)
        
        tag_string += """<li class="reply_text">{0}</li>""".format(comment.content)
        tag_string += '<li class="txt_commenting">回复</li>'
        tag_string +='<li class="txt_delete">删除</li>'
        tag_string += """<li class="grey_font">{0} </li></ul>""".format(datetime.strftime(localtime(comment.date), '%Y-%m-%d %H:%M:%S') )
    else:
        tag_string  = '' 
        for child in childs:
            tag_string += comment_hierarchy(child)
        
    return tag_string