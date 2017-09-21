# -*- coding: utf-8 -*-
from django.db import models 
import os
      
class BaseDate(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

 

class Pic(models.Model):
    url = models.CharField(max_length=4096) 
    name = models.CharField(max_length=4096, default='') 
    class Meta:
        abstract = True
        db_table = 'pic'