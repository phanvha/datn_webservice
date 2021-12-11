from flask_mongoengine import MongoEngine

db = MongoEngine()

class News(db.Document):
    _id = db.StringField()
    title = db.StringField()
    urlPage = db.StringField()
    imageUrl = db.StringField()
    created_at = db.StringField()
    updated_at = db.StringField()
    #convert this document to JSON
    def to_json(self):
        return {
            "_id":self._id,
            "title":self.title,
            "url": self.urlPage,
            "image": self.imageUrl,
            "created_at": self.created_at,
            "updated_at": self.updated_at

        }