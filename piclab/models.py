#! -*- coding:utf-8 -*-
"""
图库
"""
import pdb

from django.db import models
from basedatas.models import  Pic

class DetailPic(Pic): 
    """全局图片类"""
    ref = models.SmallIntegerField(default=0) 
    def __str__(self):
        return self.name  
    
    class Meta:
        db_table = 'piclab'
        ordering = ('-id',)