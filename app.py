# from tensorflow.keras.preprocessing import image
from database.mNews import News
from database.mUser import User
from flask import Flask, make_response, jsonify, render_template
from flask_cors import CORS, cross_origin
from flask import request, Response
from flask_mongoengine import MongoEngine
from tensorflow.keras import backend
# from tensorflow.keras.model import load_model
# from tensorflow.keras.preprocessing.image import load_img, img_to_array 

# from flask_ngrok import run_with_ngrok
import pandas as pd
import numpy as np
import cv2 as cv
import base64
import string, random
import tensorflow as tf
import os
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from config import URL
from werkzeug.utils import redirect, secure_filename  
from datetime import datetime
from database.mPothole import Pothole
from database.mTracking import Tracking
from utils.convert_image import reUpImage, base64_to_image, image_to_base64, getType, getSize

import firebase_admin
from firebase_admin import credentials, messaging

# cred = credentials.Certificate("data/json/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
# def sendPush(title, msg, registration_token, dataObject=None):
#     # See documentation on defining a message payload.
#     message = messaging.MulticastMessage(
#         notification=messaging.Notification(
#             title=title,
#             body=msg
#         ),
#         data=dataObject,
#         tokens=registration_token,
#     )

#     # Send a message to the device corresponding to the provided
#     # registration token.
#     response = messaging.send_multicast(message)
#     # Response is a message ID string.
#     print('Successfully sent message:', response)


# physical_device = tf.config.experimental.list_physical_devices('GPU')
# if len(physical_device) > 0:
#     tf.config.experimental.set_memory_growth(physical_device[0], True)

app = Flask(__name__)
# run_with_ngrok(app)

URL = "mongodb+srv://haphan:hapunit137@poro.eysuj.mongodb.net/API?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = URL
# app.config['MONGODB_SETTINGS'] = {
#     'db': 'porodb',
#     'host': 'localhost',
#     'port': 27017
# }
app.config['MAX_CONTENT_LENGTH'] = 5*1024*1024 #3171943

db = MongoEngine()
db.init_app(app)

# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CATEGORIES = [0, 1]
ALLOWED_EXTENSIONS = set(['png','jpg', 'jpeg', 'gif'])


def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choices(chars) for _ in range(size))

#nhận dạng ổ gà
def detectPothole(img):
    #load model
    model = tf.keras.models.load_model('model/detectpt.model')
    prediction = model.predict([img])
    print(CATEGORIES[prediction.argmax()])
    return CATEGORIES[prediction.argmax()]

@app.route('/')
def home():
    return redirect('index')


@app.route('/dashboard', methods=['GET'] )
def index():
    try:
        tracking  = Tracking.objects
        pot = Pothole.objects
        return render_template('index.html', data_pot = pot, data_tr = tracking, count_pt = pot.count(), count_tr = tracking.count())
    except Exception as e:
        return make_response({'error' : str(e)})

@app.route('/mapsview', methods=['GET', 'POST'])
def mapsview():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect('index')

    # show the form, it wasn't submitted
    return render_template('maps.html')

@app.before_first_request
def load_model_to_app():
    app.predictor = tf.keras.models.load_model('model/detectpt.model')

#api nhận dạng ổ gà
@app.route('/api/pothole/detect', methods=['POST'] )
@cross_origin(origin='*')
def pothole_detect_process():
    f = request.files['image']

    save_father_path = 'images'
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))    
    filename = str(ran)+'.'+f.filename
    img_path = os.path.join(save_father_path, filename)
    if not os.path.exists(save_father_path):
        os.makedirs(save_father_path)
    f.save(img_path)
    result = detectPothole(reUpImage(img_path))
    # result = [im.height, im.width]
    # print(result)
    return make_response(jsonify({
                'status': False,
                'code' : 200,
                'status_code' : "PR-00000000",
                'message': 'Hình ảnh đã được xác thực thành công!',
                'object': [
                    {
                        'data': result,
                    }
                    ]
                }))
  

#chuyển base64 sang ảnh
def chuyen_base64_sang_anh(anh_base64):
    try:
        anh_base64 = np.fromstring(base64.b64decode(anh_base64), dtype=np.uint8)
        anh_base64 = cv.imdecode(anh_base64, cv.IMREAD_ANYCOLOR)
    except:
        return None
    return anh_base64
def dem_so_mat(face):
    # Khởi tạo bộ phát hiện khuôn mặt
    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Chuyen gray
    gray = cv.cvtColor(face, cv.COLOR_BGR2GRAY)
    # Phát hiện khuôn mặt trong ảnh
    faces = face_cascade.detectMultiScale(gray, 1.2, 10)

    so_mat = len(faces)
    return so_mat
#api nhận dạng khuôn mặt
@app.route('/nhandienkhuonmat', methods=['POST'] )
@cross_origin(origin='*')
def face_detect_process():
    face_numbers = 0
    # Đọc ảnh từ client gửi lên
    facebase64 = request.form.get('facebase64')
    # Chuyển base 64 về OpenCV Format
    face = chuyen_base64_sang_anh(facebase64)
    # Đếm số mặt trong ảnh
    face_numbers = dem_so_mat(face)

    # Trả về
    return "Số mặt là = " + str(face_numbers)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#create new pothole
@app.route('/api/create-pothole', methods=['POST'] )
@cross_origin(origin='*')
def create_pothole():
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 17)) 
    _id = str(ran)
    email = request.form.get('email')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    note = request.form.get('note')
    addres = request.form.get('address')
    img = request.files['image']
    timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if not img.filename:
        print("No image")
        img = ""
        return make_response(jsonify({
                'status': False,
                'code' : 401,
                'status_code' : "",
                'message': 'Hình ảnh không được để trống!',
                }))
    else:
        date = datetime.now()
        date = date.strftime("%d-%m-%y")
        save_father_path = 'static\data\images'
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))    
        mimeType = img.content_type
        mimeType = getType(mimeType)
        filename = str(mimeType)+'_'+str(date)+"_"+str(ran)+'_'+img.filename
        img_path = os.path.join(save_father_path, filename)
        # if getSize(img):
        #     print("bbc")
        # else:
        #     print("xxx")
        if not os.path.exists(save_father_path):
            os.makedirs(save_father_path)
        img.save(img_path)
        result = detectPothole(reUpImage(img_path))
        
        if result == 1:
            pothole1 = Pothole(
                _id             = _id,
                email           = email,
                latitude        = latitude,
                longitude       = longitude,
                address         = addres,
                note            = note,
                image_url       = filename,
                timestamp       = timestamp
                )
            pothole1.save()

            response = {
                '_id'       : pothole1._id,
                'email'     : pothole1.email,
                'latitude'  : pothole1.latitude,
                'longitude' : pothole1.longitude,
                'address'   : pothole1.address,
                'note'      : pothole1.note,
                'image'     : pothole1.image_url,
                'timestamp' : pothole1.timestamp
            }
            return make_response(jsonify({
                'status': True,
                'code' : 200,
                'message': 'Tạo dữ liệu thành công!',
                'object' : response
                
            }),200)
        else:
            return make_response(jsonify({
                'status': False,
                'code' : 401,
                'status_code': 'PR-00000001',
                'message': 'Error',
                'data' : []
                }), 401)

    # return make_response(Pothole.objects.first())

@app.route('/api/v1/potholes', methods=['GET', 'POST'] )
@cross_origin(origin='*')
def _api():
    try:
        if request.method == 'GET':
            potholes = []
            for poth in Pothole.objects:
                potholes.append(poth)
            return make_response(jsonify(
                {
                    'status': True,
                    'code': 200,
                    'status_code': "PR-00000000",
                    'message': "Lấy dữ liệu thành công!",
                    'object' : potholes
                }),200)
        elif request.method == 'POST':
            content = request.json
            pot = Pothole(
                latitude=content['latitude'], 
                longitude=content['longitude'], 
                note=content['note'])
            pot.save()
            return make_response(jsonify(
                {
                    'status': True,
                    'code': 201,
                    'status_code': "PR-00000000",
                    'message': "Upload dữ liệu thành công",
                    'object' : pot
                    
                }),201)
    except print(0):
        return make_response(jsonify(
                {
                    'status': True,
                    'code': 200,
                    'status_code': "PR-00000004",
                    'message': "Không thể lấy dữ liệu!",
                }),401)


   

@app.route('/api/potholes/<_id>', methods=['GET','POST','DELETE'])
@cross_origin(origin='*')
def api_each_potholes(_id):
    if request.method == 'GET':
        pothole_obj = Pothole.objects(_id=id).first()
        if pothole_obj:
            return make_response(jsonify(pothole_obj.to_json()), 200)
        else:
            return make_response("Error", 404)

    elif request.method == 'POST':
        content = request.json
        pothole_ob = Pothole.objects(_id=_id).first()
        #pothole_ob.reload()
        pothole_ob.latitude    = content['latitude']
        pothole_ob.longitude   = content['longitude']
        pothole_ob.note        = content['note']
        pothole_ob.save()
        #return make_response("ok", 204)
        return make_response(jsonify(pothole_ob.to_json()), 200)

    elif request.method == 'DELETE':
        obj = Pothole.objects(_id=_id).first()
        obj.delete()

        return make_response("ok", 200)
    
@app.route('/api/potholes/<_id>/delete', methods=['POST'])
@cross_origin(origin='*')
def api_delete(_id):
    obj = Pothole.objects(_id=_id).first()
    obj.delete()

    return make_response("Deleted", 200)


# tracking user location
@app.route('/api/pothole/tracking', methods=['POST'])
@cross_origin(origin='*')
def tracking():
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 17)) 
    _id = str(ran)
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    pot = Tracking(
        _id         = _id,
        latitude    = latitude, 
        longitude   = longitude,
        timestamp   = timestamp
        )
    pot.save()
    return make_response(jsonify(
        {
            'status': True,
            'code': 200,
            'message': "OK",
            'data': [pot]
        }
        ), 201)
# news
@app.route('/api/news/add', methods=['POST'])
@cross_origin(origin='*')
def add_news():
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 17)) 
    _id = str(ran)
    title = request.form.get('title')
    urlPage = request.form.get('urlPage')
    imgURL = request.form.get('imageUrl')
    timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(title)
    pot = News(
        _id         = _id,
        title       = title, 
        urlPage     = urlPage,
        imageUrl       = imgURL,
        created_at   = timestamp
        )
    pot.save()
    return make_response(jsonify(
        {
            'status': True,
            'code': 200,
            'message': "OK",
            'data': [pot]
        }
        ), 201)

@app.route('/api/news/get', methods=['GET', 'POST'] )
@cross_origin(origin='*')
def get_news():
    if request.method == 'GET':
        news = []
        for pot in News.objects:
            news.append(pot)
        
        return make_response(jsonify(news),200)



@app.route('/api/user/add', methods=['POST'])
@cross_origin(origin='*')
def create_user():
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 17)) 
    _id = str(ran)
    name = request.form.get('name')
    email = request.form.get('email')
    address = request.form.get('address')
    password = request.form.get('password')
    img = request.files['image']
    timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    
    user = User.objects(email=email)
    if user:
        return make_response(jsonify({
                'status': False,
                'code' : 401,
                'message': 'User already exists!',
                'data' : []
                }))

    filename = ""
    
    if img.filename != '':
        date = datetime.now()
        date = date.strftime("%d-%m-%y")
        save_father_path = 'static\data\images'
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))    
        mimeType = img.content_type
        mimeType = getType(mimeType)
        print(str(mimeType))
        filename = str(mimeType)+'_'+str(date)+"_"+str(ran)+'_'+img.filename
        img_path = os.path.join(save_father_path, filename)
        if not os.path.exists(save_father_path):
            os.makedirs(save_father_path)
        img.save(img_path)
    
    _password = generate_password_hash(password)
    pot = User(
                _id         = _id,
                name        = name, 
                email       = email,
                address     = address,
                image       = filename,
                _password   = _password, 
                created_at  = timestamp,
                updated_at  = ""
            )
    pot.save()
    return make_response(jsonify(
        {
            'status': True,
            'code': 200,
            'message': "OK",
            'data': [pot]
        }
        ), 201)

@app.route('/api/user/login', methods=['POST'] )
@cross_origin(origin='*')
def user_login():
    
        
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.objects(email=email)
    #print(str(user[0]['_password']))
    
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if user is None or not user:
        return make_response(jsonify({
                'status': False,
                'code' : 401,
                'message': 'Login failed!',
                'data' : [
                    {
                        'error' : 'Account does not exist!',
                    }
                ]
                }))
    elif(not check_password_hash(user[0]['_password'], password)):
        return make_response(jsonify({
                'status': False,
                'code' : 401,
                'message': 'Login failed!',
                'data' : [
                    {
                        'error' : 'Password incorrect!',
                    }
                ]
                }))
    else:
        return make_response(jsonify(
        {
            'status': True,
            'code': 200,
            'message': "Login successfully!",
            'data': user
        }
        ), 201)
        
        

# Start Backend
if __name__ == '__main__':
    # app.run(host='localhost', port='4040')
    app.run(host='localhost', port='5050')
    # app.run()


