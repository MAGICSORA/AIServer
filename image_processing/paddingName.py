import os
import glob
import json
PaddingName = "TomatoDatas"
padding_path = os.path.abspath(f"D:/PaddingDatas/{PaddingName}/padding")


def jsonRename():
    ann_path = padding_path+"\\ann_dir"
    jsons = glob.glob(os.path.join(ann_path,"*.json"))
    for v in jsons:
        rawJson = v.split("\\")[-1]
        newName = rawJson.split(".")[0] + ".jpg.json"
        with open(v,'r',encoding='utf-8') as f:
            data = json.load(f)
        image_file_name = data["description"]["image"]
        rawName = image_file_name.split(".")[0]
        data["description"]["image"] = rawName.split("_padding")[0]+"_padding.jpg"
        #print(data)
        #print(v,ann_path+"\\"+newName)
        print(v)
        with open(v,'w+',encoding="utf-8") as f:
            json.dump(data,f)
        #os.rename(v,ann_path+"\\"+newName)
def imgRename():
    img_path = padding_path + "\\imgs_dir"
    imgs = []
    for v in ["*.jpg","*.JPG","*.JPEG","*.jpeg"]:
        imgs += glob.glob(os.path.join(img_path,v))
    for v in imgs:
        rawImg = v.split("\\")[-1]
        rawName = rawImg.split(".")[0]
        newName = rawName.split("_padding")[0]  + "_padding.jpg"
        print(img_path+"\\"+newName)
        if os.path.isfile(v):
            os.rename(v,img_path+"\\"+newName)
#imgRename()
jsonRename()