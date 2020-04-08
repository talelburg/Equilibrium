import furl as furl

from equilibrium.queue.rabbitmq import RabbitMQAdapter


class QueueHandler:
    queue_adapters = {"rabbitmq": RabbitMQAdapter}

    def __init__(self, url):
        f = furl.furl(url)
        self.adapter = self.queue_adapters[f.scheme](f.host, f.port)

    def publish(self, *args, **kwargs):
        self.adapter.publish(*args, **kwargs)
