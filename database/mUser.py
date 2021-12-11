from hashlib import scrypt
from flask_mongoengine import MongoEngine

db = MongoEngine()

class User(db.Document):
    _id = db.StringField()
    email = db.StringField()
    name = db.StringField()
    address = db.StringField()
    image = db.StringField()
    _password = db.StringField()
    created_at = db.StringField()
    updated_at = db.StringField()
    #convert this document to JSON
    def to_json(self):
        return {
            "_id":self._id,
            "email":self.email,
            "name": self.name,
            "address": self.address,
            "image": self.image,
            "created_at": self.created_at,
            "updated_at": self.updated_at

        }