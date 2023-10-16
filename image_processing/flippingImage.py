import cv2
import glob
import json
import os
import multiprocessing
import flipingFn
import random
#여기 경로 수정하기
PaddingName = "TomatoDatas"
crop_path = os.path.abspath(f"D:/PaddingDatas/{PaddingName}/padding_flip")
origin_path = os.path.abspath(f"D:/PaddingDatas/{PaddingName}/padding")
def getImg_path(path,image_name,flip_code):
    return path+"\\imgs_dir\\"+image_name.split(".")[0]+f"_flipping{flip_code}.jpg"

def rotatingSize(image_name,ssize,flip_code):
    json_origin_path = origin_path + f"\\ann_dir\\{image_name}.jpg.json"
    with open(json_origin_path,'r',encoding='utf-8') as file:
        data = json.load(file)
        points = data["annotations"]["points"][0]
        image_file_name = data["description"]["image"]
        diseaseCode = data["annotations"]["disease"]
        print(diseaseCode)
    xtl,ytl,xbr,ybr = points.values()
    img_path = origin_path+"\\imgs_dir\\"+image_file_name
    if not os.path.isfile(img_path):
        return
    origin = cv2.imread(img_path)

    img,bbox = flipingFn.flip_image(origin,flip_code,[xtl,ytl,xbr,ybr])


    #이미지 저장
    cv2.imwrite(crop_path+f"\\imgs_dir\\{image_name}_flipping{flip_code}.jpg",img)
    #라벨링 데이터 bounding_box와 크기와 너비를 모두 주어진 크기로 조정한다.
    data["annotations"]["points"][0] = {
                "xtl": bbox[0],
                "ytl": bbox[1],
                "xbr": bbox[2],
                "ybr": bbox[3]
    }
    data["description"]["height"] = ssize
    data["description"]["width"] = ssize
    data["description"]["image"] = image_name +f"_flipping{flip_code}.jpg"
    export_json_file_path = crop_path+f"\\ann_dir\\{image_name}_flipping{flip_code}.jpg.json"
    with open(export_json_file_path,'w+',encoding="utf-8") as f:
        json.dump(data,f)
    return

def get_image_paths():
    file_pattern = '*.json'
    return [raw_path.split("\\")[-1].split(".")[0] for raw_path in glob.glob(os.path.join(origin_path+"\\ann_dir", file_pattern))]

def count(data):
    # Test Code 10개 까지만 돌림
    #print("isRunning")
    rotatingSize(data[0],640,data[1])

if __name__ == '__main__':
    tasks = []
    pool = multiprocessing.Pool(processes=8)
    paths = get_image_paths()
    print(len(paths))
    
    num_list = [f"{v}: thread"for v in range(0,8)]
    for i in range(0,3):
        pool.map(count,[[v,i]for v in random.sample(paths,10000)])
    print("isFinished!!")
    pool.close()
    pool.join()
    

