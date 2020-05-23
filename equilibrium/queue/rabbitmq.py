import pika


class RabbitMQAdapter:
    def __init__(self, host, port):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, port))

    def publish(self, exchange="", routing_key="", body=""):
        channel = self.connection.channel()
        channel.basic_qos(prefetch_count=1)
        if exchange:
            channel.exchange_declare(exchange=exchange, exchange_type="fanout", durable=True)
        if routing_key:
            channel.queue_declare(queue=routing_key, durable=True)
        channel.basic_publish(exchange, routing_key, body)

    def consume(self, queue, callback, exchange=""):
        channel = self.connection.channel()
        channel.basic_qos(prefetch_count=1)
        if exchange:
            channel.exchange_declare(exchange=exchange, exchange_type="fanout", durable=True)
        channel.queue_declare(queue)
        if exchange:
            channel.queue_bind(exchange=exchange, queue=queue)
        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
