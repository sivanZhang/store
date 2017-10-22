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
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.utils.translation import ugettext as _
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser
dmb     = DetectMobileBrowser()

class SitecontentView(View):
    @method_decorator(login_required)
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {} 
         
        if 'new' in request.GET:
            if isMble:
                return render(request, 'sitecontent/m_new.html', content)
            else:
                return render(request, 'sitecontent/new.html', content)
        if 'test' in request.GET:
            if isMble:
                return render(request, 'm_new.html', content)
            else:
                return render(request, 'test.html', content)
        if 'detail' in request.GET:
            if isMble:
                return render(request, 'sitecontent/m_detail.html', content)
            else:
                return render(request, 'sitecontent/m_detail.html', content)
        if 'unpayed' in request.GET:
            # 给客户展示订单支付页面
            # 需要订单号
            if 'sitecontentno' in request.GET:
                sitecontentno = request.GET['sitecontentno']
                 
            else:
                content['error'] = _("Need sitecontentno, Not Found...")
            if isMble:
                return render(request, 'sitecontent/m_unpayed.html', content)
            else:
                return render(request, 'sitecontent/m_unpayed.html', content)
        else:
            if isMble:
                return render(request, 'sitecontent/m_lists.html', content)
            else:
                return render(request, 'sitecontent/m_lists.html', content)