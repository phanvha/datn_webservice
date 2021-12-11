from flask_mongoengine import MongoEngine


db = MongoEngine()

class Tracking(db.Document):
    _id = db.StringField()
    latitude = db.FloatField()
    longitude = db.FloatField()
    timestamp = db.StringField()

    #convert this document to JSON
    def to_json(self):
        return {
            "_id": self._id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp
        }