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

    def get_users(self):
        return [{
            "user_id": document["user_id"],
            "username": document["username"],
        } for document in self.db.users.find()]

    def get_user(self, user_id):
        document = self.db.users.find_one({"user_id": user_id})
        if not document:
            return {}
        return {
            "user_id": document["user_id"],
            "username": document["username"],
            "birthday": document["birthday"],
            "gender": document["gender"],
        }

    def get_snapshots(self, user_id):
        return [document["timestamp"] for document in self.db.users.find({"user_id": user_id})]

    def get_snapshot(self, user_id, timestamp):
        document = self.db.snapshots.find_one({"user_id": user_id, "timestamp": timestamp})
        if not document:
            return {}
        return {
            "timestamp": document["timestamp"],
            "results": [k for k in document if k not in {"user_id", "timestamp"}]
        }

    def get_result(self, user_id, timestamp, result_name):
        document = self.db.snapshots.find_one({"user_id": user_id, "timestamp": timestamp})
        if not document:
            return {}
        return document[result_name]
