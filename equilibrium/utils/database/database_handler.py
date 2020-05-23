import furl as furl

from equilibrium.utils.database.mongo import MongoDBAdapter
from equilibrium.utils.general.wait_for_tcp_port import wait_for_port


class DatabaseHandler:
    database_adapters = {"mongodb": MongoDBAdapter}

    def __init__(self, url):
        f = furl.furl(url)
        wait_for_port(f.host, f.port)
        self.adapter = self.database_adapters[f.scheme](f.host, f.port)

    def save_data(self, *args, **kwargs):
        self.adapter.save_data(*args, **kwargs)
