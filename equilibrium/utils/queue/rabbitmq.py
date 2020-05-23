import pika


class RabbitMQAdapter:
    def __init__(self, host, port):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, port))

    def publish(self, exchange="", routing_key="", body=""):
        channel = self.connection.channel()
        if exchange:
            channel.exchange_declare(exchange=exchange, exchange_type="fanout", durable=True)
        if routing_key:
            channel.queue_declare(queue=routing_key, durable=True)
        print(exchange, routing_key, body)
        channel.basic_publish(exchange, routing_key, body)

    def consume(self, queue, callback, exchange=""):
        def rabbitmq_callback(channel, method, properties, body):
            callback(body)
            channel.basic_ack(delivery_tag=method.delivery_tag)

        channel = self.connection.channel()
        channel.queue_declare(queue)
        if exchange:
            channel.exchange_declare(exchange=exchange, exchange_type="fanout", durable=True)
            channel.queue_bind(exchange=exchange, queue=queue)
        channel.basic_consume(queue=queue, on_message_callback=rabbitmq_callback, auto_ack=False)
        channel.start_consuming()
