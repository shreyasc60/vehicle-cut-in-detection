# Documentation
A python based vehicle cut-in detection algorithm making the use of existing deep learning model YOLO
for object detection, and using the obtained data to detect cut-in(s) and generating collision alerts.

__Contributors__: [shreyasc60](https://github.com/shreyasc60), [Shantnu-Talokar](https://github.com/Shantnu-Talokar), [sachinbisen](https://github.com/sachinbisen), [kinshookk](https://github.com/kinshookk)

# Dependencies
To run this code you'll need to install the following dependencies or modules through the 
`py -m pip install -r requirements.txt` command (on Windows 10+).

- ***Dependencies***:    opencv-python, numpy, winsound
- Additionally you'll also need to [download](https://www.kaggle.com/datasets/valentynsichkar/yolo-coco-data?select=yolov3.weights) the ***'yolov3.weights'*** file, and place it in the root directory for the code to run successfully.
  The yolov3.cfg and coco.names are provided in the repo by default.

# How to use this? 
- Requirements: Windows 10 or above
1. Clone repo in your working directory
2. Install and download the dependencies
3. Configure the code to load your own image/video file in OpenCV

   > 15 `cap = cv2.VideoCapture("/path/to/your/file")  # Change to 0 for webcam`
   
   Change the path in the code to load your personal file
4. Execute the code
5. You can wait for the video capture to end, or alternatively press ***'q'*** on your keyboard to stop the execution 

# Project Report
- Here's a link to our project report: [.....](https://docs.google.com/document/d/1UT5YCXEsNrlOida02AvIHntJtMJGXVao/edit?usp=sharing&ouid=101209253185197768734&rtpof=true&sd=true)
