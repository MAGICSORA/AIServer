import cv2
import numpy as np
import math
def example():
# 이미지를 로드합니다.
    image = cv2.imread('C:\\Users\\Public\\MagicSora\\RealData\\TomatoCrops\\images\\V006_77_0_00_11_01_13_0_c01_20201013_0000_S01_padding.jpg')
    
    # 이미지의 높이, 너비를 가져옵니다.
    height, width = image.shape[:2]
    
    # 이미지 중심을 기준으로 45도 회전할 회전 행렬을 생성합니다.
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), 45, 1)
    
    # 이미지를 회전합니다.
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    #[x1,y1,x2,y2] = [int(v*640) for v in [0.5140625,0.5453125,0.10625,0.090625]]
    x1,y1,x2,y2 = 273,149,343,187
    
    bbox = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
    midx,midy = (x2+x1)/2,(y2+y1)/2
    rad = math.sqrt(abs(x1-midx)**2 + abs(y1-midy)**2)
    # 바운딩 박스를 회전합니다.
    rotated_bbox = cv2.transform(np.array([[[midx, midy]]]), rotation_matrix)
    transformed_midx, transformed_midy = rotated_bbox[0][0]
    x1_rot,x2_rot = transformed_midx-rad,transformed_midx+rad
    y1_rot,y2_rot = transformed_midy-rad,transformed_midy+rad
    # 회전된 이미지와 바운딩 박스를 그립니다.
    cv2.rectangle(rotated_image, (int(x1_rot), int(y1_rot)), 
                  (int(x2_rot), int(y2_rot)), (0, 255, 0), 2)
    
    cv2.rectangle(image,(int(x1), int(y1)), (int(x2), int(y2)),(255,0,0),2)
    
    
    # 결과 이미지를 출력합니다.
    cv2.imshow("Image",image)
    cv2.imshow('Rotated Image', rotated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def ratatingImg(img,set_size,angle):
    # 이미지의 높이, 너비를 가져옵니다.
    height, width = img.shape[:2]

# 이미지 중심을 기준으로 45도 회전할 회전 행렬을 생성합니다.
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)

# 이미지를 회전합니다.
    rotated_image = cv2.warpAffine(img, rotation_matrix, (width, height))
    img = cv2.resize(rotated_image, (set_size, set_size))
    return img



def rotatingBox(raw_box,set_size,angle):
    x1,y1,x2,y2 = raw_box
    midx,midy = (x2+x1)/2,(y2+y1)/2
    rad = math.sqrt(abs(x1-midx)**2 + abs(y1-midy)**2)

    
    rotation_matrix = cv2.getRotationMatrix2D((set_size / 2, set_size / 2), angle, 1)
    # 바운딩 박스를 회전합니다.
    rotated_bbox = cv2.transform(np.array([[[midx, midy]]]), rotation_matrix)
    transformed_midx, transformed_midy = rotated_bbox[0][0]
    x1_rot,x2_rot = transformed_midx-rad,transformed_midx+rad
    y1_rot,y2_rot = transformed_midy-rad,transformed_midy+rad
    # 회전된 이미지와 바운딩 박스를 그립니다.
    return (int(x1_rot),int(x2_rot),int(y1_rot),int(y2_rot))