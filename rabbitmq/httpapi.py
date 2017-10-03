 

import configparser
import os
import pdb
import requests


from  readconf import ReadConf


class HttpApi(object):
    """this is wrapper for rabbit MQ HTTP API"""

    HEADERS = {'content-type': 'application/json'}

    USERNAME = ''
    PASSWORD = ''

    EXCHANGE_URL = ''
    QUEUE_URL = ''

    def __init__(self):
        conf = ReadConf()
        self.USERNAME = conf.username
        self.PASSWORD = conf.password

        self.EXCHANGE_URL = conf.exchangeurl
        self.QUEUE_URL = conf.queue_url

    def get_exchanges(self, headers=HEADERS):
        """
        get the exchanges from rabbit MQ server
        Parameters:
             headers: the headers of request
        Return:
            return status code and the list,
            if success, status code is 200, and contains the list of exchanges
            else only return the request code
        """

        req = requests.get(self.EXCHANGE_URL, headers=headers, auth=(self.USERNAME, self.PASSWORD))

        result = {}
        result['status_code'] = req.status_code

        if req.status_code == 200:
            ls_json = req.json()
            ls = []

            for l in ls_json:
                ls.append(l)
            result['ls'] = ls
            return result
        else:
            return result

    def get_exchange_names(self, headers=HEADERS):
        """
        get the exchanges' name from rabbit MQ server
        Parameters:
             url: the API url
             headers: the headers of request
             username: the username in rabbit MQ, default is guest
             password: the password for the username in rabbit MQ, default is guest
        Return:
            return status code and the list, result['status_code'] and result['ls']
            if success, status code is 200, and contains the list of exchanges
            else only return the request code
        """
        ls_exchanges_result = self.get_exchanges(headers=headers)
        result = {}

        if ls_exchanges_result['status_code'] != 200:
            result['status_code'] = ls_exchanges_result['status_code']
            return result

        result['status_code'] = 200
        ls_exchange_names = []
        for ls in ls_exchanges_result['ls']:
            ls_exchange_names.append(ls['name'])
        result['ls'] = ls_exchange_names

        return result

    def check_exchange(self, exchange_name):
        """check if the specified exchange exist in server"""
        result = self.get_exchange_names()
        if result['status_code'] == 200:
            exchange_name = exchange_name.strip()
            if exchange_name in result['ls']:
                return True
            else:
                return False
        else:
            raise Exception(' HTTP API status code is %d' % result['status_code'])

    def get_queues(self, headers=HEADERS):
        """Get all queues from server"""
        result = {}
        req = requests.get(self.QUEUE_URL, headers=headers, auth=(self.USERNAME, self.PASSWORD))
        result['status_code'] = req.status_code
        if req.status_code == 200:
            ls_json = req.json()
            ls = []
            for l in ls_json:
                ls.append(l)

            result['ls'] = ls
        else:
            raise Exception('Request status code is %d' % req.status_code)

        return result

    def get_queue_names(self, headers=HEADERS):
        """get all queue names from the queue list"""
        result = self.get_queues()
        queue_ls = result['ls']
        queuename_ls = []
        for queue in queue_ls:
            queuename_ls.append(queue['name'])

        return queuename_ls

    def check_queue(self, queue_name):
        """check if a queue is in server"""
        queuename_ls = self.get_queue_names()
        if len(queuename_ls) > 0:
            queue_name = queue_name.strip()
            if queue_name in queuename_ls:
                return True
            else:
                return False

        else:
            return False


if __name__ == "__main__":
    api = HttpApi()
    ls = api.check_queue('celery')
    if ls:
        print('true')
    else:
        print('false')

