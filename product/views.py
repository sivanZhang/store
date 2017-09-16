#! -*- coding:utf-8 -*-
import pdb
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from category.models import Category
from product.models import AdaptorProduct
from common.fileupload import FileUpload
from django.utils.decorators import method_decorator
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser

dmb     = DetectMobileBrowser()

class ProductView(View):
    
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {} 
        products = AdaptorProduct.objects.all()
        content['products'] = products
        if 'new' in request.GET:
            if isMble:
                return render(request, 'm_new.html', content)
            else:
                return render(request, 'new.html', content)
        else:
            if isMble:
                return render(request, 'm_detail.html', content)
            else:
                return render(request, 'detail.html', content)

  
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
        """
        result = {}
        pdb.set_trace()
        
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
        if 'title' in request.POST and 'categoryid' in request.POST: 
            title = request.POST['title'].strip()
            categoryid = request.POST['categoryid'].strip()
             
            # 创建商品
            try:
                category = Category.objects.get(id=categoryid)  
                product = AdaptorProduct.objects.create(user=user, title=title, 
                          category=category)
                
                if 'unit' in request.POST:
                    unit = request.POST['unit'].strip()
                    product.unit = unit 
                if 'price' in request.POST:
                    price = request.POST['price'].strip()
                    product.price = price
                if 'parameters' in request.POST:
                    parameters = request.POST['parameters'].strip()
                    product.parameters = parameters
                if 'detail' in request.POST:
                    detail = request.POST['detail'].strip()
                    product.detail = detail
                
                product.save()

                result['id'] = product.id
                result['status'] ='ok'
                result['msg'] ='Done'
            except Category.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Category not found ID:{}'.format(categoryid)  
        else:
            result['status'] ='error'
            result['msg'] ='Need name in POST'
        return httpjson(result)

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
                        return httpjson(result)
                    
                if 'unit' in data:
                    unit = data['unit']
                    product.unit = unit
                if 'price' in data:
                    price = data['price']
                    product.price = price
                if 'parameters' in data:
                    parameters = data['parameters']
                    product.parameters = parameters 
                if 'detail' in data:
                    detail = data['detail']
                    product.detail = detail
                
                product.save() 
                result['status'] ='ok'
                result['msg'] ='Done'
            except AdaptorProduct.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the Product ID:{}'.format(productid) 
        else:
            result['status'] ='error'
            result['msg'] ='Need id  in POST'

        return httpjson(result)

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

        return httpjson(result)

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

        return httpjson(result)
 
    def httpjson(self, result):
        return HttpResponse(json.dumps(result), content_type="application/json")