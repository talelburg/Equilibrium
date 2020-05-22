import pika


class RabbitMQAdapter:
    def __init__(self, host, port):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, port))

    def publish(self, exchange, routing_key, body):
        channel = self.connection.channel()
        channel.queue_declare(routing_key)
        channel.basic_publish(exchange, routing_key, body)
