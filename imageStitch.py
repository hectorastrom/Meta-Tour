import cv2 as cv
import os
import time
import json
import numpy as np
from matplotlib import pyplot as plt

# Suppresses scientific notation
np.set_printoptions(suppress=True)

def main():

    imageFolder = 'Images'
    folders = os.listdir(imageFolder)

    # Goes through all folders in images folder (rooms) and takes images
    for room in folders[4:]:
        path = imageFolder + "/" + room
        images = []
        myList = os.listdir(path)
        # Reads images from folder and adds them to images list, resizing them
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


def convert_milli_to_frames(milli : int, totalMilli: int, totalFrames : int):
    """Returns the frame in a video given a specific timestamp in milliseconds"""
    ratio = milli/totalMilli
    return np.floor(ratio*totalFrames)


def select_timestamps(rotations, distance: float):
    """Creates a list of all the desired timestamps for a given rotation distance between frames. Selects the frame closest to the next step. It will return a list of length: 360/distance full of timestamps in milliseconds."""
    if distance <= 0: 
        print("[ERROR]: Distance must be > 0")
        exit(1)
    # Timestamps stores our relevant timestamps
    timestamps = []
    # Need to store where we start
    startRotation = rotations[0][0]
    timestamps.append(rotations[0][1])
    # We want a point every distance degrees, so 360/distance points + 1 for the start
    length = 360//distance+1
    for i in range(1, length):
        # Finding our desired rotation
        desRot = startRotation + i*distance
        # Gets the index of where desired rotation would fit in our array, checks to make sure we don't go out of bounds
        index = max(np.searchsorted(rotations[:,0], desRot) -1, 0)
        timestamps.append(rotations[index][1])
    return timestamps


def load_video_frames(vidcap, frameList: list, resizeCoeff: float, flip: bool):
    """Returns a list of all the frames of a video rotates 180 degrees from a list of integers specifying the desired frames"""
    frames = []
    # Read in image and success status
    for frame in frameList:
        vidcap.set(1, frame)
        success,image = vidcap.read()
        if success:
            image = cv.resize(image, (0,0), None, resizeCoeff, resizeCoeff)
            if flip:
                image = cv.rotate(image, cv.ROTATE_180)
            frames.append(image)
            # cv.imshow(f"{frame}", image)
            # cv.waitKey(2)

    return frames

def load_json(filename: str):
    """Returns a dictionary from a json file"""
    with open(filename, "r") as file:
        return json.load(file)


# Check if there is an images and stitches folder
def check_folder(folderName: str):
    """Checks if a folder exists and returns True if it does or creates the folder and returns False if it doesn't"""
    currentPath = os.getcwd()
    folderPath = os.path.join(currentPath, folderName)
    if not os.path.isdir(folderPath):
        print(f"[INFO]: '{folderName}' not found, automatically created new folder")
        os.mkdir(folderPath)
        exit(1)
        return False
    return True

if (check_folder("Data") and check_folder("Stitches")):
    print("[INFO]: All necessary folders exist")

# folders = os.listdir("Data")


# Prints rounded values for each value in each row of the JSON file
def videoToPanorama(dataName, videoName):
    tourData = load_json(dataName)
    vidcap = cv.VideoCapture(videoName)
    totalFrames = vidcap.get(7)
    # Creates a list of tuples with all timestamps and y absolute rotations (relevant rotation). 
    rotations = np.array([(row[9]*180/np.pi, row[0]) for row in tourData[::]])
    totalMilli = rotations[-1][1]

    # Sorts the array by orientation ascending (starts around 0, ends around 360)
    rotations = rotations[rotations[:, 0].argsort()]
    print("[INFO]: Rotations Sorted")

    # Printing scatter plot of index against rotation
    # plt.scatter(range(len(rotations)), rotations[:,0])
    # plt.show(block=True)

    # Want an image every 12 or so degrees
    timestamps = np.array(select_timestamps(rotations, 12))
    frames = convert_milli_to_frames(timestamps, totalMilli, totalFrames)
    images = load_video_frames(vidcap, frames, 1, True)
    print("[INFO]: Images gathered")
    print("[INFO]: Stiching images...")

    start_time = time.time()
    stitcher = cv.Stitcher_create()
    (status,result) = stitcher.stitch(images)
    if (status == 0):
        print(f"[SUCCESS]: Image Sphere Generated for {videoName}")
        cv.imwrite(f"Stitches/stitch-{videoName}.jpg", result)
        print(f"[INFO]: Time elapsed to stitch {videoName} was {round(time.time()-start_time, 3)} seconds.")
        cv.imshow(videoName,result)
        cv.waitKey(0)
        return result
    elif status == 1:
        print(f"[ERROR] Not enough keypoints in images of {videoName}")
        return 1
    else: 
        print(f"[ERROR]: {videoName} Status {status}")
        return 1
    

videoToPanorama("hectordata.json", "hectorvid.webm")


