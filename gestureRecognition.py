import cv2
import time
import os
import mediapipe as mp

import handLandmarkDetection

landmarkDetection = handLandmarkDetection.handLandmarkDetection()

def gestureRec():
    print("We Checkin hand signs")

    # Sets up video capture
    cap = cv2.VideoCapture(0)

    # The amount of iterations that will occur for checking which hand gesture is being done
    iteration_amt = 20

    # The percent is must be above for the hand gesture prediction to be accepted
    min_certainty = 0.75

    # This reads what is currently being shown on the camera e.g. the current frame and
    # Saves it to a variable called "image". The variable return states whether an image
    # Was returned or not
    past = []
    for i in range(0, iteration_amt):
        ret, image = cap.read()


        landmarks, image = landmarkDetection.detect_hand_landmarks(image, draw_default_style=False)

        fingers = landmarkDetection.count_up_fingers(landmarks)
        fingers_up = int(fingers[0].count(1)) + int(fingers[1].count(1))
        print(str(fingers_up))
        past.append(fingers_up)

    hand_gesture = past[0]
    if hand_gesture == 0:
        return -1, True
    else:
        percent_certainty = past.count(hand_gesture)/iteration_amt
        print(str(percent_certainty))
        if percent_certainty > min_certainty:
            print("Decided on a ", hand_gesture)
            return hand_gesture, False

    return -1, True



