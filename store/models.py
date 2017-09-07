# -*- coding: utf-8 -*-
from django.db import models

class BaseDate(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True