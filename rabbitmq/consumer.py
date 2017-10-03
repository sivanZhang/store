 
import pika
import pdb

from  rabbit import Rabbit
from  httpapi import HttpApi


class Consumer(Rabbit):
    """this class fetch messages from queue"""

    def __init__(self, connection=None):
        super(Consumer, self).__init__(connection)

    def check_exchange(self, exchange_name):
        """
        check if exchange exist in RabbitMQ server.
             string exchange_name: the name of exchange
        Return:
            if the exchange exist, return True
            else return False
        """
        if not isinstance(exchange_name, str):
            raise TypeError('exchange name must be string')

        if len(exchange_name) == 0:
            raise ValueError('exchange name can not be empty here.')

        httpapi = HttpApi()
        name_result = httpapi.get_exchange_names()
        if name_result['status_code'] == 200:
            name_list = name_result['ls']
            if exchange_name in name_list:
                return True
            else:
                return False
        else:
            raise Exception('Can not get exchange name list from HTTP API, please check ' +
                            'if rabbitmq-management is enabled')

    def basic_qos(self, callback=None, prefetch_size=0, prefetch_count=0, all_channels=False):
        return self.channel.basic_qos(callback=callback, prefetch_size=prefetch_size,
                                      prefetch_count=prefetch_count, all_channels=all_channels)

    def consume(self, queue, no_ack=False,
                exclusive=False, arguments=None,
                inactivity_timeout=None):
        return self.consume(queue, no_ack, exclusive, arguments, inactivity_timeout)

    def basic_consume(self, consumer_callback, queue, no_ack=False,
                      exclusive=False, consumer_tag=None, arguments=None):
        return self.channel.basic_consume(consumer_callback, queue, no_ack,
                                          exclusive, consumer_tag, arguments)

if __name__ == "__main__":
    consume = Consumer()
    print(consume.check_exchange('consumer'))
