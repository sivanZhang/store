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
    DELETED = 3 # 

    # 是否允许永久删除产品，即从数据库中删除产品
    # 可以根据不同客户的不同需求具体确定
    # 如果 ALLOW_DELETE = True的时候代表可以删除
    # 如果 ALLOW_DELETE = False的时候代表不可以永久删除，status字段应该被设置为DELETED
    # 这主要是针对有订单产生的产品，没有订单产生的产品可以永久删除，而不在意ALLOW_DELETE的设置
    ALLOW_DELETE = True

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
    # 3 删除状态 代表用户已经执行了删除操作，但是系统没有从数据库中永久删除
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
    

    class Meta:
        abstract = True


class StoreProduct(Product):
    """商城类的Product适配器""" 
    def fallback(self ):
        """下架商品"""
        self.status = self.FALLDOWN
        self.save()
    
    @property
    def hasbill(self): 
        """查看产品是否有订单产生，如果有的话，return True 否则 return False """
        bills = self.adaptorbill_set.all()
        if len(bills) > 0:
            return True
        else:
            return False

    def set_undeleted(self):
        """
        修改product时，将product的规格的deleted字段预先都设置为1
        """
        self.adaptorrule_set.all().update(deleted=1)
    

    def delete_droped_rules(self):
        """
        修改product时，有些规格可能被用户删除了
        被删除的规格的deleted字段标记为1

        注意：有未支付订单的规格不能删除
        返回没有删除的记录列表
        """
        rules = self.adaptorrule_set.filter(deleted=1)
        undeleted_list = []
        for rule in rules:
            if rule.has_unpayedbill() > 0:
                rule_error = {}
                rule_error['ruleid'] = rule.id  
                rule_error['name'] = rule.name                
                undeleted_list.append(rule_error)
                rule.deleted = 0
                rule.save()
            else:
                rule.delete()
        
        return undeleted_list

    def publish(self):
        """发布商品， 商品上架"""
        self.status = self.PUBLISHED
        self.save()

    objects = AdaptorProductManager() 
    taobaourl = models.CharField(_('taobao url'), max_length = 2048, null=True)
    def __str__(self):
        return self.title

    class Meta:
        abstract = True  

class AdaptorProduct(StoreProduct):
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

    class Meta:
        db_table = 'pic'
     
 
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
    
    # 标记这个规格在用户修改的过程中是否被删除了
    # 算法：
    #     1 修改商品前将商品的所有规格的deleted字段设置为1
    #     2 修改的过程中设置为0
    #     3 删除那些deleted字段仍为1的规格记录
    deleted = models.PositiveIntegerField(default = 0)
     
    def _reduce(self, num, inventory_type = OP_REDUCE_TYPE_AVAIL):
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

    def _add(self, num):
        """同时增加可用库存和物理库存""" 
        # +库存 
        self.available_inventory = F('available_inventory') + num
        self.real_inventory = F('real_inventory') + num
        self.save()

    def billlist(self):
        """
        # 判断本条规格是否有订单产生，如果有，返回订单列表，否则返回空的列表
        """ 
        from bill.models import AdaptorBill
        bills = self.adaptorbillitem_set.filter(bill__status = AdaptorBill.STATUS_PAYED)
        return bills

    def has_unpayedbill(self):
        """
        查看是否有未支付的订单
        如果有，返回未支付订单锁定的数量，否则，返回0
        """
        # 如果可用库存和实物库存不一致，那么就有未支付的订单
        return self.real_inventory - self.available_inventory 

    class Meta:
        abstract = True

class AdaptorRule(Rule):
    """Rule 适配器"""
    objects = AdaptorRuleManager()
    def __str__(self):
        return self.name  

