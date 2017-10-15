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
from bill.models import AdaptorBill, AdaptorBillItem
from product.models import AdaptorRule, AdaptorProduct
from django.utils.translation import ugettext as _
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
from rabbitmq.publisher import Publisher

dmb     = DetectMobileBrowser()

   
class BillView(View):
    
    @method_decorator(login_required)
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {} 
        bills = AdaptorBill.objects.filter(owner = request.user)
        content['bills'] = bills
        if 'new' in request.GET:
            if isMble:
                return render(request, 'bill/m_new.html', content)
            else:
                return render(request, 'bill/new.html', content)
        if 'test' in request.GET:
            if isMble:
                return render(request, 'm_new.html', content)
            else:
                return render(request, 'test.html', content)
        if 'detail' in request.GET:
            if isMble:
                return render(request, 'bill/m_detail.html', content)
            else:
                return render(request, 'bill/m_detail.html', content)
        if 'unpayed' in request.GET:
            # 给客户展示订单支付页面
            # 需要订单号
            if 'billno' in request.GET:
                billno = request.GET['billno']
                try:
                    bill = AdaptorBill.objects.get(no = billno, owner = request.user)
       
                    content['bill'] = bill
                except AdaptorBill.DoesNotExist:
                    content['bill'] = False
                    content['error'] = _("Not Found...") 
            else:
                content['error'] = _("Need billno, Not Found...")
            if isMble:
                return render(request, 'bill/m_unpayed.html', content)
            else:
                return render(request, 'bill/m_unpayed.html', content)
        else:
            if isMble:
                return render(request, 'bill/m_lists.html', content)
            else:
                return render(request, 'bill/m_lists.html', content)
    
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request):
        """
        新建: 参数中带没有method，或method的值不等于put或者delete
                # phone【必须字段】： 收货人电话
                # reciever【必须字段】： 收货人 
                # area【可选字段】：有的有地址，有的没有地址，所以这个不是必须的
                # address【可选字段】：订单收货地址的详细地址
                # items 【必须字段】订单中商品
                     items['rule'] : 必填，规格id
                     items['num'] : 必填，数量  

        取消订单：参数中带有method，并且值是'cancel'，大小写不敏感
                # # id【必须字段】：订单id 

        删除：参数中带有method，并且值是'delete'，大小写不敏感
                # # id【必须字段】：订单id 

        修改：参数中带有method，并且值是'put'，大小写不敏感 
        """
        result = {} 
        
        if 'method' in request.POST:
            method = request.POST['method'].lower()
            if method == 'put':# 修改
                return self.put(request)
            elif method == 'delete': # 删除
                return self.delete(request)
            elif method == 'cancel': # 取消
                return self.cancel(request)
            elif method == 'create': # 创建
                return self.create(request)
            elif method == 'detail_file': # 上传详情图片
                return HttpResponse('geu')
        else:
            return self.create(request)

    def create(self, request):
        """创建"""
        # 新建订单
        # title\category字段是必须的
        user = request.user
        result = {}
        if  'address_id' in request.POST   and 'items' in request.POST  :   
            
            items_str = request.POST['items']
            items = json.loads(items_str) 
            if len(items) > 0:
                # 创建订单 
                bill = AdaptorBill.objects.createbill(request.POST, user) 
                for item in items:
                    try:
                        rule = AdaptorRule.objects.get(pk = item['ruleid'])
                        item['rule'] = rule
                    except AdaptorRule.DoesNotExist:
                        result['status'] ='error'
                        result['msg'] ='订单创建失败，未找到商品...' 
                        bill.delete()
                        return  self.httpjson(result)
                
                # 创建订单分表
                AdaptorBillItem.objects.createitem(bill, items)
                
                # 提交到queue中
                q_bill={}
                q_bill['billid'] = bill.id 
                q_bill['items'] = items_str
                p = Publisher()
                p.publish_message('store_exchange', json.dumps(q_bill), 'msg_avail')
                p.close_connection()

                result['id'] = bill.id
                result['status'] ='ok'
                result['msg'] ='创建成功...' 
            else:
                result['status'] ='error'
                result['msg'] ='Need items in POST' 
        else:
            result['status'] ='error'
            result['msg'] ='Need  items in POST'
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
        删除指定订单
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

    def cancel(self, request):
        """取消订单"""
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

class RabbitBillDetailView(APIView):
    """bill detail"""
    model = AdaptorBill
    def get_object(self, pk):
        try:
            return AdaptorBill.objects.get(pk=pk)
        except AdaptorBill.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        bill = self.get_object(pk)
        isMble  = dmb.process_request(request)
        
        content = {}
        if bill.status == AdaptorBill.STATUS_SUBMITTED: 
            rules = []
            for item in bill.adaptorbillitem_set.all():
                item.product_title = item.product.title
                item.rule_title = item.rule.name
                item.save()
                rule = {}
                rule['ruleid'] = item.rule.id
                rule['num'] = item.num
                rules.append(rule)
            
            # 减可用库存
            result = AdaptorRule.objects.inventory_op(rules=rules, 
                                                    op_type=AdaptorRule.objects.OP_REDUCE, 
                                                    reduce_type=AdaptorRule.OP_REDUCE_TYPE_AVAIL)
            if result['status'] == 'ok':
                bill.status = AdaptorBill.STATUS_UNPAYED
                bill.save()
            else:
                # 减库存失败，存储失败状态和原因
                bill.status = AdaptorBill.STATUS_FAILED
                bill.errromsg = result['msg']
                bill.save()

            content = result
        elif bill.status == AdaptorBill.STATUS_UNPAYED:
            content['status'] = 'error'
            content['msg'] = '订单已提交成功，无需再次提交...'
        return HttpResponse(json.dumps(content), content_type='application/json')


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
            result['msg']    = 'Method error..'
                  
        return HttpResponse(json.dumps(result), content_type='application/json')

class BillDetailView(APIView):
    """bill detail"""
    model = AdaptorBill
    def get_object(self, pk):
        try:
            return AdaptorBill.objects.get(pk=pk)
        except AdaptorBill.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        bill = self.get_object(pk)
        isMble  = dmb.process_request(request)
        
        content={
            'bill':bill
        }
        content['mediaroot'] = settings.MEDIA_URL
        if 'status' in request.GET:
            # 查询订单状态
            result = {
                'status':'ok',
                'billstatus' : bill.get_status_display(),
                'billmsg' : bill.errromsg,
                'billno' : bill.no
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
        if isMble:
            return render(request, 'bill/m_lists_products.html', content)
        else:
            return render(request, 'bill/m_lists_products.html', content)


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
            result['msg']    = 'Method error..'
                  
        return HttpResponse(json.dumps(result), content_type='application/json')
         