from flask_mongoengine import MongoEngine

db = MongoEngine()

class Pothole(db.Document):
    _id = db.StringField()
    email = db.StringField()
    latitude = db.FloatField()
    longitude = db.FloatField()
    address = db.StringField()
    note = db.StringField()
    image_url = db.StringField()
    timestamp = db.StringField()

    #convert this document to JSON
    def to_json(self):
        return {
            "_id"       :self._id,
            "email"     :self.email,
            "latitude"  : self.latitude,
            "longitude" : self.longitude,
            "address"   : self.address, 
            "note"      : self.note,
            "image_url" : self.image_url,
            "timestamp" : self.timestamp
        }