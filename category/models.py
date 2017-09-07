#! -*- coding:utf-8 -*-
from django.db import models
from category.manager import CategoryManager

class Category(models.Model):
    name = models.CharField(max_length= 1024)
    # 分类
    level = models.IntegerField(default = 1)
    parent = models.ForeignKey('Category')
    objects = CategoryManager()

    def __str__(self):
        return self.name