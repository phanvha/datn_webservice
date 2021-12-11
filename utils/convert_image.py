import cv2 as cv
import numpy as np
import base64
import string, random
import os

def reUpImage(path):
    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    new_arr = cv.resize(img, (60, 60))
    new_arr = np.array(new_arr)
    new_arr = new_arr.reshape(-1, 60, 60, 1)
    return new_arr

def base64_to_image(img_base64):
    try:
        anh_base64 = np.fromstring(base64.b64decode(img_base64), dtype=np.uint8)
        anh_base64 = cv.cvtColor(anh_base64, cv.COLOR_RGB2GRAY)
        anh_base64 = cv.resize(anh_base64, (60, 60))
        anh_base64 = np.array(anh_base64)
        anh_base64 = anh_base64.reshape(-1, 60, 60, 1)
    except:
        return None
    return anh_base64

def image_to_base64(image):
    try:
        image_file = image
        encoded_string = base64.b64encode(image_file.read())
        print(encoded_string)

    except:
        return None
    return encoded_string

def getType(mimeType):
    type = ""
    if mimeType == "image/jpeg":
        type = "JPEG"
        return type
    elif mimeType == "image/jpg":
        type = "JPG"
        return type
    elif mimeType == "image/png": 
        type = "PNG"
        return type
    else:
        return  type
def getSize(img):
    # img.seek(0, os.SEEK_END)
    # image_size = img.tell()
    image_size = img.file.size
    print(str(image_size))
    result = 0
    mess = ""
    s = 2097152 # 2 MB
    if image_size >= s:
        mess = "The size of the file is too large! Limited to 2048"
        print(mess)
        return False

    else:
        print(mess)
        return True
    
    
        
    
    