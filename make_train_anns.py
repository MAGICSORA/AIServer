import glob
import json
import os
from multiprocessing import Pool



def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def diseaseMatch(crop_type,disease_type):
    print(f"crop_type {crop_type} disease_type {disease_type}")
    crop_table = {2:0,4:3,5:6,11:9}
    disease_table = {
        3:1,4:2,
        7:4,8:5,
        9:7,10:8,
        18:10,19:11
    }
    if disease_type == 0:
        return crop_table[crop_type]
    else:
        if disease_type in disease_table:
            return disease_table[disease_type]
        else: -1
def makeTrainAnns(crops_json_path,train_ann_dir):
    for idx,crop_json_path in enumerate(crops_json_path):
        with open(crop_json_path,'r',encoding='utf-8') as file:
            data = json.load(file)
            img_name = data["description"]["image"]
            disease_type = data["annotations"]["disease"]
            crop_type = data["annotations"]["crop"]
            bbox = data["annotations"]["points"][0]
            height = data["description"]["height"]
            width = data["description"]["width"]
        xtl,ytl,xbr,ybr = bbox.values()
        x_center_norm = (xtl+xbr)/(2*width)
        y_center_norm = (ytl+ybr)/(2*height)
        x_width = abs(xtl-xbr) / width
        y_height = abs(ytl-ybr) / height
        img_name = img_name.replace(".jpg","")
        img_name = img_name.replace(".jpeg","")
        img_name = img_name.replace(".JPG","")
        img_name = img_name.replace(".JPEG","")
        with open(train_ann_dir+"/"+img_name+".txt","w+",encoding="utf-8") as f:
            f.write(f'{diseaseMatch(crop_type,disease_type)} {x_center_norm} {y_center_norm} {x_width} {y_height}\n')
        #print(idx)
    print("is Done")
    return

if __name__ == '__main__':
    crop_dirs = ["LettuceCrops","PepperCrops","StrawBerryCrops","TomatoCrops"]
    file_format = "*.json"
    p = Pool(len(crop_dirs))
    for crop_dir in crop_dirs:
        #crop_ann_dir = os.path.abspath(".")+f'/RealData/{crop_dir}/ann_dir'
        crops_json_path = glob.glob(os.path.join(crop_ann_dir, file_format))
        train_ann_dir = os.path.abspath(".")+f'/RealData/{crop_dir}/ann_train_dir'
        createFolder(train_ann_dir)
        p.apply_async(makeTrainAnns,(crops_json_path,train_ann_dir))
    p.close()
    p.join()
