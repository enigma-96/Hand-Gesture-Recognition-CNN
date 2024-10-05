import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import pyttsx3                               # type: ignore
import threading
import time

# Function to speak out the predicted label
def speak_label(label):
    engine.say(label)                                          
    engine.runAndWait()

cap = cv2.VideoCapture(0)   
detector = HandDetector(maxHands=2)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
offset = 20
imgSize = 128
counter = 0

labels = ["Hello", "I Love you", "No", "okay", "Thank you", "yes"]

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Get screen resolution
screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Decrease the size of the output window
output_width = int(screen_width * 1.2)
output_height = int(screen_height * 1.2)

# Define the dirty orange color in BGR format
dirty_orange = (0, 166, 255)  # #ffa600 in BGR

quit_flag = False

while not quit_flag:
    success, img = cap.read()

    if not success:
        print("Failed to read frame.")
        continue  # Continue to the next iteration of the loop if frame reading fails

    imgOutput = np.zeros((screen_height, screen_width, 3), np.uint8)  # Create black background
    imgOutput[0:screen_height, 0:screen_width] = img  # Place original frame on black background

    hands, img = detector.findHands(img)

    # Check if hands are detected
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']

            # Check if hand bounding box coordinates are valid
            if x < 0 or y < 0 or w <= 0 or h <= 0:
                continue  # Skip this hand if bounding box coordinates are invalid

            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

            # Check if imgCrop is empty
            if imgCrop.size == 0:
                print("Empty hand crop. Skipping...")
                continue

            imgCropShape = imgCrop.shape

            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                imgWhite[:, wGap: wCal + wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                accuracy = prediction[index] * 100  # Get accuracy percentage

            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                imgWhite[hGap: hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                accuracy = prediction[index] * 100  # Get accuracy percentage

            # Speak out the predicted label in a separate thread
            threading.Thread(target=speak_label, args=(labels[index],)).start()

            # Create a transparent overlay for the prediction box
            overlay = imgOutput.copy()
            box_height = 50  # Height of the prediction box
            box_width = w + 20  # Increased width of the prediction box
            box_y1 = y - offset - box_height - 10  # Adjust the vertical position to be higher
            box_y2 = box_y1 + box_height
            cv2.rectangle(overlay, (x - 10, box_y1), (x - 10 + box_width, box_y2), (0, 0, 0), cv2.FILLED)
            alpha = 0.6  # Transparency factor
            imgOutput = cv2.addWeighted(overlay, alpha, imgOutput, 1 - alpha, 0)

            # Add the text with white color
            cv2.putText(imgOutput, f"{labels[index]} {accuracy:.2f}%", (x, box_y1 + 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)


            # Draw hand outline with the specified dirty orange color
            cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), dirty_orange, 4)

            cv2.imshow('ImageCrop', imgCrop)
            cv2.imshow('ImageWhite', imgWhite)

    # Resize the window displaying the output
    imgOutput = cv2.resize(imgOutput, (output_width, output_height))
    cv2.imshow('Image', imgOutput)
    cv2.resizeWindow('Image', output_width, output_height)

    # Check for key events including 'q' to exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        quit_flag = True

    # Check if the window has been closed
    if cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1:
        quit_flag = True

# Close OpenCV windows immediately
cv2.destroyAllWindows()

# Release video capture device
cap.release()
