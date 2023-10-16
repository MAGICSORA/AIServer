import cv2
import glob
import json
import os
import multiprocessing
#여기 경로 수정하기
CropName = "TomatoDatas"
crop_path = os.path.abspath(f"D:/CropDatas/{CropName}/crop")
origin_path = os.path.abspath(f"D:/CropDatas/{CropName}/origin")
def getImg_path(path,image_name):
    return path+"\\imgs_dir\\"+image_name

def cropSize(origin_json_file_path,export_json_file_path,ssize):
    with open(origin_json_file_path,'r',encoding='utf-8') as file:
        data = json.load(file)
        points = data["annotations"]["points"][0]
        image_file_name = data["description"]["image"]
    xtl,ytl,xbr,ybr = points.values()
    
    origin = cv2.imread(getImg_path(origin_path,image_file_name))
    h,w,c = origin.shape
    minNum = min(h,w)
    if minNum==h:
        mid = w/2
        crop_img = origin[0:h][int(mid-minNum/2):int(mid+minNum/2)]
        xtl,xbr = xtl - (w-minNum)/2, xbr - (w-minNum)/2 #bounding box 변경
    else:
        mid = h/2
        crop_img = origin[int(mid-minNum/2):int(mid+minNum/2)][0:w]
        ytl,ybr = ytl - (h-minNum)/2, ybr - (h-minNum)/2 #bounding box 변경
    resize_img = cv2.resize(crop_img,(ssize,ssize))
    cv2.imwrite(getImg_path(crop_path,image_file_name),resize_img)
    #라벨링 데이터 bounding_box와 크기와 너비를 모두 주어진 크기로 조정한다.
    data["annotations"]["points"][0] = {
                "xtl": xtl,
                "ytl": ytl,
                "xbr": xbr,
                "ybr": ybr
    }
    for (key,val) in data["annotations"]["points"][0].items():
        data["annotations"]["points"][0][key] = int(val/minNum*ssize)
    data["description"]["height"] = ssize
    data["description"]["width"] = ssize
    with open(export_json_file_path,'w+',encoding="utf-8") as f:
        json.dump(data,f)
    return

def get_origin_json_paths(origin_dir,export_dir):
    now_path = os.path.abspath(f"D:/CropDatas/{CropName}")
    file_pattern = '*.json'
    origin_paths = glob.glob(os.path.join(now_path+"\\"+origin_dir+"\\"+"ann_dir", file_pattern))
    return [(origin_path,now_path+'\\'+export_dir+'\\ann_dir\\'+origin_path.split("\\")[-1]) 
            for origin_path in origin_paths
            ]

def count(name):
    for (origin_json_path,export_json_path) in get_origin_json_paths("origin","crop"):
        print(name)
        cropSize(origin_json_path,export_json_path,640)

if __name__ == '__main__':
    tasks = []
    pool = multiprocessing.Pool(processes=8)
    num_list = [f"{v}: thread"for v in range(0,8)]
    pool.map(count,num_list)
    #for (origin_json_path,export_json_path) in get_origin_json_paths("origin","crop"):
    #    thread = Process(target = cropSize,args=(origin_json_path,export_json_path,640))
    #    tasks.append(thread)
    #    thread.start()

    #for task in tasks:
    #    task.join()
    pool.close()
    pool.join()