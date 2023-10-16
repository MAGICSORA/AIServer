import cv2
from ultralytics import YOLO
import torch
import os

class Detector:
    def load_model(self,model_path):
        if model_path:
            try:
                model = YOLO(os.path.abspath(".")+"/"+model_path)
                return model
            except:
                print("Model Name is Wrong!!")
                return None
            
    def __init__(self, model_path):
        self.model = self.load_model(model_path)
        self.crop_type_match = {
            0: [0, 1, 2],
            1: [3, 4, 5],
            2: [6, 7, 8],
            3: [9, 10, 11]
        }
        self.empty_dict = {
            "responseCode": 1,
            "diagnoseReults": []
        }

    def getMyDiagnosis(self,crop_type, boxes):
        return list(filter(lambda box: True if int(box.cls) in self.crop_type_match[crop_type] and float(box.conf) > 0.5 else False, boxes))
    
    def getTop3Diagnosis(self,boxes):
        return list(map(lambda box:{
                "diseaseCode":int(box.cls),
                "accuracy":float(box.conf),
                "bbox":[float(v) for v in box.xyxyn[0].tolist()]
            },sorted(boxes,key=lambda x: float(x.conf), reverse = True)[:3])
        )
    def __call__(self,crop_type,img_path):
        result = self.model([img_path])[0]
        boxes = list(result.boxes)
        if not boxes: return self.empty_dict
        boxes = self.getMyDiagnosis(crop_type,boxes)
        if not boxes:
            return self.empty_dict
        return {
            "responseCode" : 0,
            "diagnoseResults": self.getTop3Diagnosis(boxes)
        }
