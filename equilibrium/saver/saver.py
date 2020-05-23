import json

from equilibrium.utils.database import DatabaseHandler
from equilibrium.utils.sample import SampleHandler


class Saver:
    def __init__(self, url):
        self.db = DatabaseHandler(url)

    def save(self, topic, data):
        json_dict = json.loads(data)
        snapshot_data = SampleHandler.json_to_data(json_dict)
        self.db.save_data(snapshot_data["user_information"], snapshot_data["snapshot"].datetime, json_dict["result"])
