# -*- coding: utf-8 -*-
from django.db import models

class Area(models.Model):
    parent_id = models.PositiveIntegerField(default = 0)
    short_name= models.CharField(u'简称', max_length=100) 
    name      = models.CharField(u'名称', max_length=100)
    longitude = models.DecimalField(u'经度', max_digits=10, decimal_places=6, default =0)
    latitude  = models.DecimalField(u'经度', max_digits=10, decimal_places=6, default =0)
    # 等级(1省/直辖市,2地级市,3区县,4镇/街道)
    level     = models.PositiveSmallIntegerField() 
    sort      = models.PositiveSmallIntegerField(default = 1 ) # 排序
    status    = models.PositiveSmallIntegerField(default = 0 ) # 状态(0禁用/1启用)

    def __unicode__(self):
        return self.short_name
    
    class Meta:
        db_table = 'area'
        #managed = False


