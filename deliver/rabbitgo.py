#!/usr/bin/env python
import os
import pdb
import configparser

import sys
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(basedir, '../'))

from  rabbit import Rabbit
from  readconf import ReadConf
from  bind import Bind
from server import rabbit as rabbit_conf

class RabbitGo(Rabbit):
    """read configuration file, do the following jobs:

        # first: check or declare exchange
        # two  : check or declare queues
        # three : bind exchange or queue
    """
    conf = ReadConf()

    def __init__(self, connection=None):
        """get connection with the rabbit server"""
        super(RabbitGo, self).__init__(connection)

    def go_steps_conf(self):
        """
        move three steps:
        # first: check or declare exchange
        # two  : check or declare queues
        # three : bind exchange or queue
        """  
        # step1: check or declare exchange
        exchange = rabbit_conf['EXCHANGE'].strip()
        if len(exchange) == 0:
            raise ValueError('Exchange name in svr.conf cannot be empty')
        self.set_topic_exchange(exchange)
        print('Step 1: exchange declared')

        # step2: check or declare
        queue_avail = rabbit_conf['Q_AVAILABLE_GOODS']
        self.declare_queue(queue_avail)

        queue_real = rabbit_conf['Q_REAL_GOODS']
        self.declare_queue(queue_real)
        print('Step 2: queue {0} and {1} declared '.format(queue_real, queue_avail))

        # step3 bind queue and exchange
        bind = Bind(self.connection)
        avail_bind_key = rabbit_conf['KEY_FOR_Q_AVAIL']
        bind.bind_topic(exchange, queue_avail, avail_bind_key)

        real_bind_key = rabbit_conf['KEY_FOR_Q_REAL']
        bind.bind_topic(exchange, queue_real, real_bind_key)
        print('Step 3:  key {0} and {1} binded '.format(avail_bind_key, real_bind_key))
        print('Done.')
    

if __name__ == "__main__":
    rgo = RabbitGo()
    rgo.go_steps_conf()
    rgo.close_connection()
