# -*- coding: utf-8 -*-

from django.shortcuts import render
import getpass
#from django.contrib.auth.models import User,Group
from appuser.models import   VerifyCode
from appuser.models import AdaptorUser as User
import pdb
from django.utils import timezone
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from ticket.models import Ticket
from task.models import Todo_list
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
import random
import string
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import threading

import smtplib
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart  
from email.MIMEText import MIMEText
from basedatas.e_mail import Email, EmailEx

from django.conf import settings
from django.db.models import Q
import re

from mobile.detectmobilebrowsermiddleware import DetectMobileBrowser


from basedatas.bd_comm import Common
from common.stat import StatComm

from .models import Day_words, Reltn_dayword_comm
from good.models import G_daywords
from comment.models import Comment
from msg.models import Msg
from msg.msg_comm import MsgComm
from blocks.models import Block

#validate email format
EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
            
dmb     = DetectMobileBrowser()
comm    = Common()

def new_day_words(request):
        StatComm.count_page_traffic(request)
        is_Mobile = dmb.process_request(request)
        if  request.user.is_anonymous():
                return comm.redirect_login_path(is_Mobile, request)
         
        if is_Mobile:
                return render(request, 'daywords/m_new.html', {} )
        else:                
                return render(request, 'daywords/m_new.html', {} )

@csrf_exempt    
def save_day_words(request):
    if  request.user.is_anonymous():
        return redirect(settings.APP_WEB_LOGIN_URL)
     
    if request.method == 'POST' and 'words' in request.POST:
        words     = request.POST["words"]
         
        day_words = Day_words.objects.create(content=words,date=timezone.now(),user=request.user) 
        day_words.save()
        return HttpResponse("发布成功,去首页看看吧...")


def index_day_words(request):

    StatComm.count_page_traffic(request)
    isMobile = dmb.process_request(request)
    
    
    day_words_list = Day_words.objects.all().order_by('-pk')
    words_list = []
    each_word = {}
    
    
    if request.user.is_anonymous():
        user = ''
    else:
        user = request.user
        
        
    #I need log module to get the efficiency of this for section
    for day_words in day_words_list:
        g_dayword_list = G_daywords.objects.filter(app = day_words)
        #count = g_dayword_list.count()
        
        #get if current user praised this day_word
        Praised = False
        for g_dayword in g_dayword_list:
            if user == g_dayword.owner:
                Praised = True
                break
                
                
        each_word={
            'word_id':day_words.id,
            'username':day_words.user.get_full_name(),
            'words':day_words.content,
            'date':day_words.date,
            'count':day_words.good_count,
            'isPraised':Praised,
            'comment_count':day_words.comment_count
        }
         
        words_list.append(each_word)
        
        
    context = {'words_list' : words_list}
    isMobile = dmb.process_request(request)
     
    if isMobile:
        return render(request, 'daywords/m_index.html', context)
    else:
        return render(request, 'daywords/m_index.html', context)
     
        


def index(request):

    StatComm.count_page_traffic(request)
    isMble  = dmb.process_request(request)

    context = {  }
    #if not request.user.is_anonymous():
    user = request.user
        
    next_url = request.GET.get('next');
     
    if next_url: 
            return redirect(next_url)
    else:
            #get user list
            user_list = User.objects.filter().order_by('-date')
            day_word_list = Day_words.objects.filter().order_by('-id') 
            if day_word_list:
                day_word = day_word_list[0]
                context = { 'user_list':user_list,
                        'content':day_word.content,
                        'creator':day_word.user.get_full_name()}
            else:
                context = { 'user_list':user_list}
            
            blocks = Block.objects.all()
            context['blocks'] = blocks
            if isMble:
                return render(request, 'map2family/m_hostpage.html', context)
            else:
                return render(request, 'map2family/homepage.html', context)
    
def guide_L2(request):
        return render(request, 'guide/guide.html', {})
def guide_L1(request):
        return render(request, 'guide/guide_l1.html', {})
def contact_us(request):
    StatComm.count_page_traffic(request)
    isMble  = dmb.process_request(request)
    if isMble:
                return render(request, 'help/m_contact-us.html', {})
    else:
                return render(request, 'help/m_contact-us.html', {})
    
    
def user_register(request):

    StatComm.count_page_traffic(request)
    dmb     = DetectMobileBrowser()
    isMble  = dmb.process_request(request)
    
    content = {'page':'user_register',
	'page_title':'注册为新会员'} 
    print isMble
    if isMble:
        return render(request, 'basedatas/m_user_register.html', content)
    else:
        return render(request, 'basedatas/user_register.html', content)
        
def find_password(request):
    StatComm.count_page_traffic(request)
    isMble  = dmb.process_request(request) 
    content = {'page':'find_password',
	'page_title':'找回密码'}
    if isMble:
        return render(request, 'basedatas/m_user_register.html', content)
    else:
        return render(request, 'basedatas/user_register.html', content)
		
    #return render(request, 'basedatas/find_pwd.html', content)

def reset_password(request):
    result = {}
    if request.method == 'GET':
            if 'email' in request.GET and 'verifycode' in request.GET and 'pwd' in request.GET:
                email           = request.GET["email"]
                verifycode      = request.GET["verifycode"]
                pwd             = request.GET["pwd"]
                try:
                    verify_code = VerifyCode.objects.get(email__exact = email, code=verifycode, type ='1')
                    try:
                        user    = User.objects.get(email = email)
                        '''
                        password    = ''.join(random.choice(string.ascii_uppercase + string.lowercase 
                               +  string.digits) for i in range(6))
                        '''
                        user.set_password(pwd)
                        user.save()
                        verify_code.delete()
                        
                        #send email
                        email_insance = EmailEx()
                        Subject = 'map2family密码已重置' 
                        content = '您好, 您在map2family中的密码已重置成功. <br />若不是您本人操作请立即登录重新修改...'
                        try:
                            email_insance.send_text_email(Subject, content, email)
                            result['status'] = 'OK'
                            result['msg'] = '密码重置成功...'
                            return HttpResponse(json.dumps(result), content_type='application/json')
                        except   Exception, e: 
                            result['status'] = 'ERROR'
                            result['err_msg'] = '发送邮件的过程中发生错误： '+ e
                            return HttpResponse(json.dumps(result), content_type='application/json')
                    except User.DoesNotExist:
                        result['status'] = 'ERROR'
                        result['err_msg'] = '您输入的邮箱用户不存在， 请重试... !'
                        return HttpResponse(json.dumps(result), content_type='application/json')
                    
                except VerifyCode.DoesNotExist:
                    result['status'] = 'ERROR'
                    result['err_msg'] = '验证码与邮箱不匹配, 请检查邮件和验证码... !'
                    return HttpResponse(json.dumps(result), content_type='application/json')
            else:
                result['status']  = 'ERROR'
                result['err_msg'] = '非法参数， 你在干什么 !'
                return HttpResponse(json.dumps(result), content_type='application/json')   
    else:
        result['status'] = 'ERROR'
        result['err_msg'] = '非法参数， 你在干什么 !'
        return HttpResponse(json.dumps(result), content_type='application/json') 
def send_email(subject, content, receiver):
    email_insance = EmailEx()
    print 'Thread for sending email'
    #get verify code
    try:
        email_insance.send_text_email(subject, content, receiver)
    except   Exception, e:
        print '发送邮件的过程中发生错误： '+ e
    
@csrf_exempt
def save_user(request):
    
    result={}
                               
    
    if request.method == 'POST':
        if 'email' in request.POST and 'verifycode' in request.POST and 'name' in request.POST and  'pwd_1' in request.POST \
                and  'pwd_2' in request.POST:

            user_email  = request.POST["email"]
            verifycode  = request.POST["verifycode"]
            name        = request.POST["name"]
            
            pwd_1       = request.POST["pwd_1"]
            pwd_2       = request.POST["pwd_2"]
                
            #validate email format
            EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
            if not EMAIL_REGEX.match(user_email):
                result['status'] = '0'
                result['err_msg'] = '邮箱格式不正确 !'
                return HttpResponse(json.dumps(result), content_type = 'application/json')
                
                
            if pwd_1 != pwd_2:
                result['status'] = '1'
                result['err_msg'] = '您两次输入的密码不一致， 请重新输入 。 '
                return HttpResponse(json.dumps(result), content_type = 'application/json')
 
            if len(pwd_1) < 6:
                result['status'] = '2'
                result['err_msg'] = '您输入的密码还不够六位呢， 太短了， 往长点走...'
                return HttpResponse(json.dumps(result), content_type = 'application/json')
                  
            try:
                obj = User.objects.get(email__exact=user_email)
                result['status'] = '3'
                result['err_msg'] = '亲, 这个邮箱已经注册过了你是不是把密码忘了 ? '
                return HttpResponse(json.dumps(result), content_type = 'application/json')
            except User.DoesNotExist:
                try:
                    verifycode_instance = VerifyCode.objects.get(email__exact = user_email)
                    if verifycode_instance.code == verifycode:
                        try:
                            user = User(name= name, email = user_email, date=timezone.now(), password=pwd_1, is_active=True)
                            user.set_password(pwd_1)   
                            user.save()
                            verifycode_instance.delete()
                            result['status'] = '4'
                            result['suc_msg'] = '注册成功， 你可以登录了， 开始使用吧 !'
                                                  
                            Subject = 'New user in map2family'
                            email_content = 'New user: '+ user_email
                            
			    t_send_email =  threading.Thread(target=send_email, args=[Subject, email_content, settings.SUPPORTOR_EMAIL])
			    t_send_email.start()
			    
                            return HttpResponse(json.dumps(result), content_type = 'application/json') 
                        except e:
                            result['status'] = '5'
                            result['err_msg'] = '保存用户失败! ERROR: ' + e
                            return HttpResponse(json.dumps(result), content_type = 'application/json') 
                    else:
                        result['status'] = '6'
                        result['err_msg'] = '验证码不对哦， 请重新查看您的验证码!'
                        return HttpResponse(json.dumps(result), content_type = 'application/json') 
                      
                except verifycode.DoesNotExist:
                   
                    result['status'] = '7'
                    result['err_msg'] = '数据库发送错误， 出现重复的邮箱!'
                    return HttpResponse(json.dumps(result), content_type = 'application/json') 
        else:
            result['status'] = '8'
            result['err_msg'] = '参数错误， 非法的输入 !'
            return HttpResponse(json.dumps(result), content_type = 'application/json') 
            
@csrf_exempt
def get_email_verify_code(request):
    result={} 
    if request.method == 'POST':
        if 'email' in request.POST:
            email       = request.POST["email"]
            result={} 
            if not EMAIL_REGEX.match(email):
                result['status'] = '1'
                result['err_msg'] = '亲， 电子邮件格式不正确哦 !'
                 
            else:
                    
                    try:
                        obj = User.objects.get(email__exact=email)
                        result['status'] = '2'
                        result['err_msg'] = '亲， 这个邮箱已经注册过了你可以找回密码'
                        
                    except User.DoesNotExist:
                        
                        email_insance = EmailEx()
                        #get verify code
                        code    = ''.join(random.choice(string.lowercase + string.digits) for i in range(5))
                        Subject = 'map2family 注册邮箱验证码' 
                        content = '您好， 欢迎您注册map2family， 欢迎加入我们， 您的邮箱验证码是：  ' + code
                         
                        try:
                            email_insance.send_text_email(Subject, content, email)
                            try:
                                verify_code = VerifyCode.objects.get(email__exact = email, type ='0')
                                verify_code.code = code
                                verify_code.save()
                            except VerifyCode.DoesNotExist:
                                verify_code = VerifyCode(email=email, code=code, type ='0')
                                verify_code.save()
                                
                            result['status'] = '3'
                            result['err_msg'] = '验证码已发至您的邮箱中， 请到邮箱中查看您的验证码!'    
                            
                    
                        except   Exception, e:
                            result['status'] = '4'
                            result['err_msg'] = '发送邮件的过程中发生错误： '+ e
 
                    
        else:
            result['status'] = '5'
            result['err_msg'] = '非法参数， 你在干什么 !'
            
    else:
         result['status'] = '5'
         result['err_msg'] = '非法参数， 你在干什么 !'
        
    return HttpResponse(json.dumps(result), content_type = 'application/json')


@csrf_exempt
def get_reset_pwd_verify_code(request):
    
                        
    result = {}
    if request.method == 'POST':
        if 'email' in request.POST:
            email       = request.POST["email"]
            
            if not EMAIL_REGEX.match(email):
                result['status'] = 'ERROR'
                result['err_msg'] = '亲， 电子邮件格式不正确哦 !'
                return HttpResponse(json.dumps(result), content_type='application/json')
            else: 
                try:
                    user    = User.objects.get(email = email)
                except User.DoesNotExist:
                    result['status'] = 'ERROR'
                    result['err_msg'] = '用户不存在,该用户尚未注册... !'
                    return HttpResponse(json.dumps(result), content_type='application/json')  
                        
                email_insance = EmailEx()
                #get verify code
                code    = ''.join(random.choice(string.lowercase + string.digits) for i in range(4))
                Subject = 'map2family重置密码验证码' 
                content = '您好， 您正在重置您在map2family的密码，输入正确的验证码后，即可修改您的密码。  验证码是：  ' + code + ' <br />感谢您使用map2family。'
                try:
                    email_insance.send_text_email(Subject, content, email)
                except   Exception, e: 
                    result['status'] = 'ERROR'
                    result['err_msg'] = '发送邮件的过程中发生错误： '+ e
                    return HttpResponse(json.dumps(result), content_type='application/json')
                try:
                    verify_code = VerifyCode.objects.get(email__exact = email, type ='1')
                    verify_code.code = code
                    verify_code.save()
                except VerifyCode.DoesNotExist:
                    verify_code = VerifyCode(email=email, code=code, type ='1')
                    verify_code.save()
                result['status'] = 'OK'
                result['msg'] = '验证码已发至您的邮箱中， 请到邮箱中查看您的验证码 !'
                return HttpResponse(json.dumps(result), content_type='application/json')    
                
                    
        else:
            result['status'] = 'ERROR'
            result['err_msg'] = '非法参数， 你在干什么 !'
            return HttpResponse(json.dumps(result), content_type='application/json')  
    else:
        result['status'] = 'ERROR'
        result['err_msg'] = '非法参数， 你在干什么 !'
        return HttpResponse(json.dumps(result), content_type='application/json')               
@csrf_exempt
def validate_username(request):
    if request.method == 'POST':

        username    = request.POST["username"]
        try:
            User.objects.get(username = username)
            return HttpResponse('nThe username is exist, please input another one !')
        except:
            return HttpResponse('yAvailble !')
@csrf_exempt
def validate_uniqueness_email(request):
    if request.method == 'POST':
        if 'email' in request.POST :
            email    = request.POST["email"]
            users    = User.objects.filter(email = email)
            if users.count() > 0:#The email is exist
               return HttpResponse('nThe email is exist, please input another one !')
        else:
            return HttpResponse('nCannot get the email address !')   
    else:
        return HttpResponse('nMethdod error !')   


 
def go_comment(request, day_word_id):
    """
    add comment for day words
    """
    
    """
    device type
    """
    is_Mobile = dmb.process_request(request)
    
    """
    User validation 
    """
    if  request.user.is_anonymous():
                return comm.redirect_login_path(is_Mobile, request)
    
    try:    
        Day_words_instance = Day_words.objects.get(pk = day_word_id)
        #get the comment list
        comment_ls = Reltn_dayword_comm.objects.filter(day_word = Day_words_instance ) 
        
        g_dayword_list = G_daywords.objects.filter(app = Day_words_instance)
        #count = g_dayword_list.count()
        
        #get if current user praised this day_word
        Praised = False
        for g_dayword in g_dayword_list:
            if request.user == g_dayword.owner:
                Praised = True
                break
                
        context = {
                    'day_word'   : Day_words_instance,
                    'comment_ls' : comment_ls,
                    'Praised'    : Praised,
                   }
        if is_Mobile:
            return render(request, 'daywords/m_day_word_comment.html', context )
        else:                
            return render(request, 'daywords/m_day_word_comment.html', context )
        
    except Day_words.DoesNotExist:
        return HttpResponse ('start_comment ERROR CODE 4...')
    except Day_words.MultipleObjectsReturned: 
        return HttpResponse ('start_comment ERROR CODE 5...')
            
    


@csrf_exempt
def add_comment(request):
    """
    add comment for day words
    """
    
    """
    device type
    """
    is_Mobile = dmb.process_request(request)
    
    """
    User validation 
    """
    
        
    if  request.user.is_anonymous():
          return comm.redirect_login_path(is_Mobile, request)
    result = dayword_comment(request, 1)  
    return HttpResponse(json.dumps(result), content_type='application/json')
       
    
       
def dayword_comment(request, type):
    """
    type = 1, add comment
    type = 0, del comment
    
    return result{
        'status': status_value,
        'msg'   : msg_value
    }
    """ 
    #main logic
    result = {}
    day_words_id = ' '
    
    
    #validate start
    if request.method == 'POST':
        if 'day_words_id' in request.POST and 'content' in request.POST :
            day_words_id = request.POST.get('day_words_id') 
            content      = request.POST.get('content')
        else:
            #return parameter error
            result['status'] = '2'#
            result['msg']    = 'dayword_comment ERROR CODE 2...'
            return result 
    else:
        #return request method error
        result['status'] = '3'#
        result['msg']    = 'dayword_comment ERROR CODE 3...'
        return result
        
    #validate end
    #save start
    try:    
        Day_words_instance = Day_words.objects.get(pk = day_words_id)
        if type == 1:
            Day_words_instance.comment_count = Day_words_instance.comment_count+1
            Day_words_instance.save()
        
        user               = request.user
        comment_new        = Comment.objects.create(
            commenter = user, content = content
            )
        comment_new.save()
        
        Reltn_dayword_comm_instance = Reltn_dayword_comm.objects.create(
            day_word = Day_words_instance, comment = comment_new
            )
            
        Reltn_dayword_comm_instance.save()
        
        #mark the msg to True
        Day_words_instance.user.msg_mark = True
        Day_words_instance.user.save()
        
        
        #call msg app to add msg item to DB
        msg_url = reverse('base:go_comment', args={ Day_words_instance.id})
        if len( content ) > 100:
            msgtext = content[:100] + '...'
        else:
            msgtext = content
        urlpic = '' 
        type = 1 # from comment app
        MsgComm.add(Day_words_instance.user, msg_url, urlpic, msgtext, type)
        #call msg app to add msg item to DB ---end
         
        result['status'] = '1'
        result['msg']    = '评论成功...'                         
    except Day_words.DoesNotExist:
        result['status'] = '4'
        result['msg']    = 'dayword_comment ERROR CODE 4...'
    except Day_words.MultipleObjectsReturned:
        result['status'] = '5'
        result['msg']    = 'dayword_comment ERROR CODE 5...'
    return result
    
    
def applications( request):
    isMobile = dmb.process_request(request) 
      
    context = { }
    if isMobile:
        return render(request, 'basedatas/m_application.html', context)
    else:
        return render(request, 'basedatas/m_application.html', context)
        
def drag( request):
    isMobile = dmb.process_request(request)
  
    context = { }
    if isMobile:
        return render(request, 'basedatas/m_drag.html', context)
    else:
        return render(request, 'basedatas/m_drag.html', context)