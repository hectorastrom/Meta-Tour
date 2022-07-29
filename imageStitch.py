import cv2 as cv
import os


imageFolder = 'Images'
folders = os.listdir(imageFolder)
if not folders:
    print("[ERROR]: No Images Folder")
    exit(1)

# Goes through all folders in images folder (rooms) and takes images
for room in folders[:1]:
    path = imageFolder + "/" + room
    images = []
    myList = os.listdir(path)
    for imgName in myList:
        curImg = cv.imread(f'{path}/{imgName}')
        curImg = cv.resize(curImg, (0,0), None, .2, .2)
        images.append(curImg)
        cv.imshow(imgName, curImg)
        cv.waitKey(1)

    print("[INFO] Images Parsed")

    stitcher = cv.Stitcher_create()
    (status,result) = stitcher.stitch(images)
    if (status == 0):
        print("[SUCCESS]: Image Sphere Generated")
        cv.imshow(room,result)
        cv.waitKey(1)
    elif status == 1:
        print("[ERROR] Not enough keypoints in images")
    else: 
        print(f"[ERROR]: Status {status}")
        
cv.waitKey(0)