import cv2
import glob
import json
import os
import multiprocessing
import paddingFn
#여기 경로 수정하기
PaddingName = "PepperDatas"
crop_path = os.path.abspath(f"D:/PaddingDatas/{PaddingName}/padding")
origin_path = os.path.abspath(f"D:/PaddingDatas/{PaddingName}/origin")
def getImg_path(path,image_name):
    return path+"\\imgs_dir\\"+image_name.split(".")[0]+"_padding.jpg"

def paddingSize(origin_json_file_path,export_json_file_path,ssize):
    with open(origin_json_file_path,'r',encoding='utf-8') as file:
        data = json.load(file)
        points = data["annotations"]["points"][0]
        image_file_name = data["description"]["image"]
        diseaseCode = data["annotations"]["disease"]
    xtl,ytl,xbr,ybr = points.values()
    origin = cv2.imread(origin_path+"\\imgs_dir\\"+image_file_name)
    img = paddingFn.padding(origin,ssize)
    h,w,c = origin.shape
    cv2.imwrite(getImg_path(crop_path,image_file_name),img)
    #라벨링 데이터 bounding_box와 크기와 너비를 모두 주어진 크기로 조정한다.
    maxLen = max(h,w)
    if h<w:
        ytl += (w-h)/2
        ybr += (w-h)/2
    else:
        xtl += (h-w)/2
        xbr += (h-w)/2
    xtl,ytl,xbr,ybr = [int(v*ssize/maxLen) for v in [xtl,ytl,xbr,ybr]]
    data["annotations"]["points"][0] = {
                "xtl": xtl,
                "ytl": ytl,
                "xbr": xbr,
                "ybr": ybr
    }
    data["description"]["height"] = ssize
    data["description"]["width"] = ssize
    data["description"]["image"] = image_file_name.split(".")[0]+"_padding.jpg"
    print("Padding Complete")
    with open(export_json_file_path,'w+',encoding="utf-8") as f:
        json.dump(data,f)
    return

def get_origin_json_paths(origin_dir,export_dir):
    def paddingName(origin_path):
        rawImg = origin_path.split("\\")[-1]
        return rawImg.split(".")[0]+"_padding.jpg.json"
    now_path = os.path.abspath(f"D:/PaddingDatas/{PaddingName}")
    file_pattern = '*.json'
    origin_paths = glob.glob(os.path.join(now_path+"\\"+origin_dir+"\\"+"ann_dir", file_pattern))
    
    return [(origin_path,now_path+'\\'+export_dir+'\\ann_dir\\'+paddingName(origin_path))
            for origin_path in origin_paths
            ]

def count(path):
    # Test Code 10개 까지만 돌림
        #print(name)
        paddingSize(path[0],path[1],640)

if __name__ == '__main__':
    tasks = []
    pool = multiprocessing.Pool(processes=8)
    path_list = get_origin_json_paths("origin","padding")
    #for (origin_json_path,export_json_path) in 
    num_list = [f"{v}: thread"for v in range(0,8)]
    pool.map(count,path_list)
    #for (origin_json_path,export_json_path) in get_origin_json_paths("origin","crop"):
    #    thread = Process(target = cropSize,args=(origin_json_path,export_json_path,640))
    #    tasks.append(thread)
    #    thread.start()

    #for task in tasks:
    #    task.join()
    pool.close()
    pool.join()

