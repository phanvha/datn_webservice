from flask_mongoengine import MongoEngine

db = MongoEngine()

class Notifications(db.Document):
    _id = db.StringField()
    title = db.StringField()
    content = db.StringField()
    status = db.StringField()
    type = db.StringField()
    modified = db.StringField()
    created = db.StringField()
    #convert this document to JSON
    def to_json(self):
        return {
            "_id":self._id,
            "title":self.title,
            "content": self.content,
            "status": self.status,
            "type": self.type,
            "modified": self.modified,
            "created": self.created

        }