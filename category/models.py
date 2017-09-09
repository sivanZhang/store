#! -*- coding:utf-8 -*-
from django.db import models
from category.manager import AdaptorCategoryManager

class Category(models.Model):
    """类别模型"""
    TOP_LEVEL = 1

    name = models.CharField(max_length = 1024)
    # 分类
    level = models.IntegerField(default = TOP_LEVEL)
    
    # 顶级分类可以没有父类别
    parent = models.ForeignKey('Category', on_delete=models.CASCADE , null = True)
    objects = AdaptorCategoryManager()

    def __str__(self):
        return self.name
