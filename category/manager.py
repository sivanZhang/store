#! -*- coding:utf-8 -*-
from django.db import models

class CategoryManager(models.Manager):
    '''
    Category model manager
    '''
    
    def get_children(self, parent_id):
        """
         获得parent的子类别
        """
        return self.filter(parent__id = parent_id)
    
    def get_brothers(self, item):
        """
        获取类别对象item的同级类别
        """
        return self.filter(level = item.level)

class AdaptorCategoryManager(CategoryManager):
    pass