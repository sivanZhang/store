#! -*- coding:utf-8 -*-
from django.db import models 
import threading 
import pdb
import json





class ProductManager(models.Manager):
    
    def fallback(self, ):
        """下架商品"""
        self.model.status = self.model.FALLDOWN
        self.model.save()

    def publish(self):
        """发布商品， 商品上架"""
        self.model.status = self.model.PUBLISHED
        self.model.save()
    
    def get_published(self):
        """获取已经发布的商品，商品状态为：published"""
        return self.filter(status=self.model.PUBLISHED)
        
class AdaptorProductManager(ProductManager):
    pass



class RuleManager(models.Manager):
    """
    规格的manager，增加库存，减少库存都需要在这里执行
    """
    
    def mul_create(self, rules_str, product):
        """
        批量创建规格
        rules_str参数的样式：'[{"key":"23","value":"JK37"},{"key":"2332","value":"WL7"}]'
        """ 
        rules = json.loads(rules_str)
        for rule in rules: 
            self.create(product = product, name=rule['name'], price = float(rule['price']), inventory=rule['inv'], unit=rule['unit'] )
      
    
    def check_available_inventory(self, rules):
        """
        检测rules中可用库存是否满足出库条件。
        返回可用库存不足的的rules，
        返回状态为：status=1代表可用库存足够，status=0代表可用库存不足，检测返回的rules list来查看哪些库存不足
        对于没有找到的rule，在notfound字段中返回

        如果result['status']！= 1 时，需要判断result['notfound']和result['notenough']
        两个的list长度，可能可用库存不足，也可能没有找到相应的rule，两个问题也可能同时存在
        """
        result = {}
        result['status'] = 1 #默认为可用库存满足
        notfound = []
        notenough = []
        for rule in rules:
            try:
                rule_instance = self.model.objects.get(pk = rule['id'])
                if rule_instance.available_inventory <  rule['num']:
                    notenough.append(rule['id'])
                    result['status'] = -0
            except self.model.DoesNotExist:
                notfound.append(rule['id'])
                result['status'] = -1

        result['notfound'] = notfound
        result['notenough'] = notenough
        return result

class AdaptorRuleManager(RuleManager):
    pass