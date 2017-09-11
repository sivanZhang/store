# -*- coding: utf-8 -*-
from django.db import models 
import os
      
class BaseDate(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class Pic(models.Model):
    image = models.ImageField(upload_to=get_image_path) 
    class Meta:
        abstract = True
        db_table = 'pic'