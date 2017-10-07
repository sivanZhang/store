#! -*- coding:utf-8 -*-
from django.db import models  
import pdb
import json
from datetime import datetime


class BillManager(models.Manager): 
    def createbill(self, post, user):
        """
        # 创建订单：主表
        """
        bill_kwargs = {}
        
        no = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S') + str(user.id)

        bill_kwargs['ownser'] = user
        bill_kwargs['no'] = no
        if 'address_id' in post:
            bill_kwargs['address_id'] = post['address_id'].strip()
        if 'phone' in post:
            bill_kwargs['phone'] = post['phone'].strip() 
        if 'reciever' in post:
            bill_kwargs['reciever'] = post['reciever'].strip() 
       
        pdb.set_trace()
        bill = self.create( **bill_kwargs )
        return bill

class AdaptorBillManager(BillManager):
    pass

class BillItemManager(models.Manager):
    def createitem(self, bill, items):
        """
        # 创建订单：附表
        item: ruleid, productis, num
        """ 
        pdb.set_trace()
        for item in items:
            self.create(bill = bill, rule_id=item['ruleid'], 
                        product_id=item['productid'], num=item['num'])

          
class AdaptorBillItemManager(BillItemManager):
    pass
