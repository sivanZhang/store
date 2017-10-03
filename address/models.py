# -*- coding: utf-8 -*-
from django.db import models
from area.models import Area
from appuser.models import AdaptorUser as User
from django.utils.translation import ugettext_lazy as _


class Address(models.Model):
    user = models.ForeignKey(User)
    area = models.ForeignKey(Area)
    # 收货人地址
    detail = models.CharField(_('Detail'), max_length = 4096, null = True)
    #收货人
    receiver = models.CharField(_('Receiver'), max_length = 256, null = True) 
    #收货人电话
    phone = models.CharField(_('Phone'), max_length = 128, null = True) 

 