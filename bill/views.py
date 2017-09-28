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


from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser


dmb     = DetectMobileBrowser()

   
class BillView(View):
    
    def get(self, request):
        isMble  = dmb.process_request(request)
        content = {} 
        
        if 'new' in request.GET:
            if isMble:
                return render(request, 'm_new.html', content)
            else:
                return render(request, 'new.html', content)
        if 'test' in request.GET:
            if isMble:
                return render(request, 'm_new.html', content)
            else:
                return render(request, 'test.html', content)
        if 'pic' in request.GET:
            if isMble:
                return render(request, 'm_pic.html', content)
            else:
                return render(request, 'pic.html', content)
        else:
            if isMble:
                return render(request, 'bill/m_lists.html', content)
            else:
                return render(request, 'bill/m_lists.html', content)