from flask import Flask,render_template,url_for,redirect,request
from werkzeug.utils import secure_filename
import cv2 as cv
import numpy as np
import os
UPLOAD_FOLDER = '/Users/yvette_wu/Desktop/od-web/tmp'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def contours_demo(image,filename):
    dst = cv.GaussianBlur(image, (5, 5), 0) #高斯模糊去噪
    gray = cv.cvtColor(dst, cv.COLOR_RGB2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU) #用大律法、全局自適應閾值方法進行圖像二值化
    contours, heriachy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    data=[]
    for i, contour in enumerate(contours):
        M = cv.moments(contour)
        cv.drawContours(image, contours, i, (0, 0, 255), 2)
        area = cv.contourArea(contour)
        if area > 100 and area < 10000:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv.circle(image, (cx,cy), 1, (0, 255, 0), 4)
            perimeter = cv.arcLength(contour,True)
            data.append([i,area,perimeter/3.14159,cx,cy])
    cv.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], "L_"+filename), image)
    return data
    #cv.imshow("contours", image)
@app.route('/')
def index():
    return 'Hello! This website is for edge detection'
@app.route('/detect',methods=['POST','GET'])
def detect():
    if request.method =='POST':
        file =request.files['file']
        filename = secure_filename(file.filename) 
        if filename.split('.')[1] in ALLOWED_EXTENSIONS:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = cv.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            objectinfo=contours_demo(img,filename)
            return str(objectinfo)
        return 'Not Image File'
    return 'Not Post Method'
@app.route('/upload')
def upload():
    return render_template('upload.html')
if __name__ == '__main__':
    app.run(debug=True,port='5001')