# -*- coding:utf-8 -*-

from django.db import models

from basedatas.models import BaseDate
from product.models import AdaptorProduct
from appuser.models import AdaptorUser as User 

class PageAdaptor(AdaptorProduct):
    """
    page 类继承自产品适配器类，将来应用至新项目的时候，
    修改这个类的父类即可

    """
    pass

class Comment(BaseDate):
    COMMENT_REPLAY = 1
    COMMENT_NEW = 0

    user = models.ForeignKey(User)
    content = models.TextField()
    # Comment 类型
    # type = 0,表示这条评论不是回复别人的评论
    # type = 1,表示这条评论是回复别人的评论，
    #          此时parent代表被回复的评论
    type = models.SmallIntegerField(default=COMMENT_NEW)
    # type = 0时，可以忽略parent字段
    parent = models.ForeignKey("AdaptorPageComment", null=True, on_delete=models.CASCADE)# or parent = models.ForeignKey("self")
    
    class Meta:
        abstract = True

class PageComment(Comment):
    """
    目前这个评论是商品的评论，如果要给其他功能加评论功能
    则新添加类，并继承Comment类，然后再写个适配器类，继承
    新添加的类。
    """
    page = models.ForeignKey(PageAdaptor)

    class Meta:
        abstract = True

class AdaptorPageComment(PageComment):
    pass
    class Meta:
        db_table = 'page_comment' 