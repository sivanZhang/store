
# -*- conding:utf-8 -*- 
from django.db import models
from django.utils.translation import ugettext_lazy as _
from appuser.models import AdaptorUser as User
from basedatas.models import BaseDate
from bill.manager import AdaptorBillManager, AdaptorBillItemManager
from product.models import AdaptorProduct, AdaptorRule
from address.models import Address

import threading

class Bill(BaseDate):
    """
    订单主表
    """
    STATUS_FAILED = -3 # 订单创建失败
    STATUS_SUBMITTED = -2 # 订单已提交
    STATUS_UNPAYED = 0 # 未支付
    STATUS_PAYED = 1   # 已支付
    STATUS_FINISHED = 2# 已完成

    STATUS_CHOICES = (
        (STATUS_FAILED, _('failed')),
        (STATUS_SUBMITTED, _('submitted')),
        (STATUS_UNPAYED, _('unpayed')),
        (STATUS_PAYED, _('payed')),
        (STATUS_FINISHED, _('finished')),
    )

    
    # 组成方式：年月日时分秒毫秒用户ID
    no = models.CharField(_('Bill No.'), max_length=1024)
    # 提交订单的人
    owner = models.ForeignKey(User) 
    
    # 收货人地址
    address = models.ForeignKey(Address, null = True) 
    # 收货人电话号码
    phone = models.CharField(_('phone'), max_length=20, null = True) 
    # 收货人姓名
    reciever = models.CharField(_('reciever'), max_length=120, null = True)
  
    #订单金额
    money = models.DecimalField(_('Money'), max_digits = 9, decimal_places = 2, default = 0.0)

    # 订单状态
    # 订单已提交状态在验证了库存之后，直接转入未支付状态
    status = models.SmallIntegerField(choices = STATUS_CHOICES, default = STATUS_SUBMITTED)
    
    # 订单失败的原因， 在订单创建失败之后，这个字段存储创建失败的原因，如库存不足
    errromsg = models.CharField(_('Phone'), max_length = 4096, null =True) 

    # 备注
    remark = models.TextField(_('Remark'), null=True)

    class Meta:
        abstract = True

class AdaptorBill(Bill):
    objects = AdaptorBillManager()

class BillItem(models.Model):
    """
    订单items
    """  
    # 订单主表
    bill = models.ForeignKey(AdaptorBill)

    # 产品名称
    product_title = models.CharField(_('Address'), max_length = 4096, null = True) 
    # 规格名称
    rule_title = models.CharField(_('Rule'), max_length = 4096, null = True) 
    
    # 外键，规格和产品都有可能被删除和编辑，所以这里的外键仅作为减库存时的依据
    # 如果在减库存的时候，
    rule = models.ForeignKey(AdaptorRule, on_delete=models.SET_NULL, null = True)
    product = models.ForeignKey(AdaptorProduct, on_delete=models.SET_NULL, null = True)

    # 下订单时的价格
    price = models.DecimalField(_('Price'), max_digits = 9, decimal_places = 2, default = 0.0)
    # 订单中某商品的数量
    num = models.PositiveIntegerField(_('Number'))
 
    class Meta:
        abstract = True


class AdaptorBillItem(BillItem):
    objects = AdaptorBillItemManager()
