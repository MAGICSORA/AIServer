import os
import time
import json

from flask import Flask, request, jsonify
from PIL import Image
from yolov8_detect import Detector

app = Flask(__name__)

class AI_Server:
    def __init__(self, _type):
        with app.app_context():
            if _type == 0:
                self.detector = Detector("pepper_crop_padding.pt")
            elif _type == 1:
                self.detector = Detector("strawberry_crop_padding.pt")
            elif _type == 2:
                self.detector = Detector("lettuce_crop_padding.pt")
            elif _type == 3:
                self.detector = Detector("tomato_crop_padding.pt")

    def runner(self, json_file, img_file):
        with app.app_context():
            result = self.detector(json_file['cropType'], Image.open(img_file))
            result['cropImageId'] = json_file['cropImageId']
            print(result)
            return result

worker = []
for i in range(4):
    worker.append(AI_Server(i))

@app.route('/')
def hello():
    return '2023-1 Capstone MAGICSORA'

@app.route('/predict', methods = ['POST'])
def predict():
    try:
        json_file = json.loads(request.form.get('data'))
        img_file = request.files['file']
        return worker[json_file['cropType']].runner(json_file, img_file)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)


