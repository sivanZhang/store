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

 

from .form import UploadPortrainForm, GroupForm, UserForm

 

from django.contrib import auth

#from socialoauth import SocialSites,SocialAPIError  

from basedatas.bd_comm import Common
from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser

dmb     = DetectMobileBrowser()
comm    = Common()


#list all user portraits in a page
def list_users(request):
    isMble  = dmb.process_request(request)
    
    context = {  }
     
    #get user list
    user_list = User.objects.all().order_by('-date')
           
    context = { 'user_list':user_list }
    if isMble:
        return render(request, 'map2family/m_users.html', context)
    else:
        return render(request, 'map2family/users.html', context)


#list all user for administrator to manage
def admin_list_users(request):
    isMble  = dmb.process_request(request)
    
    context = {  }
     
    #get user list
    user_list = User.objects.all().order_by('-date')
           
    context = { 'user_list':user_list }
    if isMble:
        return render(request, 'admin_user/m_userslist.html', context)
    else:
        return render(request, 'admin_user/userslist.html', context)
    
@csrf_exempt
def portrait(request):
    #response for the social site user login
    '''
    socialsites = SocialSites(settings.SOCIALOAUTH_SITES)
 
    if request.GET.get('state',None)=='socialoauth':
 
        auth.logout(request) #logout first
         
        access_code = request.GET.get('code')
         
        qq_object = socialsites.get_site_object_by_name('qq')
        try:
            qq_object.get_access_token(access_code)
            fake_email = qq_object.uid+"@qq.com"
            try:
                #user exist
                User.objects.get(email=fake_email)
            except User.DoesNotExist:
                #user doesn't exist, need add it first
                social_user = User(name=qq_object.name,email=fake_email,head_portrait=qq_object.avatar,social_user_status=1,social_site_name=1,social_user_id=qq_object.uid)
                social_user.set_password(qq_object.uid)
                social_user.date = timezone.now()
                social_user.save()
            
            user = auth.authenticate(email=fake_email, password=qq_object.uid)    
            request.user = user
            auth.login(request, user)
            return HttpResponseRedirect("/")
        except SocialAPIError as e:
            print (e )
    '''
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
    result = {} 
    if request.method == 'POST':
        user = request.user
        
        #remove the old portraint
        
        if 'media' in usesr.head_portrait.name[1:]:
            oldportraint = os.path.join(settings.MEDIA_ROOT, user.head_portrait.name[7:])
        else:
            oldportraint = os.path.join(settings.MEDIA_ROOT, user.head_portrait.name[1:])
        
     
        if os.path.isfile(oldportraint):
            os.remove(oldportraint)
            #rename the fake portrait 
            if 'media' in usesr.fake_head_portrait.name[1:]:
                os.rename(os.path.join(settings.MEDIA_ROOT,user.fake_head_portrait.name[7:]), oldportraint)
            else:
                os.rename(os.path.join(settings.MEDIA_ROOT,user.fake_head_portrait.name[1:]), oldportraint) 
        user.head_portrait = user.fake_head_portrait
        user.is_head_portrait = True
        user.save()
    
        result['status'] = 'OK'
        result['msg']    = '头像上传成功...' 
        return HttpResponse(json.dumps(result), content_type='application/json')
    else:
        form = UploadPortrainForm()
        form.fields['portrain'].label = '点击上传头像'
        admin_granted = has_admin_perm(request.user)
        
        context = {
            'form':form.as_ul(),
            'admin_granted':admin_granted,
            }
        if isMobile:
            return render(request, 'admin_user/m_change_portrait.html', context)
        else:
            return render(request, 'admin_user/change_portrait.html', context)
 
        
@csrf_exempt
def upload_fake_portrait(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    result = {}      
    if request.method == 'POST':
        form = UploadPortrainForm(request.POST, request.FILES)
        if form.is_valid(): 
            usesr = request.user

            #remove the old portraint 
            if 'media' in usesr.head_portrait.name[1:]:
                oldportraint = os.path.join(settings.MEDIA_ROOT, usesr.head_portrait.name[7:])
            else:
                oldportraint = os.path.join(settings.MEDIA_ROOT, usesr.head_portrait.name[1:])
            
            
            if os.path.isfile(oldportraint):
                os.remove(oldportraint)
                    
            
            code    = ''.join(random.choice(string.lowercase + string.digits) for i in range(4))
            filename = handle_uploaded_file(request.FILES['portrain'], str(usesr.id)+'_'+ code)
                
            #usesr.is_head_portrait = False  
            usesr.head_portrait = filename.replace('\\', '/')
            usesr.is_head_portrait  = True
            usesr.save()
            result['status'] = 'OK'
            result['msg']    = '头像上传成功...'
            result['file']    = filename  
        else:
            result['status'] = 'ERROR'
            result['msg']    = '请先选择图片..'
             
    else:
        result['status'] = 'ERROR'
        result['msg']    = '请先选择图片..'
  
    return HttpResponse(json.dumps(result), content_type='application/json')

def handle_uploaded_file(f, userid):
    #with open(os.path.join(settings.MEDIA_ROOT, 'portrait'), 'wb+') as destination:
        
    filename = str(userid) + '.png' 
    
    with open(os.path.join(settings.MEDIA_ROOT, 'portrait', filename), 'wb+') as destination:
        for chunk in f.chunks() :
            destination.write(chunk)
    return os.path.join(settings.MEDIA_URL, 'portrait', filename)

def grouplist(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
     
    #get group list
    group_list = Group.objects.all()
        
    context = { 'group_list':group_list }
    if isMobile:
        return render(request, 'admin_user/m_grouplist.html', context)
    else:
        return render(request, 'admin_user/grouplist.html', context)

             
def newgroup(request):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
    if  not has_admin_perm(request.user):
        context = {
                     'not_granted' : True, 
                  }
    else: 
        if request.method == 'POST':
            form = GroupForm(request.POST)
            
            if form.is_valid(): 
                new_group = form.save() 
                form = GroupForm()
                context = {
                     'form'       :  form,
                     'saved'      :  True,
                     'validate'   :  True,
                  }
            else:
                #invalide form
                form = GroupForm()
                context = {
                     'form'       : form,
                     'validate'   : False,
                  }
        else: 
            form = GroupForm()
            context = {
                     'form'       : form,
                     'validate'   :  True,
                  }
    if isMobile:    
        return render(request, 'admin_user/m_group.html', context)
    else:
        return render(request, 'admin_user/m_group.html', context)

def modify_group(request, groupid):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
    

    if  not has_admin_perm(request.user):
        context = {
                     'not_granted' : True, 
                  }
    else:
        try:
            group = Group.objects.get(pk=groupid)
            if request.method == 'POST':
                form = GroupForm(request.POST, instance=group) 
                if form.is_valid(): 
                    form.save() 
                    context = { 
                         'form'       :  form,
                         'saved'      :  True,
                         'validate'   :  True,
                      }
                else:
                    #invalide form
                    form = GroupForm()
                    context = {
                         'form'       : form,
                         'validate'   : False,
                      }
            else: 
                form = GroupForm(instance = group)
                context = {
                         'form'       : form,
                         'validate'   :  True,
                      }
        except Group.DoesNotExist:
            context = {
                         'usernotexist'   :  True,
                      }
        
    
    if isMobile:    
        return render(request, 'admin_user/m_group.html', context)
    else:
        return render(request, 'admin_user/m_group.html', context)

def has_admin_perm(user):
    '''
       if a user has permission to manage user, group and permission
       if has, return True, else return False
    '''
    if user.is_superuser:
        return True
    else:
        return user.has_perm('appuser.admin_management') 


def modify_user(request, userid):
    isMobile = dmb.process_request(request)
    if  request.user.is_anonymous():
        return comm.redirect_login_path(isMobile, request)
    
  
    if  not has_admin_perm(request.user):
        context = {
                     'not_granted' : True, 
                  }
    else:
        try:
            user = User.objects.get(pk=userid)
            if request.method == 'POST':
                form = UserForm(request.POST, instance=user) 
                if form.is_valid(): 
                    form.save() 
                    context = { 
                         'form'       :  form,
                         'saved'      :  True,
                         'validate'   :  True,
                      }
                else:
                    #invalide form
                    form = UserForm()
                    context = {
                         'form'       : form,
                         'validate'   : False,
                      }
            else: 
                form = UserForm(instance = user)
                context = {
                         'form'       : form,
                         'validate'   :  True,
                      }
        except User.DoesNotExist:
            context = {
                         'usernotexist'   :  True,
                      }
        
    
    if isMobile:    
        return render(request, 'admin_user/m_change_user.html', context)
    else:
        return render(request, 'admin_user/change_user.html', context)



'''
new frame start
'''
def usernames(request, username):
    if request.method == 'GET':
        msg= User.objects.uniqueUsername(username) 
        status={'result':'ok',
        'msg':msg}
    return HttpResponse(json.dumps(status), content_type="application/json")

def email(request, email):
    if request.method == 'GET':
        msg= User.objects.uniqueEmail(email) 
        status={'result':'ok',
        'msg':msg}
    return HttpResponse(json.dumps(status), content_type="application/json")

def emailscode(request, email):
    if request.method == 'GET':
        msg= VerifyCode.objects.send_code(email)  
    return HttpResponse(json.dumps(msg), content_type="application/json")

def verify(request, email, code):
    if request.method == 'GET':
        result = VerifyCode.objects.veirfy_code(code, email)  
    return HttpResponse(json.dumps(result), content_type="application/json")