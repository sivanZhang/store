from django.shortcuts import render
import pdb
import json
import random
import string
import os
from datetime import datetime
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponse
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
from django.views.decorators.csrf import csrf_exempt
from apis.models import AdaptorApis
dmb     = DetectMobileBrowser()

   
class ApisView(View):
    
    @method_decorator(login_required)
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {} 
        apis = AdaptorApis.objects.filter()
        content['apis'] = apis
        if 'new' in request.GET:
            if isMble:
                return render(request, 'apis/m_new.html', content)
            else:
                return render(request, 'apis/new.html', content) 
        else:
            if isMble:
                return render(request, 'apis/m_lists.html', content)
            else:
                return render(request, 'apis/m_lists.html', content)
    
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request):
        """
     
        """
        result = {} 
        
        if 'method' in request.POST:
            method = request.POST['method'].lower() 
            if method == 'delete': # 删除
                return self.delete(request) 
            elif method == 'create': # 创建
                return self.create(request) 
        else:
            return self.create(request)

    def create(self, request):
        """创建"""
        
        user = request.user
        result = {}
        if  'url' in request.POST   and 'remark' in request.POST  :   
            
            url = request.POST['url']
            remark = request.POST['remark']
         
            AdaptorApis.objects.create(url=url,  remark=remark)
             
            result['status'] ='ok'
            result['msg'] ='创建成功...' 
             
        else:
            result['status'] ='error'
            result['msg'] ='Need url  and remark in POST'
        return self.get( request)

    

    def delete(self, request):
        """
        删除指定订单
        """
        result = {} 
        data = request.POST
        if 'id' in data:
            apiid = data['id'] 
            try: 
                api = AdaptorApis.objects.get(id=apiid)
                api.delete() 
                result['status'] ='ok'
                result['msg'] ='Done'
            except AdaptorApis.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the id {}'.format(apiid) 
        else:
            result['status'] ='error'
            result['msg'] ='Need id in POST'

        return self.httpjson(result)
    def httpjson(self, result):
        return HttpResponse(json.dumps(result), content_type="application/json")
 