# Overview
imageStitch.py is the script that uses gyroscope and video data to extract frames and build a panorama of a room. 

# Usage
The script is run in the format of `python imageStitch.py 'datafile.json' 'videofile.webm' 'scaleCoefficient' 'degrees'`. Each file should be found in the same directory as imageStitch.py.
- The **datafile** is a JSON file. The user must write .json after the file name.
- The **videofile** is built for a .webm file, though with a little code modification it could work for any video format. 
- The **scaleCoeffiecient** tells the program what scale to render the images at. It is a float value between 0-1, with 1 being original scale and 0 being nothing. Default value = 1.0
- The **degrees** is the float number of degrees between the different image captures from the video. For example, a degree value of 10.0, the program would take a frame approximately every 10.0 degrees from the video, so frame at degree 0, 10.0, 20.0, etc. Lower degree values lead to longer render times but more accurate stitches. Default value = 12.0

Once the stitch is created, it is stored in a **Stitches** folder which is automatically created when the program is first run. 