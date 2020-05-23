import pymongo


class MongoDBAdapter:
    def __init__(self, host, port):
        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client.db

    def save_data(self, user_information, timestamp, data):
        users = self.db.users
        snapshots = self.db.snapshots
        query = {"user_id": user_information.user_id}
        if not users.find_one(query):
            users.insert_one({
                "user_id": user_information.user_id,
                "username": user_information.username,
                "birthday": user_information.birthday,
                "gender": user_information.gender
            })
        query["timestamp"] = timestamp
        if not snapshots.find_one(query):
            snapshots.insert_one(query)
        snapshots.find_one_and_update(query, {"$set": data})
