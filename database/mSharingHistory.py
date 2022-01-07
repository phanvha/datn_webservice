from flask_mongoengine import MongoEngine

db = MongoEngine()

class SharingHistory(db.Document):
    _id = db.StringField()
    userId = db.StringField()
    contentNote = db.StringField()
    potholeSharingId = db.StringField()
    modified = db.StringField()
    created = db.StringField()
    #convert this document to JSON
    def to_json(self):
        return {
            "_id":self._id,
            "userId":self.userId,
            "contentNote": self.contentNote,
            "potholeSharingId": self.potholeSharingId,
            "modified": self.modified,
            "created": self.created

        }
