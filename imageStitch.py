import cv2 as cv
import os
import time

start_time = time.time()

# Check if there is an images and stitches folder
def checkFolder(folderName: str):
    currentPath = os.getcwd()
    folderPath = os.path.join(currentPath, folderName)
    if not os.path.isdir(folderPath):
        print(f"[INFO]: {folderName} not found, automatically created new folder")
        os.mkdir(folderPath)
        return False
    return True

if (checkFolder("Images") and checkFolder("Stitches")):
    print("[INFO]: All necessary folders exist")

imageFolder = 'Images'
folders = os.listdir(imageFolder)

# Goes through all folders in images folder (rooms) and takes images
for room in folders[4:]:
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

    print(f"[INFO]: Time elapsed for {room} was {time.time()-start_time}")