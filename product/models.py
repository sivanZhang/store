#! -*- coding:utf-8 -*-
import threading
import pdb

from django.db import models
from appuser.models import AdaptorUser as User 
from category.models import Category
from django.utils.translation import ugettext_lazy as _
from product.manager import AdaptorProductManager, AdaptorRuleManager
from basedatas.models import BaseDate, Pic
from django.db.models import F

"""
全局锁，锁住的时候，不允许进行任何库存的写操作
"""
 

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
        permissions = (
            'manage_product', _('Permission to manage product')
        )
    def fallback(self ):
        """下架商品"""
        self.status = self.FALLDOWN
        self.save()

    def publish(self):
        """发布商品， 商品上架"""
        self.status = self.PUBLISHED
        self.save()

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
    OP_REDUCE_TYPE_AVAIL = 0 # 减可用库存
    OP_REDUCE_TYPE_REAL = 1  # 减物理库存
    OP_REDUCE_TYPE_ALL = 2   # 同时减少可用库存和物理库存
    
    product = models.ForeignKey(AdaptorProduct)
    # 名称 ：8G
    name = models.CharField(_('name'), max_length=1024, null=True)
    # 价格:6999
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2, null=True)

    # 如果可以随便增加、删除库存，那么没有办法核对库存信息。
    # 要可以核对库存信息，则还需要完善的入库操作
    # 物理库存：100
    real_inventory = models.PositiveIntegerField(_('real inventory'), default = 0, null=True)
    # 可用库存：100
    available_inventory = models.PositiveIntegerField(_('available inventory'), default = 0, null=True)

    # 单位：台
    unit = models.CharField(_('unit'), max_length=128, null=True)
     
    def _reduce(self,  num, inventory_type = OP_REDUCE_TYPE_AVAIL):
        """
        减少库存
        inventory_type表示减少库存的类型，当=0时，代表减少可用库存
        =1 时代表减少物理库存
        """ 
        status = {} 
        # 减库存
        if inventory_type == self.OP_REDUCE_TYPE_AVAIL:
            # 减可用库存
            
            if self.available_inventory - num < 0:
                status['result'] = 'error'
                status['msg'] = '错误：可用库存不足'
            else: 
                self.available_inventory = F('available_inventory') - num
                self.save()
                status['result'] = 'ok'
                status['msg'] = 'Done'
        elif inventory_type == self.OP_REDUCE_TYPE_REAL:
            # 减物理库存
            if self.real_inventory - num < 0:
                status['result'] = 'error'
                status['msg'] = '错误：物理库存不足'
            else:
                self.real_inventory = F('real_inventory') - num
                self.save()
                status['result'] = 'ok'
                status['msg'] = 'Done'
        elif inventory_type == self.OP_REDUCE_TYPE_ALL:
            # 同时减少可用库存和物理库存
            # 减物理库存
            if self.real_inventory - num < 0 or self.available_inventory - num < 0:
                status['result'] = 'error'
                status['msg'] = '错误：库存不足'
            else:
                self.available_inventory = F('available_inventory') - num
                self.real_inventory = F('real_inventory') - num
                self.save()
                status['result'] = 'ok'
                status['msg'] = 'Done'
        else:
            status['result'] = 'error'
            status['msg'] = 'inventory type invalid'
     
        return status

    def _add(self,  num):
        """同时增加可用库存和物理库存"""
        status = {} 
        # +库存 
        self.available_inventory = F('available_inventory') + num
        self.real_inventory = F('real_inventory') + num
        self.save()
   
    class Meta:
        abstract = True
  
class AdaptorRule(Rule):
    """Rule 适配器"""
    objects = AdaptorRuleManager()
    def __str__(self):
        return self.name  

