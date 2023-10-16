import cv2

def flip_image(image, flip_code, bbox):
    # 이미지 플립
    flipped_image = cv2.flip(image, flip_code)
    
        # 바운딩 박스 좌표 추출
    x1, y1, x2, y2 = bbox
    
    # 이미지의 너비와 높이
    height, width, _ = image.shape
    
    if flip_code == 0:  # 좌우 플립
        bbox_flipped = [x1, height - y2, x2, 640 - y1]
    elif flip_code == 1:  # 상하 플립
        bbox_flipped = [width - x2, y1, width - x1, y2]

    else:  # 상하 및 좌우 플립
        bbox_flipped = [width - x2, height - y2, width - x1, height - y1]
        
    print([x1,y1,x2,y2])
    return flipped_image, bbox_flipped

def example():
    bbox = [261,228,418,382]
    image = cv2.imread("D:\\PaddingDatas\\TomatoDatas\\padding\\imgs_dir\\V006_77_0_00_11_01_13_0_c01_20201013_0017_S01_1_padding.jpg")
    flipped_image,flipped_bbox = flip_image(image,0,bbox)

    cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
    cv2.imshow("Original Image", image)

    cv2.rectangle(flipped_image, (flipped_bbox[0], flipped_bbox[1]), (flipped_bbox[2], flipped_bbox[3]), (0, 255, 0), 2)
    cv2.imshow("Flipped Image", flipped_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()