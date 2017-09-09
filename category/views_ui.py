#! -*- coding:utf-8 -*-
import json
import pdb
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from category.models import Category
from django.http import QueryDict

class CategoryView(View):

    def get(self, request):
        content = {}
        categories = Category.objects.filter(level=1)
        content['categories'] = categories
        return render(request, 'category.html', content)

    def post(self, request):
        """
        新建分类名称
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
        if 'name' in request.POST : 
            name = request.POST['name'].strip()
            parentid = request.POST.get('parentid') 
            if parentid:
                # 创建顶级子类别
                try:
                    category = Category.objects.get(id=parentid) 
                    level = category.level
                    category = Category.objects.create(name=name, level=level+1, 
                    parent=category)
                    print('get u')
                    result['id'] = category.id
                    result['status'] ='ok'
                    result['msg'] ='Done'
                except Category.DoesNotExist:
                    result['status'] ='error'
                    result['msg'] ='404 Parent Category not found ID:{}'.format(parentid) 
            else:
                # 创建顶级类别
                category = Category.objects.create(name=name)
                result['id'] = category.id
                result['status'] ='ok'
                result['msg'] ='Done'
        else:
            result['status'] ='error'
            result['msg'] ='Need name in POST'
   
        return HttpResponse(json.dumps(result), content_type="application/json")
    
    def put(self, request):
        """
        修改分类名称
        """
        result = {}  
        data = QueryDict(request.body.decode('utf-8')) 
        if 'id' in data:
            categoryid = data['id']
            try:
                category = Category.objects.get(id=categoryid)
                if 'name' in data:
                    name = data['name']
                    category.name = name
                    category.save()
             
                result['status'] ='ok'
                result['msg'] ='Done'
            except Category.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the id'
     
        else:
            result['status'] ='error'
            result['msg'] ='Need name and id  in POST'

        return HttpResponse(json.dumps(result), content_type="application/json")

    def delete(self, request):
        """
        删除指定分类
        """
        result = {}
        data = QueryDict(request.body.decode('utf-8')) 
        if 'id' in data:
            categoryid = data['id'] 
            try:
                print(categoryid)
                category = Category.objects.get(id=categoryid) 
                category.delete() 
                result['status'] ='ok'
                result['msg'] ='Done'
            except Category.DoesNotExist:
                result['status'] ='error'
                result['msg'] ='404 Not found the id' 
        else:
            result['status'] ='error'
            result['msg'] ='Need id in POST'

        return HttpResponse(json.dumps(result), content_type="application/json")