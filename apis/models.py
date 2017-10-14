from django.db import models
from django.utils.translation import ugettext_lazy as _

class Apis(models.Model):
    """
    api 列表
    """   
    url = models.CharField(_('Address'), max_length = 2048, null = True) 
    #  
    remark = models.CharField(_('Rule'), max_length = 4096, null = True) 
  
class AdaptorApis(Apis):
    pass