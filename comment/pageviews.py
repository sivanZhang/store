#! -*- coding:utf-8 -*-
import pdb
import json
import random
import string
import os
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.http import Http404, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.conf import settings
from django.utils.translation import ugettext  as _

from comment.models import AdaptorPageComment, PageAdaptor
#from product.models import AdaptorProduct as PageAdaptor
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
dmb     = DetectMobileBrowser()
class PageCommentView(View):

    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {} 
        if 'id' in request.GET:
            pageid = request.GET['id']
            comments = AdaptorPageComment.objects.filter(page__id = pageid, parent__isnull= True)
            content['comments'] = comments

        if 'new' in request.GET:
            if isMble:
                return render(request, 'm_new.html', content)
            else:
                return render(request, 'new.html', content)
        if 'test' in request.GET:
            if isMble:
                return render(request, 'm_new.html', content)
            else:
                return render(request, 'comment\comment.1.html', content) 
        else:
            if isMble:
                return render(request, 'comment\comment.html', content)
            else:
                return render(request, 'comment\comment.html', content)

    
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request):
        """
        新建Comment
            删除：参数中带有method，并且值是'delete'，大小写不敏感
                # # id【必须字段】：Comment id 
            新建: 参数中带没有method，或method的值不等于put或者delete
                # id【必须字段】：page id ,如，产品id或者文章id等
                # content【必须字段】：Comment 内容   
        """ 
        
        if 'method' in request.POST:
            method = request.POST['method'].lower()
            if method == 'delete': # 删除
                return self.delete(request) 
            elif method == 'create': # 创建
                return self.create(request) 
            else:
                return self.create(request)
        else:
            return self.create(request)
    
    def create(self, request):
        """创建"""
        # 新建Comment
        # content\id字段是必须的
        user = request.user
        result = {}
        if 'content' in request.POST and 'id' in request.POST: 
            content = request.POST['content'].strip()
            id = request.POST['id'].strip()
             
            # 创建Comment
            try: 
                page = PageAdaptor.objects.get(pk=id)  
                pagecomment = AdaptorPageComment.objects.create(user=user, content=content, 
                          page=page)
                if 'rating' in request.POST:
                    rating = request.POST['rating'].strip()
                    pagecomment.rating = int(rating)
                    pagecomment.save()

                if 'parentid' in request.POST:
                    # 这条评论是回复别人的评论，parentid代表上一条评论的ID
                    parentid = request.POST['parentid'].strip()
                    if len(parentid) > 0:
                        try:
                            parent = AdaptorPageComment.objects.get(pk=parentid)
                            pagecomment.parent = parent
                            pagecomment.type = AdaptorPageComment.COMMENT_REPLAY
                            pagecomment.save()
                            result['id'] = pagecomment.id
                            result['status'] ='ok'
                            result['msg'] = _('Saved') +' ' + _('Complately')

                        except AdaptorPageComment.DoesNotExist:
                            pagecomment.delete()
                            result['status'] ='error'
                            result['msg'] = _('404 Parent comment not found.') 
                    else:
                        pagecomment.delete()
                        result['status'] ='error'
                        result['msg'] = 'parentid' + _(' cannot be null.')
                else: 
                    result['id'] = pagecomment.id
                    result['status'] ='ok'
                    result['msg'] = _('Saved') +' ' + _('Complately')
                    
            except AdaptorPageComment.DoesNotExist:
                result['status'] ='error'
                result['msg'] = _('404 Page not found ID:{}'.format(id) ) 
        else:
            result['status'] ='error'
            result['msg'] ='Need content and id in POST'

        return self.httpjson(result)
    
    def delete(self, request):
        """
        删除指定Comment
        """
        result = {}
        data = request.POST
        if 'id' in data:
            commentid = data['id']  
            try: 
                pagecomment = AdaptorPageComment.objects.get(id=commentid)
                pagecomment.delete() 
                result['status'] ='ok'
                result['msg'] = _('Done')
            except AdaptorPageComment.DoesNotExist:
                result['status'] ='error'
                result['msg'] = _('404 Not found the id {}'.format(commentid) )
        else:
            result['status'] ='error'
            result['msg'] = _('Need id in POST')

        return self.httpjson(result)
    
    def httpjson(self, result):
        return HttpResponse(json.dumps(result), content_type="application/json")