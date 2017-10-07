 
import pika
import pdb

from rabbitmq.rabbit import Rabbit


class Publisher(Rabbit):
    """
    Produce messages to Rabbit Queue
    """

    def __init__(self,  connection=None):
        super(Publisher, self).__init__(connection)

    def publish_message(self, exchange_name, message, route_key):
        """
        this method is used to send message to queue, you can specify the exchange name
        by call method set_exchange.

        Parameters:
             message:
             route_key:
        raises:
            ValueError: the route_ek
        """

        self.channel.basic_publish(exchange=exchange_name, routing_key=route_key, body=message)

if __name__ == "__main__":
    p = Publisher()
    p.publish_message('store_exchange', 'REAL: hi i am jeawy', 'msg_real')
    
