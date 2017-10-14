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
from django.utils.translation import ugettext as _
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


class ShopcarView(APIView):

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
        创建需要参数：method:create, ruleid, num
        """
        result = {} 
        if request.method == 'POST': 
            user = request.user
            if user.is_anonymous():
                result['status'] = 'ERROR'
                result['msg']    = _('login required....')
            else:
                if 'method' in request.POST:
                    method = request.POST['method']
             
                    ruleid = request.POST['ruleid']
                    try:
                        rule = AdaptorRule.objects.get(id = ruleid)
                
                        if method == 'delete': 
                            caritem = CartItem.objects.get(rule = rule, user = user)
                            caritem.delete()
                            result['status'] = 'ok'
                            result['msg']    = _('Delete successfully....')#'删除成功...' 
                        else :
                            # create 
                            quantity = request.POST['num']
                            car, create = CartItem.objects.get_or_create(rule = rule, user=user )
                            car.quantity += int(quantity )
                            car.save()
                            result['status'] = 'ok'
                            result['msg']    = _('Add successfully....') # '添加成功...' 
                    except AdaptorRule.DoesNotExist:
                        result['status'] = 'error'
                        result['msg']    = _('Not found....') #'未找到商品....'
                
                else:   
                    result['status'] = 'error'
                    result['msg']    = _('Need method in post...') 
        else:
            result['status'] = 'error'
            result['msg']    = _('Method error..')
                  
        return HttpResponse(json.dumps(result), content_type='application/json')
         