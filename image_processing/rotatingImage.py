import cv2
import glob
import json
import os
import multiprocessing
import rotatingFn
#여기 경로 수정하기
PaddingName = "TomatoDatas"
crop_path = os.path.abspath(f"D:/PaddingDatas/{PaddingName}/padding_rotating")
origin_path = os.path.abspath(f"D:/PaddingDatas/{PaddingName}/padding")
def getImg_path(path,image_name):
    return path+"\\imgs_dir\\"+image_name.split(".")[0]+"_rotating.jpg"

def rotatingSize(image_name,ssize):
    json_origin_path = origin_path + f"\\ann_dir\\{image_name}.jpg.json"
    with open(json_origin_path,'r',encoding='utf-8') as file:
        data = json.load(file)
        points = data["annotations"]["points"][0]
        image_file_name = data["description"]["image"]
        diseaseCode = data["annotations"]["disease"]
        print(diseaseCode)
    xtl,ytl,xbr,ybr = points.values()
    origin = cv2.imread(origin_path+"\\imgs_dir\\"+image_file_name)
    img = rotatingFn.ratatingImg(origin,640,45)
    #이미지 저장
    cv2.imwrite(crop_path+f"\\imgs_dir\\{image_name}_rotating.jpg",img)
    #라벨링 데이터 bounding_box와 크기와 너비를 모두 주어진 크기로 조정한다.
    xtl,ytl,xbr,ybr = rotatingFn.rotatingBox([xtl,ytl,xbr,ybr],640,45)
    data["annotations"]["points"][0] = {
                "xtl": xtl,
                "ytl": ytl,
                "xbr": xbr,
                "ybr": ybr
    }
    data["description"]["height"] = ssize
    data["description"]["width"] = ssize
    data["description"]["image"] = image_name +"_rotating.jpg"
    export_json_file_path = crop_path+f"\\ann_dir\\{image_name}_rotating.jpg.json"
    with open(export_json_file_path,'w+',encoding="utf-8") as f:
        json.dump(data,f)
    return

def get_image_paths():
    file_pattern = '*.json'
    return [raw_path.split("\\")[-1].split(".")[0] for raw_path in glob.glob(os.path.join(origin_path+"\\ann_dir", file_pattern))]

def count(image_name):
    # Test Code 10개 까지만 돌림
    #print("isRunning")
    rotatingSize(image_name,640)

if __name__ == '__main__':
    tasks = []
    pool = multiprocessing.Pool(processes=8)
    paths = get_image_paths()
    print(paths)

    num_list = [f"{v}: thread"for v in range(0,8)]
    pool.map(count,paths)
    print("isFinished!!")
    pool.close()
    pool.join()

