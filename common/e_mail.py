import smtplib
from email import encoders
from email import utils
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText
from django.conf import settings
import pdb
import re

class Email(object):
    EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')

    def send_text_email(self,Subject,preamble,content,receiver):
        if settings.EMAIL_SWITCH:
            sender              = 'zhaji25@ca.com'
            themsg              = MIMEMultipart()
            themsg['Subject']   = Subject
            themsg['To']        = receiver
            themsg['From']      = 'L2 Tools Management System'
            themsg.preamble     = preamble

            msgAlternative      = MIMEMultipart('alternative')
            themsg.attach(msgAlternative)
            content = content + '<br/>www.map2family.com'
            msgText = MIMEText(content,'html', 'utf-8')
            msgAlternative.attach(msgText)
            themsgtest = themsg.as_string()      
            # send the message
            try:
                smtp = smtplib.SMTP(settings.SMTP_SERVER)#SMTP server IP, or postfix server in linux
                smtp.sendmail(sender, receiver, themsgtest)
                smtp.close()#close the connnection
                return 'email has been sent successfully'
            except Exception as e: 
                return e
        
class EmailEx(Email):
    def send_text_email(self,Subject,content,receiver):
        if settings.EMAIL_SWITCH:
            sender              = 'postmaster@map2family.com'
            themsg              = MIMEMultipart()
            themsg['Subject']   = Subject
            themsg['To']        = receiver
            themsg['From']      = settings.PROJECTNAME
            themsg['Date']      = utils.formatdate(localtime = 1)
            themsg['Message-ID'] = utils.make_msgid()
            msgAlternative      = MIMEMultipart('alternative')
            themsg.attach(msgAlternative)
            content = content + '<br/>www.map2family.com'
            msgText = MIMEText(content,'html', 'utf-8')
            msgAlternative.attach(msgText)
            themsgtest = themsg.as_string()      
            # send the message
            server = smtplib.SMTP()  
            server.connect(settings.SMTP_SERVER) 
            server.login(settings.SMTP_SERVER_USER, settings.SMTP_SERVER_PWD)
            server.sendmail(sender, receiver, themsgtest)
            server.quit()#SMTP.quit()
   
    @staticmethod        
    def send_html_email( Subject,content,receiver):
        if settings.EMAIL_SWITCH: 
            html = open(settings.TEMPLATES[0]['DIRS'][0] + '\\basedatas\\email.html', 'r')
            data = html.read()
            html.close() 
             
            data = data.replace('CONTENT', content)
             

            sender              = 'postmaster@map2family.com'
            themsg              = MIMEMultipart()
            themsg['Subject']   = Subject
            themsg['To']        = receiver
            themsg['From']      = settings.PROJECTNAME
            themsg['Date']      = utils.formatdate(localtime = 1)
            themsg['Message-ID'] = utils.make_msgid()
            msgAlternative      = MIMEMultipart('alternative')
            themsg.attach(msgAlternative)
            content = content + '<br/>www.map2family.com'
            msgText = MIMEText(content,'html', 'utf-8')
            msgAlternative.attach(msgText)
            themsgtest = themsg.as_string()     
            # send the message
            server = smtplib.SMTP()  
            server.connect(settings.SMTP_SERVER) 
            server.login(settings.SMTP_SERVER_USER, settings.SMTP_SERVER_PWD)
            server.sendmail(sender, receiver, themsgtest)
            server.quit()#SMTP.quit()