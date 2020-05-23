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

    def get_users(self):
        return self.adapter.get_users()

    def get_user(self, user_id):
        return self.adapter.get_user(user_id)

    def get_snapshots(self, user_id):
        return self.adapter.get_snapshots(user_id)

    def get_snapshot(self, user_id, timestamp):
        return self.adapter.get_snapshot(user_id, timestamp)

    def get_result(self, user_id, timestamp, result_name):
        return self.adapter.get_result(user_id, timestamp, result_name)
