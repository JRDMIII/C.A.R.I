from cv2 import cv2
import time
import os
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# This sets up our camera to record
cap = cv2.VideoCapture(0)

prev_time = 0

def find_hands():
    results = mp_hands.proce

def gestureRec():

    # This reads what is currently being shown on the camera e.g. the current frame and
    # Saves it to a variable called "image". The variable return states whether an image
    # Was returned or not
    ret, image = cap.read()

    # This shows the saved frame on the screen in a window with the title "camera"
    cv2.imshow("Camera", image)

    new_time = time.time()
    fps = 1/(new_time-prev_time)
    prev_time = new_time

    if cv2.waitKey(1) and 0xff == ord('x'):
        cap.close()

    return -1

if __name__ == "__main__":
    while True:
        gestureRec()