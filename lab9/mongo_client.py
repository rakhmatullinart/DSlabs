import pymongo
from datetime import datetime


class Connection:

    def __init__(self, ):
        self.client = pymongo.MongoClient("mongodb://18.218.33.242:27017/?replicaSet=rs0")

        self.db = self.client['chat-app']
        self.messages = self.db['messages']
        self.users = self.db['users']

    # Message functions
    def get_messages(self, max_limit=50):
        """Retrieves the messages from a chatroom."""
        results = self.messages.find({}, limit=max_limit)  # Get the messages
        results = results.sort('date', pymongo.ASCENDING)
        return results

    def add_message(self, author, content):
        """Adds a message to the database."""
        message = {
            'user': author,
            'date': datetime.now(),
            'content': content
        }
        self.messages.insert_one(message)
