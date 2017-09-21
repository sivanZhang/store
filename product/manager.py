#! -*- coding:utf-8 -*-
from django.db import models 
import threading 
import pdb
import json


lock = threading.Lock()


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
    
    def reduce(self,  num):
        """减少库存"""
        Timeout = 5 # 最多等待5秒
        status = {}
        if lock.acquire(self.Timeout):
            # 减库存
            if self.model.inventory - num < 0:
                status['result'] = 'error'
                status['msg'] = '错误：库存不足'
            else:
                self.model.inventory -= num
                self.model.save()
                status['result'] = 'ok'
                status['msg'] = 'Done'

            lock.release()

    def add(self,  num):
        """增加库存"""
        status = {}
        if lock.acquire(self.Timeout):
            # +库存 
            self.model.inventory += num
            self.model.save()
            status['result'] = 'ok'
            status['msg'] = 'Done' 
            lock.release()

    def mul_create(self, rules_str, product):
        """
        批量创建规格
        rules_str参数的样式：'[{"key":"23","value":"JK37"},{"key":"2332","value":"WL7"}]'
        """ 
        rules = json.loads(rules_str)
        for rule in rules: 
            self.create(product = product, name=rule['name'], price = float(rule['price']), inventory=rule['inv'], unit=rule['unit'] )
      
        
class AdaptorRuleManager(RuleManager):
    pass