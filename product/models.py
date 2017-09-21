#! -*- coding:utf-8 -*-
from django.db import models
from appuser.models import AdaptorUser as User 
from category.models import Category
from django.utils.translation import ugettext_lazy as _
from product.manager import AdaptorProductManager, AdaptorRuleManager
from basedatas.models import BaseDate, Pic

class Product(BaseDate):
    DRAFT = 0
    PUBLISHED = 1
    FALLDOWN = 2
    # 标题
    title = models.CharField(_('title'), max_length = 2048)
    # 描述
    description = models.TextField(null=True)
    # 创建者
    user = models.ForeignKey(User)
    # 可自定义的规则
    # json 数据
    parameters = models.TextField(_('Product Parameters'), null=True)
    # 默认0草稿状态
    # 1 已发布
    # 2 隐藏状态 对于暂时隐藏状态的产品不提供用户搜索，下单操作
    status = models.SmallIntegerField(default=DRAFT)
    # 详情
    detail = models.TextField(_('Detail'), null=True)
    # 所属类别
    category = models.ForeignKey(Category)
    thumbnail = models.CharField(_('thumbnail'), max_length = 2048, null=True)

    class Meta:
        abstract = True


class AdaptorProduct(Product):
    """Product 适配器""" 
    objects = AdaptorProductManager() 
    def __str__(self):
        return self.title  
 
class ProductPic(Pic): 
    """产品图片类"""
    SWIPER = 0
    DETAIL = 1
    product = models.ForeignKey(AdaptorProduct)
    # 默认0表示该图片是商品的轮播图图片
    # 1 详情页图片 
    type = models.SmallIntegerField(default=SWIPER)
    def __str__(self):
        return self.name  
     
 
class Rule(models.Model):
    """
    商品的规格：如：电脑商品 名称：8G/价格：6999/库存：100/单位：台
    """
    product = models.ForeignKey(AdaptorProduct)
    # 名称 ：8G
    name = models.CharField(_('name'), max_length=1024, null=True)
    # 价格:6999
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2, null=True)
    # 库存：100
    inventory = models.PositiveIntegerField(_('inventory'), default = 0, null=True)
    # 单位：台
    unit = models.CharField(_('unit'), max_length=128, null=True)

    class Meta:
        abstract = True
  
class AdaptorRule(Rule):
    """Rule 适配器"""
    objects = AdaptorRuleManager()
    def __str__(self):
        return self.name  

