from django.db import models
import pdb
import random
import string
from django.conf import settings
from common.e_mail import EmailEx
 

class CodeManager(models.Manager):
    """
    验证码的manager
    """
    email = EmailEx()
     
  
    def send_code(self, email):
        result={} 
        if not self.email.EMAIL_REGEX.match(email):
            result['status'] = 1
            result['msg'] = '电子邮件格式不正确'
        else: 
            code    = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(4))
            Subject = settings.PROJECTNAME+'注册邮箱验证' 
            content = '您好， 欢迎您注册， 欢迎加入我们， 您的邮箱验证码是： ' + code
            try:
                self.email.send_text_email(Subject, content, email)
                try:
                    verify_code = self.model.objects.get(email__exact = email, type ='0')
                    verify_code.code = code
                    verify_code.save()
                except self.model.DoesNotExist:
                    verify_code = self.model(email=email, code=code, type ='0')
                    verify_code.save()
                    
                result['status'] = 2
                result['msg'] = '验证码已发至您的邮箱中， 请到邮箱中查看您的验证码!'  
            except Exception as e:
                result['status'] = 3 
                result['msg'] = '发送邮件的过程中发生错误： '+ str(e)

        return result
    
    def veirfy_code(self, code, email): 
        try:
            verify_code = self.model.objects.get(email__exact = email, code =code)
            return True
        except self.model.DoesNotExist:
            return False

class AdaptorCodeManager(CodeManager):
    pass