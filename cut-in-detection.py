import cv2
import numpy as np
# import winsound
# import time as tm

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load COCO names file
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Initialize the video capture
cap = cv2.VideoCapture("/path/to/your/file")  # Change to 0 for webcam
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Known parameters
KNOWN_HEIGHT = 1.5  # meters (Average height of a car)
FOCAL_LENGTH = 700  # Example focal length in pixels (calibrate your camera to get this value)
SPEED = 16.67  # m/s i.e 60kmph (Average speed) 
prev_frame_time = 0
new_frame_time = 0


while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Resize frame to a smaller size
    frame = cv2.resize(frame, (640, 480))

    height, width, channels = frame.shape
     # font which we will be using to display FPS 
    font = cv2.FONT_HERSHEY_SIMPLEX 

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Information to show on screen
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] in ["car", "bus", "truck", "motorbike", "cow", "person"]:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    # Draw lane lines
    lane_color = (255, 0, 0)  # Blue color for lane lines
    line_thickness = 2

    # Points for the lane lines (adjust these values as needed)
    bottom_left = (int(width * 0.08), height)
    bottom_right = (int(width * 0.85), height)
    top_left = (int(width * 0.35), int(height * 0.6))
    top_right = (int(width * 0.52), int(height * 0.6))

    cv2.line(frame, bottom_left, top_left, lane_color, line_thickness)
    cv2.line(frame, bottom_right, top_right, lane_color, line_thickness)

    # Define lane boundaries
    lane_left_x = lambda y: int((top_left[0] - bottom_left[0]) * (y - bottom_left[1]) / (top_left[1] - bottom_left[1]) + bottom_left[0])
    lane_right_x = lambda y: int((top_right[0] - bottom_right[0]) * (y - bottom_right[1]) / (top_right[1] - bottom_right[1]) + bottom_right[0])
    
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = (0, 255, 0)  # Green for detected vehicles
            pts = np.array([[x + w // 2, y + 5], [x + w//2 - 8,y - 2], [x + w//2 - 1.5,y - 2],[x + w//2 - 1.5,y - 10], [x + w//2 + 1.5,y - 10], [x + w//2 + 1.5,y - 2],  [x + w//2 + 8,y - 2]], np.int32)
            #cv2.putText(frame, label, (x, y - 10), font, 0.5, color, 2)

            # Calculate the distance
            if label == "car":
                KNOWN_HEIGHT = 1.5
            if label == "bus":
                KNOWN_HEIGHT = 3.8
            if label == "truck":
                KNOWN_HEIGHT = 4
            if label == "motorbike":
                KNOWN_HEIGHT = 1
            if label == "cow":
                KNOWN_HEIGHT = 1.7
            if label == "person":
                KNOWN_HEIGHT = 1.6
            distance = (KNOWN_HEIGHT * FOCAL_LENGTH) / h
            time = distance / SPEED
            
            # Check if the object is within the lane lines
            if x + w - 5 > lane_left_x(y + h) and x + w - 5 < lane_right_x(y + h) and y + h > 0.6 * height:
                color = (0, 144, 255)  # Orange for objects within lane
                fff = 4000
                if time < 0.8:
                    color = (0, 0, 255)  # Red for danger Zone
                    fff = 1000
                # winsound.Beep(fff, 200)
                cv2.fillPoly(frame, [pts],color)
            if x + 5 > lane_left_x(y + h) and x + 5 < lane_right_x(y + h) and y + h > 0.6 * height:
                color = (0, 144, 255)  # Orange for objects within lane
                fff = 4000
                if time < 0.8:
                    color = (0, 0, 255)  # Red for danger Zone
                    fff = 1000
                # winsound.Beep(fff, 200)
                cv2.fillPoly(frame, [pts],color)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            #cv2.putText(frame, f"Distance: {distance:.2f}m", (x, y + h + 20), font, 0.5, (255, 0, 0), 2)
    
    # Display the frame
    cv2.imshow("Frame", frame)
    # time when we finish processing for this frame 
    # new_frame_time = tm.time()
    # fps = 1/(new_frame_time-prev_frame_time) 
    # prev_frame_time = new_frame_time 
    # fps = int(fps)
    # fps = str(fps) 
    # cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 
    # cv2.imshow('frame', frame)

    # Break the loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
