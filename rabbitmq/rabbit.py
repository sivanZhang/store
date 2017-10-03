 
import pika
import pdb
import time
import importlib

from  readconf import ReadConf


class Rabbit(object):
    """this class fetch messages from queue"""

    TOPIC = 'topic'
    DIRECT = 'direct'
    FANOUT = 'fanout'
    SLEEP = 5

    def __init__(self, connection=None):
        """
        get connection with RabbitMQ server, and initialize the channel.

        Parameters:
            host: the hostname of RabbitMQ
            username: the username in RabbitMQ, the default value is 'guest'
            password: the password in RabbitMQ, the default value is 'guest'

        Raises:
            pika.exceptions.ConnectionClosed: raise an exception if cannot
                 host
            pika.exceptions.ProbableAuthenticationError: raise an exception
                if the username or password error
        """
        if connection:
            if isinstance(connection, pika.BlockingConnection):
                self.connection = connection
                self.channel = self.connection.channel()
            else:
                raise TypeError('connection should be the instance of pika.BlockingConnection')
        else:
            self.conf = ReadConf()
            _credentials = pika.PlainCredentials(self.conf.username, self.conf.password)
            _parameters = pika.ConnectionParameters(host=self.conf.host, port=self.conf.port, credentials=_credentials)
            
            try: 
                self.connection = pika.BlockingConnection(_parameters)
                self.channel = self.connection.channel()
            except pika.exceptions.ConnectionClosed as e: 
                raise Exception('ERROR: Connect to {} failed, machine name or port error, try again...'.format(self.conf.host))
            except pika.exceptions.ProbableAuthenticationError as e:
                raise Exception('ERROR: Connect to {} failed, probable username or password error, try again...'.format(self.conf.host)) 
            """
            while(True):
                self.conf = ReadConf()
                _credentials = pika.PlainCredentials(self.conf.username, self.conf.password)
                _parameters = pika.ConnectionParameters(host=self.conf.host, port=self.conf.port, credentials=_credentials)
                
                try: 
                    self.connection = pika.BlockingConnection(_parameters)
                    self.channel = self.connection.channel()
                    break
                except pika.exceptions.ConnectionClosed as e: 
                    print ('ERROR: Connect to {} failed, machine name or port error, try again...'.format(self.conf.host)) 
                    time.sleep(self.SLEEP)  
                except pika.exceptions.ProbableAuthenticationError as e:
                    print ('ERROR: Connect to {} failed, probable username or password error, try again...'.format(self.conf.host)) 
                    time.sleep(self.SLEEP) 
            """

    def set_topic_exchange(self, exchange_name, durable=True, passive=False):
        """
        declare or check a exchange with topic type

        Parameters:
            exchange_name: the exchange name

        Raise:
            if the exchange exist with non-topic type, it will raise an exception
        """
        self.exchange_name = exchange_name
        self.exchange_type = Rabbit.TOPIC
        try:
            self.channel.exchange_declare(exchange=exchange_name,
                                          exchange_type=Rabbit.TOPIC,
                                          passive=passive,
                                          durable=durable)
        except pika.exceptions.ChannelClosed as e:
            raise Exception(e)

    def declare_queue(self, queue, durable=True):
        self.channel.queue_declare(queue, durable=durable)

    def close_connection(self):
        self.connection.close()
