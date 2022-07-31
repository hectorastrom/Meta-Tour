import cv2 as cv
import os
import time
import json
import numpy as np
from matplotlib import pyplot as plt


def main():
    start_time = time.time()
    if (check_folder("Images") and check_folder("Stitches")):
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

def convert_milli_to_frames(milli: int, totalMilli: int, totalFrames : int):
    """Returns the frame in a video given a specific timestamp in milliseconds"""
    ratio = int(milli/totalMilli)
    return int(ratio*totalFrames)

def select_timestamps(rotations, distance: float, sensitivity: int):
    """Creates a list of all the desired timestamps for a given rotation distance between frames. Selects the frame closest to the next step. It will return a list of length: 360/distance timestamps"""
    if distance <= 0: 
        print("[ERROR]: Distance must be > 0")
        exit(1)
    timestamps = []
    totalMeasurements = len(rotations)
    startRotation = rotations[0][1]
    timestamps.append(rotations[0])
    length = int(360/distance)+1
    # Under ideal conditions, we would expect the user to rotate 360 degrees at a constant rate throughout the video
    # We can then assume ideal conditions to approximate the timestamp a rotation would be at, then adjust up or down accordingly until we have
    # the timestamp with the closest rotation to the desired rotation
    def diff(a, b):
        return abs(a-b)
    for i in range(1, length):
        # Get desired rotation (ideally this rotation would be a measurement and we would save it as an image)
        desRot = startRotation + distance * i
        # Loop back around if it goes over 360 degrees
        desRot = desRot if desRot <= 360 else desRot-360
        # Approximate where we would expect to find the desired rotation under ideal conditions
        index = int((distance * i / 360) * totalMeasurements) - 1
        rot = rotations[index][1]
        print(index)
        # See if moving up 1 in the array gets a closer measurement to our desired measurement
        while index < totalMeasurements-sensitivity-1 and diff(sum(rotations[index+1: index+sensitivity+1, 1])/sensitivity, desRot) < diff(rot, desRot):
            index += 1
            rot = rotations[index][1]
        # See if moving down 1 in the array gets a closer measurement to our desired measurement
        while index > sensitivity-1 and diff(sum(rotations[index-sensitivity:index, 1])/sensitivity, desRot) < diff(rot, desRot):
            index -= 1
            rot = rotations[index][1]
        print(index)
        print()
        # Now that we should have the closest measured rotation to desired, we can add it to timestamps
        timestamps.append(rotations[index])

    return timestamps

    # 0 1 2 3 4 5 6 

def load_video_frames(vidcap, frameList: list):
    """Returns a list of all the frames of a video rotates 180 degrees from a list of integers specifying the desired frames"""
    frames = []
    # Read in image and success status
    success,image = vidcap.read()
    count = 0
    # Rotate image 180 and add to frames list
    frames.append(cv.rotate(image, cv.ROTATE_180))
    cv.imshow("Frame 1", frames[0])
    cv.waitKey(0)
    # while success: 


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
        print(f"[INFO]: {folderName} not found, automatically created new folder")
        os.mkdir(folderPath)
        return False
    return True

# Prints rounded values for each value in each row of the json file
tourData = load_json("tour_data.json")
vidcap = cv.VideoCapture("videospin.webm")
totalFrames = vidcap.get(7)
# Creates a list of tuples with all timestamps and y absolute rotations (relevant rotation). 
# Once this is in radians instead of degrees, multiply row[9] by np.pi/180
rotations = np.array([(row[0], row[9]) for row in tourData[::]])
# plt.scatter(rotations[:,0], rotations[:,1])
# plt.show(block=True)

# print("Rotations:")
# print([round(rot[1],3) for rot in rotations[::]])
print()
# Want an image every 12 or so degrees
print(select_timestamps(rotations, 12, 20))
# load_video_frames(vidcap, [1])
