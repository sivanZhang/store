import os
import pdb
import requests
import json
import sys
import time
import importlib

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

    def __init__(self, configfile):
        """
        read configuration file
        """  
        self.queue_avail = rabbit_conf['Q_AVAILABLE_GOODS']
        self.queue_outfile = rabbit_conf['Q_REAL_GOODS']

        self.http_protocol = globalinfo['HTTP_PROTOCOL']
        self.apiserver = storeserver['IP']
        self.serverport = storeserver['PORT']

        self.get_node_api = storeserver['API_GET_NODE']
        self.cert = storeserver['CERT_VERIFY']
         
        self.get_compute_api = storeserver['API_RUN_COMPUTE'] 

        self.username = storeserver['API_SERVER_USER']
        self.password = storeserver['API_SERVER_PWD']
        self.auth = HTTPBasicAuth(self.username, self.password)
        
        self.apiserver_url = '{0}://{1}:{2}'.format(self.http_protocol, self.apiserver, self.serverport)
      
    def conn(self):
        """
        connect to rabbitmq as a consumer
        """
        self.consumer = Consumer()
        print ('connected to rabbit...')
               
    def get_node(self, simfunction):
        """get the available remote node to calculate the automation"""

        httpurl = self.apiserver_url + self.get_node_api
        httpurl += '?simfunction='+simfunction
        while(True):
            if self.http_protocol.lower() == 'https':
                req = requests.get(httpurl, verify = self.cert)
            else:
                req = requests.get(httpurl)

            if req.status_code == 200:
                node_json = req.content.decode()
                nodeinfo = json.loads(node_json)
                nodeurl = ''
                if 'error' in nodeinfo: 
                    print(nodeinfo['error']) 
                    continue

                if 'protocol' in nodeinfo:
                    nodeurl = nodeinfo['protocol'] + '://'
                else:
                    raise KeyError('protocol is not in json')

                if 'identifier' in nodeinfo:
                    nodeurl += nodeinfo['identifier'] + ':'
                else:
                    raise KeyError('machine name or IP is not in json')

                if 'port' in nodeinfo:
                    nodeurl += str(nodeinfo['port'])
                else:
                    raise KeyError('port is not in json')
                
                if 'nodeid' in nodeinfo:
                    self.nodeid = nodeinfo['nodeid']
                else:
                    raise KeyError('Node ID is not in json')

                self.nodeurl = nodeurl 
                return self.nodeurl
            else:
                print('Failed to get node information, request status code is ' + str(req.status_code))
                print('try to get node again...')
                time.sleep(5)
               
    def basic_consume_compute(self, prefetch_count=1):
        if prefetch_count > 0:
            self.consumer.channel.basic_qos(prefetch_count=prefetch_count)
        
        def basic_callback(ch, method, properties, body):
            # send to remote node to compute
            msg = json.loads(body.decode())
            param = {
                'result_dir': msg['result_dir'],
                'json': msg['json'],
                'id': msg['id'],
                'simfunction': msg['simfunction'],
                'hasFile': msg['hasFile'],
            }
            
            if msg['hasFile'] == True:
                status = self.upload(msg['id'], msg['simfunction'])
                if status['result'] == False:
                    self.update(id=msg['id'], status=self.OtherError, 
                          msg='Node return error when uploading file to node,detail msg:{}'.format(status['msg']))
                    return

            nodeurl = self.get_node(msg['simfunction'])
            http = nodeurl + self.get_compute_api
            
            # add task counter
            add_task_url = self.apiserver_url + self.taskcounter_api
            headers = {"Authorization": "" }
            if self.http_protocol.lower() == 'https':
                headers['referer'] = '/' 
                requests.post(add_task_url, data={'nodeid': self.nodeid, 'counter': 1}, verify=self.cert)
            else:
                requests.post(add_task_url, data={'nodeid': self.nodeid, 'counter': 1})
             
            auth = self.auth 
            if self.http_protocol.lower() == 'https':
                headers['referer'] = '/'
                req = requests.post(http, data=param, headers=headers, auth=auth, verify=self.cert)
            else:
                req = requests.post(http, data=param, headers=headers, auth=auth)
            
            # decrease task counter
            print('request status code is ' + str(req.status_code))
            if req.status_code == 200:
                self.consumer.channel.basic_ack(delivery_tag=method.delivery_tag)
            else:
                #self.consumer.close_connection()
                self.update(id=msg['id'], status=self.OtherError, 
                          msg='Node return error[status code is {0}] when computing. details:{1}'.format(str(req.status_code), req.text))
                #raise Exception('Compute failed in remote node, status code :'
                #                + str(req.status_code)+'reason: '+req.text)
            if self.http_protocol.lower() == 'https':
                requests.post(add_task_url, data={'nodeid': self.nodeid, 'counter': -1}, verify=False)
            else:
                requests.post(add_task_url, data={'nodeid': self.nodeid, 'counter': -1})

        self.consumer.basic_consume(basic_callback, self.queue_avail)
          
    def run_consume(self, computing_num, file_num):
        """
        start consumer for computing and filehandler
        """
        self.conn()
        self.basic_consume_compute(computing_num) 
        self.consumer.channel.start_consuming()

    def stop_consume(self):
        """
        start consumer for computing and filehandler
        """ 
        self.consumer.channel.stop_consuming()
        self.consumer.channel.close()
        self.consumer.close_connection()
    
    def upload(self, resultid, simfunction):
        """
        call api to upload file from center server to node server
        """
        if not self.nodeurl:
            self.get_node(simfunction)
        
        node_upload_input_file_api = self.nodeurl + self.node_upload_input_file_api
        center_upload_input_file_api = self.center_upload_input_file_api.format(resultid, node_upload_input_file_api)
        center_upload_input_file_api = self.apiserver_url + center_upload_input_file_api

        auth = HTTPBasicAuth(self.username, self.password)
        if self.http_protocol.lower() == 'https':
            req = requests.get(center_upload_input_file_api, auth=auth, headers={'referer':'/'}, verify=self.cert)
        else:
            req = requests.get(center_upload_input_file_api, auth=auth)
        status={}
        if req.status_code == 200:
            status['result'] = True
             
        else:
            print(req.text)
            status['result'] = False
            status['msg'] = req.text
        return status

    def update(self, id, status, msg, output=''):
        """
        when node return server internal error 500, delivery need to update the result
        tell them what happened.
        """
        apiserver = self.apiserver_url
        result_update_api = self.update_result_api.format(id)
        apiurl = (apiserver + result_update_api) 

        param  = {
            'status': status,
            'pk': id,
            'output': output,
            'msg': msg,
        }
        
        auth = HTTPBasicAuth(self.username, self.password)
       
        if self.http_protocol.lower() == 'https':
            req = requests.put(apiurl, data=param, auth=auth, headers={'referer':'/'}, verify=self.cert)
        else:
            req = requests.put(apiurl, data=param, auth=auth)


if __name__ == "__main__":
    delivery = Delivery(os.path.join(BASE_DIR, 'server.conf'))
    delivery.run_consume(2, 2)