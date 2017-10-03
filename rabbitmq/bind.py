#!/usr/bin/env python
import pika

from  rabbit import Rabbit


class Bind(Rabbit):
    """bind exchange with queue"""

    def __init__(self, connection=None):
        super(Bind, self).__init__(connection)

    def bind_topic(self, exchange, queue, route_key, durable=True):
        """
        bind the exchange with topic type to queue
        Topic exchange
        Topic exchange is powerful and can behave like other exchanges.
        When a queue is bound with "#" (hash) binding key - it will receive all the messages,
         regardless of the routing key - like in fanout exchange.
        When special characters "*" (star) and "#" (hash) aren't used in bindings,
         the topic exchange will behave just like a direct one.

        Parameters:
             exchange: the exchange name, cannot be empty here
             queue:    the queue name, cannot be empty here
             route_key: the route key string, cannot be empty here
        Raise:
             will raise exception if exchange, queue, or route_key is empty
        """

        # start validate parameters
        if not isinstance(exchange, str):
            raise TypeError('exchange must be string')
        if not isinstance(queue, str):
            raise TypeError('queue must be string')
        if not isinstance(route_key, str):
            raise TypeError('route_key must be string')

        if len(exchange.strip()) == 0:
            raise ValueError('exchange name cannot be empty here')

        if len(queue.strip()) == 0:
            raise ValueError('queue name cannot be empty here')

        if len(route_key.strip()) == 0:
            raise ValueError('route key cannot be empty here')
        # end validate parameters

        self.channel.queue_declare(queue, durable=durable)
        try:
            self.channel.exchange_declare(exchange=exchange,
                                          exchange_type='topic',
                                          durable=durable)
        except pika.exceptions.ConnectionClosed as e:
            raise Exception(e)

        self.channel.queue_bind(exchange=exchange,
                                queue=queue,
                                routing_key=route_key)
