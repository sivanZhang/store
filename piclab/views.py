#! -*- coding:utf-8 -*-
import pdb
import json
import random
import string
import os
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.http import Http404, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.conf import settings
from django.utils.translation import ugettext  as _
from common.fileupload import handle_uploaded_file
from piclab.models import DetailPic
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
dmb     = DetectMobileBrowser()

class PicLabView(View):
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {}  
        content['mediaroot'] = settings.MEDIA_URL 
        pics = DetailPic.objects.all()
        content['pics'] =pics 
        return render(request, 'piclab/detailpic.html', content)
        
    
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request):
        """ 
        """
        result = {} 
         
        if 'detailpic' in request.POST and 'pic' in request.FILES: # 说明是在上传图库图片 
            files = request.FILES.getlist('pic')
            for file_item in files:
                code    = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(4))
                filename = handle_uploaded_file(file_item, str(request.user.id)+'_'+ code, 'piclab') 
                DetailPic.objects.create(url=filename.replace('\\', '/')) 
            result['status'] = 'OK'
            result['msg']    = _('Uploaded...')
            return self.httpjson(result)
        else:
            result['status'] = 'error'
            result['msg']    = _('Please select image first...')
        
        return self.httpjson(result)
    
    def httpjson(self, result):
        return HttpResponse(json.dumps(result), content_type="application/json")

