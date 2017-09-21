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
from category.models import Category
from product.models import AdaptorProduct, AdaptorRule, ProductPic
from common.fileupload import FileUpload
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.comm import handle_uploaded_file

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser


dmb     = DetectMobileBrowser()


@login_required
@csrf_exempt
def change(request, pk):
    isMble  = dmb.process_request(request)
    content = {}
    content['mediaroot'] = settings.MEDIA_URL
    categories = Category.objects.all()  
    content['categories'] = categories

    if request.method == 'GET':
        try:
             product = AdaptorProduct.objects.get(pk=pk)
             content['product'] =product 
        except AdaptorProduct.DoesNotExist:
            raise Http404
        if 'pic' in request.GET:
            if isMble:
                return render(request, 'm_pic.html', content)
            else:
                return render(request, 'pic.html', content)
        else: 
            if isMble:
                return render(request, 'm_new.html', content)
            else:
                return render(request, 'new.html', content)

    return HttpResponse()
class ProductDetailView(APIView):
    """product detail"""
    model = AdaptorProduct
    def get_object(self, pk):
        try:
            return AdaptorProduct.objects.get(pk=pk)
        except AdaptorProduct.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        isMble  = dmb.process_request(request)
        
        content={
            'product':product
        }
        content['mediaroot'] = settings.MEDIA_URL
        if isMble:
            return render(request, 'm_detail.html', content)
        else:
            return render(request, 'detail.html', content)


    @method_decorator(csrf_exempt)
    def post(self, request, pk, format=None):
        product = self.get_object(pk)
         
        content={
            'product':product
        } 
        result = {}		 
        if request.method == 'POST': 
            user = request.user
            if 'method' in request.POST:
                method = request.POST['method']
                if method == 'delete':
                    picid = request.POST['picid']
                    productpic = ProductPic.objects.get(pk = picid)
                    productpic.delete()
                    result['status'] = 'OK'
                    result['msg']    = '删除成功...' 
            elif 'picid' in request.POST: # 说明是在设置主缩略图
                picid = request.POST['picid']
                productpic = ProductPic.objects.get(pk = picid)
                product.thumbnail = productpic.url 
                product.save()
                
                result['status'] = 'OK'
                result['msg']    = '设置成功...'
            else: 
                code    = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(4))
                filename = handle_uploaded_file(request.FILES['pic'], str(user.id)+'_'+ code)
                
                ProductPic.objects.create(product=product, url=filename.replace('\\', '/'))
                
                result['status'] = 'OK'
                result['msg']    = '上传成功...' 
        else:
            result['status'] = 'ERROR'
            result['msg']    = '请先选择图片..'
                  
        return HttpResponse(json.dumps(result), content_type='application/json')
         
   
class ProductView(View):
    
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {} 
        products = AdaptorProduct.objects.all()
        categories = Category.objects.all()
        
        content['products'] = products
        content['categories'] = categories
        content['mediaroot'] = settings.MEDIA_URL
        if 'new' in request.GET:
            if isMble:
                return render(request, 'm_new.html', content)
            else:
                return render(request, 'new.html', content)
        if 'test' in request.GET:
            if isMble:
                return render(request, 'm_new.html', content)
            else:
                return render(request, 'test.html', content)
        if 'pic' in request.GET:
            if isMble:
                return render(request, 'm_pic.html', content)
            else:
                return render(request, 'pic.html', content)
        else:
            if isMble:
                return render(request, 'm_lists.html', content)
            else:
                return render(request, 'lists.html', content)
 
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request):
        """
        新建产品
            下架：参数中带有method，并且值是'fallback'，大小写不敏感
                # # id【必须字段】：商品id 
            删除：参数中带有method，并且值是'delete'，大小写不敏感
                # # id【必须字段】：商品id 
            修改：参数中带有method，并且值是'put'，大小写不敏感
                # id【必须字段】：商品id 
                # title【可选字段】：商品名称 
                # categoryid【可选字段】： 商品所属类别ID 
                # unit【可选字段】： 商品的计量单位，如：个、只
                # price【可选字段】： 商品的计量单位，如：个、只
                # parameters【可选字段】： 商品的自定义规格，是一个寄送数据
                # detail【可选字段】： 商品的详情
            新建: 参数中带没有method，或method的值不等于put或者delete
                # title【必须字段】：商品名称 
                # categoryid【必须字段】： 商品所属类别ID 
                # unit【可选字段】： 商品的计量单位，如：个、只
                # price【可选字段】： 商品的计量单位，如：个、只
                # parameters【可选字段】： 商品的自定义规格，是一个寄送数据
                # detail【可选字段】： 商品的详情
        
        修改产品
        """
        result = {} 
        
        if 'method' in request.POST:
            method = request.POST['method'].lower()
            if method == 'put':# 修改
                return self.put(request)
            elif method == 'delete': # 删除
                return self.delete(request)
            elif method == 'fallback': # 下架
                return self.fallback(request)
            elif method == 'create': # 创建
                return self.create(request)
            elif method == 'detail_file': # 上传详情图片
                return HttpResponse('geu')
        else:
            return self.create(request)
        
    
    def create(self, request):
        """创建"""
        # 新建商品
        # title\category字段是必须的
        user = request.user
        result = {}
        if 'title' in request.POST and 'categoryid' in request.POST: 
            title = request.POST['title'].strip()
            categoryid = request.POST['categoryid'].strip()
   
            # 创建商品
            try:
                category = Category.objects.get(id=categoryid)  
                product = AdaptorProduct.objects.create(user=user, title=title, 
                          category=category)
       
                if 'detail' in request.POST:
                    detail = request.POST['detail'].strip()
                    product.detail = detail 
                if 'description' in request.POST:
                    description = request.POST['description'].strip()
                    product.description = description 
  
                if 'parameters' in request.POST:
                    parameters = request.POST['parameters'].strip() 
                    product.parameters = parameters
                if 'detail' in request.POST:
                    detail = request.POST['detail'].strip()
                    product.detail = detail
                if 'status' in request.POST:
                    status = request.POST['status'].strip()
                    product.status = status
                 
                if 'rules' in request.POST:  
                    rules = request.POST['rules'].strip()
                    AdaptorRule.objects.mul_create(rules, product)
                product.save()
                result['id'] = product.id
                result['status'] ='ok'
                result['msg'] ='Done'
            except Category.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Category not found ID:{}'.format(categoryid)  
        else:
            result['status'] ='error'
            result['msg'] ='Need title and categoryid in POST'
        return self.httpjson(result)

    def put(self, request):
        """
        修改分类名称
        """
        result = {}  
        data = QueryDict(request.body.decode('utf-8'))  
        if 'id' in data:
            productid = data['id']
            try:
                product = AdaptorProduct.objects.get(id=productid)
                if 'title' in data:
                    title = data['title']
                    product.title = title
                if 'categoryid' in data:
                    categoryid = data['categoryid']
                    try:
                        category = Category.objects.get(id = categoryid) 
                        product.category = category
                    except Category.DoesNotExist:
                        result['status'] = 'error' 
                        result['msg'] = 'Category not found, category id:{}'.format(categoryid) 
                        return self.httpjson(result)
                    
                if 'unit' in data:
                    unit = data['unit']
                    product.unit = unit
                if 'price' in data:
                    price = data['price']
                    product.price = price
                if 'parameters' in data:
                    parameters = data['parameters']
                    product.parameters = parameters 
                if 'description' in request.POST:
                    description = request.POST['description'].strip()
                    product.description = description 
                if 'detail' in data:
                    detail = data['detail']
                    product.detail = detail 
                if 'rules' in request.POST:  
                    product.adaptorrule_set.all().delete()
                    rules = request.POST['rules'].strip()
                    AdaptorRule.objects.mul_create(rules, product)
                
                product.save() 
                result['status'] ='ok'
                result['msg'] ='Done'
            except AdaptorProduct.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the Product ID:{}'.format(productid) 
        else:
            result['status'] ='error'
            result['msg'] ='Need id  in POST'

        return self.httpjson(result)

    def delete(self, request):
        """
        删除指定商品
        """
        result = {}
        data = QueryDict(request.body.decode('utf-8')) 
        if 'id' in data:
            productid = data['id'] 
            try: 
                product = AdaptorProduct.objects.get(id=productid)
                product.delete() 
                result['status'] ='ok'
                result['msg'] ='Done'
            except AdaptorProduct.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the id {}'.format(productid) 
        else:
            result['status'] ='error'
            result['msg'] ='Need id in POST'

        return self.httpjson(result)

    def fallback(self, request):
        """下架商品"""
        result = {}
        data = QueryDict(request.body.decode('utf-8')) 
        if 'id' in data:
            productid = data['id'] 
            try: 
                product = AdaptorProduct.objects.get(id=productid)
                AdaptorProduct.objects.fallback(product)
                result['status'] ='ok'
                result['msg'] ='Done'
            except AdaptorProduct.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the id {}'.format(productid) 
        else:
            result['status'] ='error'
            result['msg'] ='Need id in POST'

        return self.httpjson(result)
 
    def httpjson(self, result):
        return HttpResponse(json.dumps(result), content_type="application/json")
