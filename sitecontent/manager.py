#! -*- coding:utf-8 -*-
from django.db import models 
import pdb
import json
import copy


class SiteContentManager(models.Manager): 
    def get_available_content(self):
        return self.filter(status=self.model.STATUS_SHOW)
        
class AdaptorSiteContentManager(SiteContentManager):
    pass
 

 