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
        self.mpHands = mp.solutions.hands
        self.hands = mp.solutions.hands.Hands()

        # This allows for annotations to be placed over the capture while it is running
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_draw_styles = mp.solutions.drawing_styles

    def detect_hand_landmarks(self, image, draw=True, draw_connections=True, draw_default_style=False):
        # This changes the image's colour to RGB format
        imageRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        landmark_data = []
        classified_hand_landmarks = [[], []]

        # Appying the hand tracking and finger tracking solution to the inputted image
        results = self.hands.process(imageRGB)
        landmarks = results.multi_hand_landmarks

        if landmarks:
            for hand_landmarks in landmarks:
                for id, landmark in enumerate(hand_landmarks.landmark):

                    height, width, c = image.shape
                    px, py = int(landmark.x*width), int(landmark.y*height)
                    data = (id, px, py)
                    landmark_data.append(data)
                if draw and not draw_connections:
                    self.mp_draw.draw_landmarks(image, hand_landmarks)
                elif draw and draw_connections and not draw_default_style:
                    self.mp_draw.draw_landmarks(image, hand_landmarks, self.mpHands.HAND_CONNECTIONS)
                elif draw and draw_connections and draw_default_style:
                    self.mp_draw.draw_landmarks(image,
                                                hand_landmarks,
                                                self.mpHands.HAND_CONNECTIONS,
                                                self.mp_draw_styles.get_default_hand_landmarks_style(),
                                                self.mp_draw_styles.get_default_hand_connections_style())
            if landmark_data[0][1] > landmark_data[4][1]:
                if len(landmark_data) > 20:
                    classified_hand_landmarks[1] = landmark_data[0:21]
                    classified_hand_landmarks[0] = landmark_data[21::]
                else:
                    classified_hand_landmarks[1] = landmark_data[0:21]
            elif landmark_data[4][1] > landmark_data[0][1]:
                if len(landmark_data) > 20:
                    classified_hand_landmarks[0] = landmark_data[0:21]
                    classified_hand_landmarks[1] = landmark_data[21::]
                else:
                    classified_hand_landmarks[0] = landmark_data[0:21]
        return classified_hand_landmarks, image

    def count_up_fingers(self, data):
        fingers = [[], []]
        if len(data[1]) != 0:
            if (data[1][3][1] > data[1][4][1]):
                fingers[1].append(1)
            else:
                fingers[1].append(0)

            if (data[1][5][2] > data[1][8][2] and data[1][7][2] > data[1][8][2]):
                fingers[1].append(1)
            else:
                fingers[1].append(0)
            if (data[1][9][2] > data[1][12][2] and data[1][11][2] > data[1][12][2]):
                fingers[1].append(1)
            else:
                fingers[1].append(0)
            if (data[1][13][2] > data[1][16][2] and data[1][15][2] > data[1][16][2]):
                fingers[1].append(1)
            else:
                fingers[1].append(0)
            if (data[1][17][2] > data[1][20][2] and data[1][19][2] > data[1][20][2]):
                fingers[1].append(1)
            else:
                fingers[1].append(0)
        if len(data[0]) != 0:
            if (data[0][3][1] < data[0][4][1]):
                fingers[0].append(1)
            else:
                fingers[0].append(0)
            if (data[0][5][2] > data[0][8][2] and data[0][7][2] > data[0][8][2]):
                fingers[0].append(1)
            else:
                fingers[0].append(0)
            if (data[0][9][2] > data[0][12][2] and data[0][11][2] > data[0][12][2]):
                fingers[0].append(1)
            else:
                fingers[0].append(0)
            if (data[0][13][2] > data[0][16][2] and data[0][15][2] > data[0][16][2]):
                fingers[0].append(1)
            else:
                fingers[0].append(0)
            if (data[0][17][2] > data[0][20][2] and data[0][19][2] > data[0][20][2]):
                fingers[0].append(1)
            else:
                fingers[0].append(0)
        else:
            print("Nah nothin")

        return fingers