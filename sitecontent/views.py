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
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.utils.translation import ugettext as _

from sitecontent import models
from sitecontent.comm import handle_uploaded_file

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
dmb     = DetectMobileBrowser()

class BlockContentView(View):

    @method_decorator(login_required)
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {} 
        blocks = models.AdaptorBaseBlock.objects.all()
     
        content['blocks'] = blocks
        content['mediaroot'] = settings.MEDIA_URL
        if 'new' in request.GET:
            if isMble:
                return render(request, 'sitecontent/m_blocknew.html', content)
            else:
                return render(request, 'sitecontent/blocknew.html', content)

        if 'test' in request.GET:
            if isMble:
                return render(request, 'sitecontent/test.html', content)
            else:
                return render(request, 'sitecontent/test.html', content)
        if 'detail' in request.GET:
            if isMble:
                return render(request, 'sitecontent/m_detail.html', content)
            else:
                return render(request, 'sitecontent/m_detail.html', content)
        else:
            if isMble:
                return render(request, 'sitecontent/m_lists.html', content)
            else:
                return render(request, 'sitecontent/m_lists.html', content)

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self,request ): 
        if 'method' in request.POST:
            method = request.POST['method'].lower()
            if method == 'put':# 修改
                self.put(request)
                return   self.get(request)
            elif method == 'create': # 创建
                return self.create(request) 
            elif method == 'delete': # 删除
                return self.delete(request) 
        else:
            self.create(request)
            return self.get(request)

    def create(self, request):
        """创建""" 
        # 创建时：title字段是必须的,\url\pic\mark\status是可选字段
        user = request.user
        result = {} 
        
        if 'title' in request.POST : 
            title = request.POST['title'].strip() 

            # 创建Block 
            block = models.AdaptorBaseBlock.objects.create(user=user, title=title )
            
            if 'url' in request.POST  :
                url = request.POST['url'].strip()
                block.url = url
  
            if 'pic' in request.FILES:
                pic = request.FILES['pic'] 
                pic_url = handle_uploaded_file(pic, user.id)
                block.pic = pic_url
            
            if 'mark' in request.POST:
                mark = request.POST['mark'].strip() 
                if mark:
                    block.mark = mark
            
            if 'status' in request.POST:
                status = request.POST['status'].strip() 
                if status:
                    block.status = status
    
            block.save()
            result['id'] = block.id
            result['status'] ='ok'
            result['msg'] = _('Saved completely!') 
        else:
            result['status'] ='error'
            result['msg'] ='Need title  in POST'
        return self.httpjson(result)
    
    def put(self, request):
        """修改""" 
        # 修改时：blockid字段是必须的,title\url\pic\mark\status是可选字段
        user = request.user
        result = {}
        if 'blockid' in request.POST : 
            blockid = request.POST['blockid'].strip() 

            # 创建Block 
            block = models.AdaptorBaseBlock.objects.get(pk = blockid)
            
            if  'title' in request.POST  :
                title = request.POST['title'].strip()
                block.title = title
            
            if 'pic' in request.FILES:
                pic = request.FILES['pic'] 
                pic_url = handle_uploaded_file(pic, user.id)
                block.pic = pic_url

            if  'url' in request.POST  :
                url = request.POST['url'].strip()
                block.url = url
            
            if 'mark' in request.POST:
                mark = request.POST['mark'].strip() 
                if mark:
                    block.mark = mark
            
            if 'status' in request.POST:
                status = request.POST['status'].strip() 
                if status:
                    block.status = status
                 
            block.save()
            result['id'] = block.id
            result['status'] ='ok'
            result['msg'] = _('Saved completely!') 
        else:
            result['status'] ='error'
            result['msg'] ='Need title  in POST'
        return self.httpjson(result)

    def delete(self, request):
        user = request.user
        result = {}
        if 'id' in request.POST : 
            blockid = request.POST['id'].strip() 
            try:
                block = models.AdaptorBaseBlock.objects.get(pk = blockid)
                block.delete()
                result['status'] ='ok'
                result['msg'] = _('Done')
            except models.AdaptorBaseBlock.DoesNotExist:
                result['status'] ='error'
                result['msg'] = _('Not found')
        else:
            result['status'] ='error'
            result['msg'] = 'Need title  in POST'
        
        return self.httpjson(result)

    def httpjson(self, result):
        return HttpResponse(json.dumps(result), content_type="application/json")



class BlockItemContentView(View):
    @method_decorator(login_required)
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {}   
        content['mediaroot'] = settings.MEDIA_URL
        if 'blockid' in request.GET:
            blockid = request.GET['blockid'].strip()  
            try:
                block = models.AdaptorBaseBlock.objects.get(pk = blockid )
                content['block_instance'] = block
            except models.AdaptorBaseBlock.DoesNotExist:
                raise Http404
                
        if 'new' in request.GET:
            if isMble:
                return render(request, 'sitecontent/m_new.html', content)
            else:
                return render(request, 'sitecontent/new.html', content)
        
        if 'test' in request.GET:
            if isMble:
                return render(request, 'sitecontent/testitem.html', content)
            else:
                return render(request, 'sitecontent/testitem.html', content)

        if 'detail' in request.GET:
            if isMble:
                return render(request, 'sitecontent/m_detail.html', content)
            else:
                return render(request, 'sitecontent/m_detail.html', content)
       
        else:
            if isMble:
                return render(request, 'sitecontent/m_lists.html', content)
            else:
                return render(request, 'sitecontent/m_lists.html', content)

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self,request ):
        if 'method' in request.POST:
            method = request.POST['method'].lower()
            if method == 'put':# 修改
                self.put(request)
                return   self.get(request)
            elif method == 'delete': # 删除
                return self.delete(request) 
            elif method == 'create': # 创建
                return self.create(request) 
        else:
            self.create(request)
            return self.get(request)

    def create(self, request):
        """创建""" 
        # 创建时：blockid,title字段是必须的,\url\pic\mark\status是可选字段
        user = request.user
        result = {} 
        
        if 'blockid' in request.POST and 'title' in request.POST : 
            title = request.POST['title'].strip() 
            blockid = request.POST['blockid'].strip() 

            try:
                block = models.AdaptorBaseBlock.objects.get(pk = blockid )
                item = models.AdaptorBaseBlockItem.objects.create(block = block, title = title )
                if 'url' in request.POST  :
                    url = request.POST['url'].strip()
                    item.url = url
    
                if 'pic' in request.FILES:
                    pic = request.FILES['pic'] 
                    pic_url = handle_uploaded_file(pic, user.id)
                    item.pic = pic_url
                
                if 'mark' in request.POST:
                    mark = request.POST['mark'].strip() 
                    if mark:
                        item.mark = mark
                
                if 'status' in request.POST:
                    status = request.POST['status'].strip() 
                    if status:
                        item.status = status
        
                item.save()
                result['id'] = item.id
                result['status'] ='ok'
                result['msg'] = _('Saved completely!') 
            except models.AdaptorBaseBlock.DoesNotExist:
                result['status'] ='error'
                result['msg'] = _('Not found')
        else:
            result['status'] ='error'
            result['msg'] ='Need title  in POST'
        return self.httpjson(result)
    
    def put(self, request):
        """修改""" 
        # 修改时：blockid字段是必须的,title\url\pic\mark\status是可选字段
        user = request.user
        result = {}
        if 'itemid' in request.POST : 
            itemid = request.POST['itemid'].strip() 
 
            item = models.AdaptorBaseBlockItem.objects.get(pk = itemid)
            
            if  'title' in request.POST  :
                title = request.POST['title'].strip()
                item.title = title
            
            if 'pic' in request.FILES:
                pic = request.FILES['pic'] 
                pic_url = handle_uploaded_file(pic, user.id)
                item.pic = pic_url

            if  'url' in request.POST  :
                url = request.POST['url'].strip()
                item.url = url
            
            if 'mark' in request.POST:
                mark = request.POST['mark'].strip() 
                if mark:
                    item.mark = mark
            
            if 'status' in request.POST:
                status = request.POST['status'].strip() 
                if status:
                    item.status = status
                 
            item.save()
            result['id'] = item.id
            result['status'] ='ok'
            result['msg'] = _('Saved completely!') 
        else:
            result['status'] ='error'
            result['msg'] ='Need title  in POST'
        return self.httpjson(result)

    def httpjson(self, result):
        return HttpResponse(json.dumps(result), content_type="application/json")