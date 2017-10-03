#! -*- coding:utf-8 -*-
import json
import pdb

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from address.models import Address
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
dmb     = DetectMobileBrowser()

class AddressView(View):
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {}
        addresses = Address.objects.filter(user = request.user)
        content['addresses'] = addresses
        if 'new' in request.GET:
            if isMble:
                return render(request, 'address/m_new.html', content)
            else:
                return render(request, 'address/new.html', content)
        if 'addressid' in request.GET:
            addressid = request.GET['addressid']
            try:
                address = Address.objects.get(user = request.user, id = addressid)
                content['address'] = address
                 
            except Address.DoesNotExist:
                pass
            if isMble:
                return render(request, 'address/m_new.html', content)
            else:
                return render(request, 'address/new.html', content)
        else: 
            return render(request, 'address/address.html', content)
    
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request):
        """
        新建地址名称
        """
        result = {}
        if 'method' in request.POST:
            method = request.POST['method'].lower()
            if method == 'put':# 修改
                return self.put(request)
            elif method == 'delete': # 删除
                return self.delete(request)
            
        # 新建类别
        # name字段是必须的；如果提供了parentid，则新的类别为parent类别的子类别
        # 否则添加为父类别
        if 'areaid' in request.POST and 'phone' in request.POST \
           and 'receiver' in request.POST and 'detail' in request.POST: 
            areaid = request.POST['areaid'].strip()
            phone = request.POST['phone'].strip()
            receiver = request.POST['receiver'].strip()
            detail = request.POST['detail'].strip() 
            address = Address.objects.create(user = request.user, area_id=areaid, phone=phone, 
                                           receiver=receiver, detail = detail)
            result['id'] = address.id
            result['status'] ='ok'
            result['msg'] ='保存成功'
        else:
            result['status'] ='error'
            result['msg'] ='Need name in POST'
   
        return HttpResponse(json.dumps(result), content_type="application/json")
    
    def put(self, request):
        """
        修改地址名称
        """
        result = {}  
        data = QueryDict(request.body.decode('utf-8')) 
        if 'id' in data:
            addressid = data['id']
            try:
                address = Address.objects.get(id=addressid)
                if 'areaid' in data:
                    areaid = data['areaid']
                    address.area_id = areaid
                if 'phone' in data:
                    phone = data['phone']
                    address.phone = phone
                if 'receiver' in data:
                    receiver = data['receiver']
                    address.receiver = receiver
                if 'detail' in data:
                    detail = data['detail']
                    address.detail = detail
                address.save()
             
                result['status'] ='ok'
                result['msg'] ='保存成功'
            except Address.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the id'
     
        else:
            result['status'] ='error'
            result['msg'] ='Need name and id  in POST'

        return HttpResponse(json.dumps(result), content_type="application/json")

    def delete(self, request):
        """
        删除指定地址
        """
        result = {}
        data = QueryDict(request.body.decode('utf-8')) 
        if 'id' in data:
            addressid = data['id'] 
            try: 
                address = Address.objects.get(id=addressid) 
                address.delete() 
                result['status'] ='ok'
                result['msg'] ='Done'
            except Address.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the id' 
        else:
            result['status'] ='error'
            result['msg'] ='Need id in POST'

        return HttpResponse(json.dumps(result), content_type="application/json")
