from flask_mongoengine import MongoEngine

db = MongoEngine()

class SignalHistory(db.Document):
    _id = db.StringField()
    userId_own = db.StringField()
    userId_assign = db.StringField()
    content = db.StringField()
    note = db.StringField()
    latitude = db.FloatField()
    longitude = db.FloatField()
    status = db.StringField()
    created = db.StringField()
    modified = db.StringField()
    #convert this document to JSON
    def to_json(self):
        return {
            "_id":self._id,
            "userId_own":self.userId_own,
            "userId_assign": self.userId_assign,
            "content": self.content,
            "note": self.note,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "status": self.status,
            "created": self.created,
            "modified": self.modified

        }