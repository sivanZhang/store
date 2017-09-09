#! -*- coding:utf-8 -*-
from django.db import models
from appuser.models import AdaptorUser as User 
from category.models import Category
from django.utils.translation import ugettext_lazy as _
from product.manager import AdaptorProductManager
from store.models import BaseDate

class Product(BaseDate):
    DRAFT = 0
    PUBLISHED = 1
    FALLDOWN = 2
    # 标题
    title = models.CharField(_('title'), max_length = 2048)
    # 库存
    inventory = models.PositiveIntegerField(_('inventory'), default = 0, null=True)
    # 单位
    unit = models.CharField(_('unit'), max_length=128, null=True)
    # 价格
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2, null=True)
    # 创建者
    user = models.ForeignKey(User)
    # 可自定义的规则
    parameters = models.TextField(_('Product Parameters'), null=True)
    # 默认0草稿状态
    # 1 已发布
    # 2 隐藏状态 对于暂时隐藏状态的产品不提供用户搜索，下单操作
    status = models.SmallIntegerField(default=DRAFT)
    # 详情
    detail = models.TextField(_('Detail'), null=True)
    # 所属类别
    category = models.ForeignKey(Category)
    


class AdaptorProduct(Product):
    """Product 适配器"""
    objects = AdaptorProductManager()
    def __str__(self):
        return self.title
