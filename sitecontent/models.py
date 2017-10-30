
# -*- coding:utf-8 -*-
from django.db import models
from appuser.models import AdaptorUser as User

from sitecontent.manager import AdaptorSiteContentManager

class BaseBlock(models.Model):
    """
    模块,如：主轮播图、热销产品模块
    """
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    user = models.ForeignKey(User)
    # 模块展示时显示的图片
    pic = models.CharField(max_length = 1024, null= True)
    # 模块地址
    url = models.CharField(max_length = 1024, null = True) 
    # 模块名称
    title = models.CharField(max_length = 512) 
    # 模块状态：显示或隐藏
    status = models.SmallIntegerField(default = STATUS_SHOW) 
    # 标记被显示在什么位置：如主轮播图中
    mark = models.CharField(max_length = 128) 
    class Meta:
        abstract = True
        
class AdaptorBaseBlock(BaseBlock):
    objects = AdaptorSiteContentManager()
    

class BaseBlockItem(models.Model):
    """
    模块中的具体展示元素信息， 如主轮播图中的产品、热销产品模块中的产品
    """
    STATUS_SHOW = 1
    STATUS_HIDE = 0 
    block = models.ForeignKey(AdaptorBaseBlock) 
    # item展示时显示的图片
    pic = models.CharField(max_length = 1024 )
    # item详情地址
    url = models.CharField(max_length = 1024 ) 
    # item名称
    title = models.CharField(max_length = 512) 
    # item状态：显示或隐藏
    status = models.SmallIntegerField(default = STATUS_SHOW) 
    class Meta:
        abstract = True
     
class AdaptorBaseBlockItem(BaseBlockItem): 
    pass
    