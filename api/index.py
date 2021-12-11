from flask import Flask, make_response
from flask_cors import CORS,cross_origin
from flask_mongoengine import MongoEngine

app = Flask(__name__)
database_name = "API"
mongodb_password = "Hapunit137!@#"
DB_URL = "mongodb+srv://mongoapi:{}pythoncluster.djnve.mongodb.net/{}?retryWrites=true&w=majority".format(mongodb_password, database_name)
app.config["MONGODB_HOST"] = DB_URL


db = MongoEngine()
db.init_app(app)

class Pothole(db.Document):
    pothole_id = db.IntField()
    name = db.StringField()
    latitude = db.DoubleField()
    longitude = db.DoubleField()
    

    #convert this document to JSON
    def to_json(self):
        return {
            "pothole_id": self.pothole_id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

#POST /api/db_connect -> populates the db and return 201 success code
#GET /api/potholes -> return the details of all potholes with 200 code success
#POST /api/potholes -> create a new pothole and return 201 success code
#GET /api/potholes/3 -> return the detail of pothole 3
#PUT /api/potholes/3 -> update to pothole 3
#DELETE /api/pothole/3 -> delete pothole 3

@app.response_class('/api/db_connect', methods=['POST'])
def db_connect():
    pothole1 = Pothole(
        pothole_id=1, 
        name="ddm", 
        latitude=15.2214235,
        longitude=108.12532525
        )
    pothole2 = Pothole(
        pothole_id=2, 
        name="mmm", 
        latitude=15.2223533,
        longitude=108.25267475
        )

    pothole1.save()
    pothole2.save()

    return make_response('code', 201)
    


@app.response_class('/api/potholes', methods=['GET','POST'])
def api_potholes():
    pass

@app.response_class('/api/potholes/<pothole_id>', methods=['GET','PUT','DELETE'])
def api_each_potholes():
    pass




if __name__ == '__main__':
    app.run()


