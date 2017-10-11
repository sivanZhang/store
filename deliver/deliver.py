import os
import pdb
import requests
import json
import sys
import time
import importlib
import logging

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

import pika

import rabbitmq
from requests import Request, Session
from requests.auth import HTTPBasicAuth
from rabbitmq.consumer import Consumer
from rabbitmq.server import globalinfo, storeserver 
from rabbitmq.server import rabbit as rabbit_conf


class Delivery(object):
    """deliver the message from queue to remote node"""
    requests.packages.urllib3.disable_warnings()
    OtherError = 4
    nodeurl = ''

    logging.basicConfig(level=logging.ERROR, datefmt='%a, %d %b %Y %H:%M:%S', 
                     filename='delivery.log', filemode='a+')

    def __init__(self, configfile):
        """
        read configuration file
        """  
        self.queue_avail = rabbit_conf['Q_AVAILABLE_GOODS']
        self.queue_real = rabbit_conf['Q_REAL_GOODS']

        self.http_protocol = globalinfo['HTTP_PROTOCOL']
        self.apiserver = storeserver['IP']
        self.serverport = storeserver['PORT']

        self.bill_submit_api = storeserver['BILL_SUBMIT_API']
        self.cert = storeserver['CERT_VERIFY']
          
        self.username = storeserver['API_SERVER_USER']
        self.password = storeserver['API_SERVER_PWD']
        self.auth = HTTPBasicAuth(self.username, self.password)
        
        self.apiserver_url = '{0}://{1}:{2}'.format(self.http_protocol, self.apiserver, self.serverport)
        print(self.apiserver_url)
      
    def conn(self):
        """
        connect to rabbitmq as a consumer
        """
        self.consumer = Consumer()
        print ('connected to rabbit...')
                
    def basic_consume_submit_bill(self, prefetch_count=1):
        if prefetch_count > 0:
            self.consumer.channel.basic_qos(prefetch_count=prefetch_count)
        
        def basic_callback(ch, method, properties, body): 
            msg = json.loads(body.decode())
            param = {
                'billid': msg['billid'] 
            } 
              
            submitbill_url = self.apiserver_url + self.bill_submit_api.format(msg['billid'] )
            headers = {"Authorization": "" }
             
            auth = self.auth 
            if self.http_protocol.lower() == 'https':
                headers['referer'] = '/'
                req = requests.get(submitbill_url, data=param, headers=headers, auth=auth, verify=self.cert)
            else:
                req = requests.get(submitbill_url, data=param, headers=headers, auth=auth)
            
            logging.info(msg)
            if req.status_code == 200: 
                self.consumer.channel.basic_ack(delivery_tag=method.delivery_tag)
            else:
                logging.error('Node return error[status code is {0}] when computing. details:{1}'.format(str(req.status_code), req.text))
  
        self.consumer.basic_consume(basic_callback, self.queue_avail)
          
    def run_consume(self, prefetch_count):
        """
        start consumer for computing and filehandler
        """
        self.conn()
        self.basic_consume_submit_bill(prefetch_count) 
        self.consumer.channel.start_consuming()

    def stop_consume(self):
        """
        start consumer for computing and filehandler
        """ 
        self.consumer.channel.stop_consuming()
        self.consumer.channel.close()
        self.consumer.close_connection()
     
if __name__ == "__main__":
    delivery = Delivery(os.path.join(BASE_DIR, 'server.conf'))
    delivery.run_consume(1)