import furl as furl

from equilibrium.queue.rabbitmq import RabbitMQAdapter
from equilibrium.utils.wait_for_tcp_port import wait_for_port


class QueueHandler:
    queue_adapters = {"rabbitmq": RabbitMQAdapter}

    def __init__(self, url):
        f = furl.furl(url)
        wait_for_port(f.host, f.port)
        self.adapter = self.queue_adapters[f.scheme](f.host, f.port)

    def publish(self, *args, **kwargs):
        self.adapter.publish(*args, **kwargs)

    def consume(self, *args, **kwargs):
        self.adapter.consume(*args, **kwargs)
