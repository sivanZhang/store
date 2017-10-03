import configparser
import os
import pdb
import sys
import importlib 
from server import rabbit, rabbithttpapi, rabbitserverinfo
 
class ReadConf(object):
    """read configuration from rabbit.conf"""

    def __init__(self):
        self.username = rabbitserverinfo['username']
        self.password = rabbitserverinfo['password']
        self.host = rabbitserverinfo['host']
        self.port = rabbitserverinfo['port']

        self.rooturl = rabbithttpapi['root_url']

        self.exchangeurl = self.rooturl + rabbithttpapi['exchange_url']
        self.queue_url = self.rooturl + rabbithttpapi['queue_url']
    def read_conf(self):
        rabbitserverinfo_section = 'rabbitserverinfo'
        httpapi_sectionname = 'rabbithttpapi'
        config = configparser.ConfigParser()
        configfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'server.conf')
        if os.path.isfile(configfile):
            config.read(configfile)
            self.username = config.get(rabbitserverinfo_section, 'username')
            self.password = config.get(rabbitserverinfo_section, 'password')
            self.host = config.get(rabbitserverinfo_section, 'host')
            self.port = config.getint(rabbitserverinfo_section, 'port')

            self.rooturl = config.get(httpapi_sectionname, 'root_url')

            self.exchangeurl = self.rooturl + config.get(httpapi_sectionname, 'exchange_url')
            self.queue_url = self.rooturl + config.get(httpapi_sectionname, 'queue_url')
        else:
            raise Exception('cannot file configuration file')
    def read_py(self): 
        self.username = rabbitserverinfo['username']
        self.password = rabbitserverinfo['password']
        self.host = rabbitserverinfo['host']
        self.port = rabbitserverinfo['port']

        self.rooturl = rabbithttpapi['root_url']

        self.exchangeurl = self.rooturl + rabbithttpapi['exchange_url']
        self.queue_url = self.rooturl + rabbithttpapi['queue_url']
          
if __name__ == "__main__":
    r = ReadConf()
    r.read_py()
    print(r.username)
    print(r.password)
    print(r.exchangeurl)
    print(r.queue_url)

