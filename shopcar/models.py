# -*- coding:utf8 -*-
from django.db import models 
from product.models import AdaptorRule
from appuser.models import AdaptorUser

class CartItem(models.Model):
    """ 
    购物车类：
    model class containing information each Product instance in the customer's shopping cart
    用户浏览的时候购物车中的商品的增删都是在session中操作；
    在用户关闭页面时更新数据库中的购物车，用户提交订单之后，从购物车中删除已购的商品
    """ 
    user = models.ForeignKey(AdaptorUser)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    # 购物车中存储的应该是某一产品的某一规格，比如，电脑下有256G电脑，128G电脑，购物车存储的应该是其中的一种
    # 而不是电脑本身
    rule = models.ForeignKey(AdaptorRule, unique=False, on_delete=models.CASCADE) 
            
    class Meta:
        db_table = 'cart'
        ordering = ['date_added']
    
    @property
    def total(self):
        return self.quantity * self.rule.price
    
    @property
    def name(self):
        return self.rule.product.title
    
    @property
    def price(self):
        return self.rule.price
    
    def augment_quantity(self, quantity):
        """ called when a POST request comes in for a Product instance already in the shopping cart """
        self.quantity = self.quantity + int(quantity)
        self.save()