import cv2 as cv
import os


imageFolder = 'Images'
folders = os.listdir(imageFolder)
if not folders:
    print("[ERROR]: No Images Folder")
    exit(1)

# Goes through all folders in images folder (rooms) and takes images
for room in folders[2:3]:
    path = imageFolder + "/" + room
    images = []
    myList = os.listdir(path)
    for imgName in myList:
        curImg = cv.imread(f'{path}/{imgName}')
        curImg = cv.resize(curImg, (0,0), None, .5, .5)
        images.append(curImg)
        # cv.imshow(imgName, curImg)

    print("[INFO] Images Parsed")

    stitcher = cv.Stitcher_create()
    (status,result) = stitcher.stitch(images)
    if (status == 0):
        print(f"[SUCCESS]: Image Sphere Generated for {room}")
        cv.imwrite(f"Stitches/stitch-{room}.jpg", result)
        cv.imshow(room,result)
        cv.waitKey(0)
    elif status == 1:
        print(f"[ERROR] Not enough keypoints in images of {room}")
    else: 
        print(f"[ERROR]: {room} Status {status}")