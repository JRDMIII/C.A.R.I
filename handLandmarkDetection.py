import cv2 as cv
import mediapipe as mp
import time

# This class will contain all the methods used to classify which fingers are currently up
# And which are currently down. Using this class we can then define which sequence of numbers
# Corresponds to which hand signal

class handLandmarkDetection():

    # This is the initialisation method
    def __init__(self):
        # === Defining parameters for the hand/finger tracking solution === #


        self.image_mode = False

        # This defines the maximum number of hands which will be detected in the image
        self.max_hands = 2

        # This is the minimum confidence level that must be achieved for the detection
        # To be considered successful
        self.min_detection_confidence = 0.8

        # This is the minimum confidence value from the landmark-tracking model that must
        # Be achieved for the tracking to be considered successful. If this isn't the case,
        # hand detection will be invoked automatically on the next input image
        self.min_tracking_confidence = 0.5

        # This initialises the hand tracking and finger tracking solution, inputting in all the parameters just defined above
        self.hands = mp.solutions.hands.Hands(self.image_mode, self.max_hands, self.min_detection_confidence, self.min_tracking_confidence)

        # This allows for annotations to be placed over the capture while it is running
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_draw_styles = mp.solutions.drawing_styles

