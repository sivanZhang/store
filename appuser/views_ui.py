# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect 
import pdb
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import  Group
import os
from appuser.models import AdaptorUser as User
from appuser.models import VerifyCode
import json
import random
import string
from django.utils import timezone
from django.urls import reverse
from .form import UploadPortrainForm, GroupForm, UserForm
from django.contrib import auth
#from socialoauth import SocialSites,SocialAPIError  

from basedatas.bd_comm import Common
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser

dmb     = DetectMobileBrowser()
comm    = Common()

@csrf_exempt
def login(request):
    isMble  = dmb.process_request(request)
    
    if 'email' in request.POST and 'password' in request.POST:
            auth.logout(request)
            email       = request.POST['email']
            password      = request.POST['password']
            user = auth.authenticate(email=email, password=password)
            if 'next' in request.GET: 
                next_url = request.GET.get('next')
            else:
                next_url = request.POST.get('next')
            context ={} 
            if user:
                # User is valid.  Set request.user and persist user in the session
                # by logging the user in.
                request.user = user
                auth.login(request, user)
                # redirect to the value of next if it is entered, otherwise
                # to settings.APP_WEB_PC_LOGIN_URL
                next_url
                if next_url:
                    #after login, return to the previous page, but if the previous page is logout, 
                    #then return to the host page
                    if 'logout' not in str(next_url): 
                         return redirect(next_url)
            
                return redirect(reverse('home'))
            else:
                try: 
                    user_instance = User.objects.get(email = email)
                    msg = '登录失败，密码错误...' 
                except User.DoesNotExist:
                    msg = '登录失败，用户{0}未注册...'.format(email)
          
                context = {'next':next_url,
                           'status':'error',
                           'msg':msg,
                           'email':email}
            if isMble: 
                return render(request, 'user/m_login.html', context)
            else:
                return render(request, 'user/login.html', context)
            
    else:
        next_url = request.GET.get('next')
        context = {'next':next_url}

        if isMble: 
            return render(request, 'user/m_login.html', context)
        else:  
            return render(request, 'user/login.html', context)
def logout(request):
    auth.logout(request)
    isMble  = dmb.process_request(request)
    return redirect(reverse('home'))
   
@csrf_exempt
def register(request):
    isMble  = dmb.process_request(request)
    content = {}

    if request.method == "POST":
        return HttpResponseRedirect(reverse('users:login'))
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        emailcode = request.POST['emailcode'].strip()
        if VerifyCode.objects.veirfy_code(emailcode, email):
            user = User.objects.create_user(email, username,  password)
            content={
                'result':'ok',
                'msg':'注册成功！'
            }
        else:
            content={
                'result':'error',
                'username':username,
                'email':email, 
                'msg':'验证码错误...'
            }
    
    if isMble: 
        return render(request, 'user/m_regsiter.html', content)
    else:  
        return render(request, 'user/regsiter.html', content)
 
