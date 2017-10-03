#! -*- coding:utf-8 -*-
from django.db import models 
import threading 
import pdb
import json
from datetime import datetime

lock = threading.Lock()


class BillManager(models.Manager): 
    def createbill(self, items, post):
        """
        # 创建订单：主表及附表
        """
        bill_kwargs = {}
        if 'phone' in post:
            bill_kwargs['phone'] = post['phone'].strip() 
        if 'reciever' in post:
            bill_kwargs['reciever'] = post['reciever'].strip() 
        if 'address' in post:
            bill_kwargs['address'] = post['address'].strip()
        if 'area' in post:
            bill_kwargs['area__id'] = post['area'].strip()  

class AdaptorBillManager(BillManager):
    pass

class BillItemManager(models.Manager):
    pass

class AdaptorBillItemManager(BillItemManager):
    pass
