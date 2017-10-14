#! -*- coding:utf-8 -*-
from django.db import models 
import threading 
import pdb
import json
import copy

lock = threading.Lock()
Timeout = 3

class ProductManager(models.Manager): 
    def get_published(self):
        """获取已经发布的商品，商品状态为：published"""
        return self.filter(status=self.model.PUBLISHED)
        
class AdaptorProductManager(ProductManager):
    pass
 

class RuleManager(models.Manager):
    """
    规格的manager，增加库存，减少库存都需要在这里执行
    """
    OP_ADD = 1    # 加库存操作，同时增加可用库存和物理库存
    OP_REDUCE = 0 # 减库存操作
    Timeout = 3
    def mul_create(self, rules_str, product):
        """
        批量创建规格
        rules_str参数的样式：'[{"key":"23","value":"JK37"},{"key":"2332","value":"WL7"}]'
        """ 
        rules = json.loads(rules_str)
        for rule in rules:  
            self.create(product = product, name=rule['name'], price = float(rule['price']), 
                             real_inventory=rule['inv'],available_inventory=rule['inv'], unit=rule['unit'] )

    def inventory_op(self, rules = None, reduce_type=None, op_type= OP_REDUCE, billstatus=None):
        """
        库存操作函数：对于商品的库存操作都应该经过这个函数去处理
        op_type = OP_REDUCE, 默认， 代表减库存操作， 此时rules和reduce_type字段不能为空。reduce_type代表减库存的类型
                             备选值有：
                                    OP_REDUCE_TYPE_AVAIL = 0 # 减可用库存
                                    OP_REDUCE_TYPE_REAL = 1  # 减物理库存
                                    OP_REDUCE_TYPE_ALL = 2   # 同时减少可用库存和物理库存 
                            rules, 为list，存储的字典为rules=[{'ruleid':23, 'num': 23},]
        
        op_type = OP_ADD, 代表同时增加可用库存和物理库存操作， 此时rules字段不能为空，忽略reduce_type字段。
                            rules, 为list，存储的字典为rules=[{'ruleid':23, 'num': 23},]
        """
        result = {}
        # 判断参数的有效性----开始
        if op_type == self.OP_REDUCE: # 减库存操作
            if reduce_type is None:
                result['status'] = 'error'
                result['msg'] = 'Need reduce_type'
                return result
            if rules is None:
                result['status'] = 'error'
                result['msg'] = 'Need rules'
                return result
            else:
                if not isinstance(rules, list):
                    result['status'] = 'error'
                    result['msg'] = 'rules should be list'
                    return result
                elif len(rules) == 0:
                    result['status'] = 'error'
                    result['msg'] = 'rules is empty'
                    return result
                elif isinstance(rules[0], dict):
                    keys = rules[0].keys()
                    if 'ruleid' not in keys or 'num' not in keys:
                        result['status'] = 'error'
                        result['msg'] = 'Need ruleid and num in rules '
                        return result
                else:
                    result['status'] = 'error'
                    result['msg'] = 'rules items should be dict'
                    return result
        elif op_type == self.OP_ADD: # 加库存操作
            if rules is None:
                result['status'] = 'error'
                result['msg'] = 'Need rules'
                return result
            else:
                if not isinstance(rules, list):
                    result['status'] = 'error'
                    result['msg'] = 'rules should be list'
                    return result
                elif len(rules) == 0:
                    result['status'] = 'error'
                    result['msg'] = 'rules is empty'
                    return result
                elif isinstance(rules[0], dict):
                    keys = rules[0].keys()
                    if 'ruleid' not in keys or 'num' not in keys:
                        result['status'] = 'error'
                        result['msg'] = 'Need ruleid and num in rules '
                        return result
                else:
                    result['status'] = 'error'
                    result['msg'] = 'rules items should be dict'
                    return result        
        else:
            result['status'] = 'error'
            result['msg'] = 'op_type invalid'
            return result
        # 判断参数的有效性-----结束

        # 锁库存 
        lock.acquire(self.Timeout)
        # 启用备忘录模式
        rules_backup = []
        if op_type == self.OP_ADD: # 加库存
            # 未测试：2017年10月11日20:27:16
            for rule_i in rules:
                try:
                    rule = self.model.objects.get(pk = rule_i['ruleid'])
                    rules_backup.append(copy.copy(rule)) # 加入备忘录
                    rule._add(int(rule_i['num'])) 
                except self.model.DoesNotExist:
                    # 从备忘录中恢复 
                    for rule in rules_backup:
                        rule.save()
                     
                    result['status'] = 'error'
                    result['msg'] = '{0} not found'.format(rule_i['ruleid'])
                    lock.release()
                    return result

            result['status'] = 'ok'
            result['msg'] = 'Done'
            lock.release()
            return result
        elif op_type == self.OP_REDUCE: # 减库存
            for rule_i in rules:
                try: 
                    rule = self.model.objects.get(pk = rule_i['ruleid']) 
                    rules_backup.append(copy.copy(rule)) # 加入备忘录 
                    status = rule._reduce( num = int(rule_i['num']), inventory_type=reduce_type) 
                    if status['result'] == 'error':
                        # 从备忘录中恢复  
                        for rule in rules_backup:
                            rule.save()
                        
                        result['status'] = 'error'
                        result['msg'] = status['msg']
                        lock.release()
                        return result
                     
                except self.model.DoesNotExist:
                    # 从备忘录中恢复 
                    for rule in rules_backup:
                        rule.save()
                     
                    result['status'] = 'error'
                    result['msg'] = '{0} not found'.format(rule_i['ruleid'])
                    lock.release()
                    return result
            result['status'] = 'ok'
            result['msg'] = 'Done'
            
            # 更新订单信息
            lock.release()
            return result
 

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