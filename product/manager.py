#! -*- coding:utf-8 -*-
from django.db import models 
import threading 
import pdb
lock = threading.Lock()


class ProductManager(models.Manager):
    

    def reduce(self, adaptorproduct, num):
        """减少库存"""
        Timeout = 5 # 最多等待5秒
        status = {}
        if lock.acquire(self.Timeout):
            # 减库存
            if adaptorproduct.inventory - num < 0:
                status['result'] = 'error'
                status['msg'] = '错误：库存不足'
            else:
                adaptorproduct.inventory -= num
                adaptorproduct.save()
                status['result'] = 'ok'
                status['msg'] = 'Done'

            lock.release()

    def add(self, adaptorproduct, num):
        """增加库存"""
        status = {}
        if lock.acquire(self.Timeout):
            # +库存 
            adaptorproduct.inventory += num
            adaptorproduct.save()
            status['result'] = 'ok'
            status['msg'] = 'Done' 
            lock.release()

    def fallback(self, adaptorproduct):
        """下架商品"""
        adaptorproduct.status = self.model.FALLDOWN
        adaptorproduct.save()

    def publish(self, adaptorproduct):
        """发布商品， 商品上架"""
        adaptorproduct.status = self.model.PUBLISHED
        adaptorproduct.save()
    
    def get_published(self):
        """获取已经发布的商品，商品状态为：published"""
        return self.filter(status=self.model.PUBLISHED)
        
 
class AdaptorProductManager(ProductManager):
    pass