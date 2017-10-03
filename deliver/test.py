import configparser
import os
import pdb
import requests
import json
from requests import Request, Session
from requests.auth import HTTPBasicAuth
import codecs

from  base64 import b64encode
import urllib
from deliver import Delivery
def test1():
    http = 'http://sc-server:8000/api/results/74/'
    param = {
        'status': 1,
        'pk': 75,
        'ouput'    :  'sdfsdfsd'
    }
    data = urllib.parse.urlencode(param)
    basic = b64encode(('admin:admin').encode(encoding="utf-8") ) 
    req=urllib.request.Request(http,  data.encode(encoding="utf-8"))
    req.add_header('Authorization', 'Basic '+ basic.decode())
    req.get_method = lambda: 'PUT'
    print(req.headers['Authorization'])
    try:
        f=urllib.request.urlopen(req)
        print(f.getcode())
    except urllib.error.HTTPError  as he:
        print('Error : %s'%he)
        print(type(he))
        print(he.getcode())
        print(dir(he))
        print(he.msg)

def test2():
    http = 'http://sc-server:8000/api/results/74/'
    
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, http, 'admin', 'addmin')
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    print(dir(opener))
    urllib.request.install_opener(opener)
    req = urllib.request.urlopen(http)
    print(req.getcode())

def test3():
    http = 'http://127.0.0.1:8000/api/fileserver/user_verify/'
    param = {
        'status': 1,
        'pk': 75,
        'ouput'    :  'sdfsdfsd'
    }
    req = requests.post(http, data=param , auth=('admin', 'admin'))
    print(req.text)
    print(req.status_code)
    with codecs.open('log.html', 'a+', 'utf-8-sig') as des:
        des.write(req.text)
        
if __name__ == "__main__":
    print (os.path.abspath(__file__))
    print (os.path.dirname(os.path.abspath(__file__)))
    delivery = Delivery('consumer.conf')
    delivery.run_consume(2, 2)
   
     
