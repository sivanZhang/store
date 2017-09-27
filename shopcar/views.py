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
from product.models import AdaptorRule
from shopcar.models import CartItem

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser


dmb     = DetectMobileBrowser()

class ShopcarView(View):
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {} 
       
        content['mediaroot'] = settings.MEDIA_URL
         
        if isMble:
            return render(request, 'shopcar/m_lists.html', content)
        else:
            return render(request, 'shopcar/lists.html', content)


class ShopcarDetailView(APIView):

    method_decorator(login_required)
    def get(self, request,  format=None ):
        """获取某个用户的购物车列表"""
        isMble  = dmb.process_request(request)
        ruleitems = CartItem.objects.filter(user = request.user)
        content = {}  
        content['mediaroot'] = settings.MEDIA_URL
        content['ruleitems'] = ruleitems
         
        if isMble:
            return render(request, 'shopcar/m_lists.html', content)
        else:
            return render(request, 'shopcar/lists.html', content)
    
    @method_decorator(csrf_exempt)
    def post(self, request ):
        """
        创建、删除
        创建需要参数：method:create, ruleid, quantity
        """
        result = {} 
        if request.method == 'POST': 
            user = request.user
            if user.is_anonymous():
                result['status'] = 'ERROR'
                result['msg']    = '需要登录....'
            else:
                if 'method' in request.POST:
                    method = request.POST['method']
             
                    ruleid = request.POST['ruleid']
                    try:
                        rule = AdaptorRule.objects.get(id = ruleid)
                        if method == 'delete': 
                            caritem = CartItem.objects.get(rule = rule, user = user)
                            caritem.delete()
                            result['status'] = 'OK'
                            result['msg']    = '删除成功...' 
                        else :
                            # create 
                            quantity = request.POST['quantity']
                            car, create = CartItem.objects.get_or_create(rule = rule, user=user )
                            car.quantity += int(quantity )
                            car.save()
                            result['status'] = 'OK'
                            result['msg']    = '添加成功...' 
                    except AdaptorRule.DoesNotExist:
                        result['status'] = 'ERROR'
                        result['msg']    = '未找到商品....'
                
                else:   
                    result['status'] = 'ERROR'
                    result['msg']    = 'Need method in post...' 
        else:
            result['status'] = 'ERROR'
            result['msg']    = 'Method error..'
                  
        return HttpResponse(json.dumps(result), content_type='application/json')
         