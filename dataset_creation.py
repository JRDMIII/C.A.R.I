# These are the modules that will be used to take pictures
import cv2
import os
import time
import uuid

# === Dataset Creation === #
def dataset_creation():

    # These are the names for the different hand signs I will have
    # labels = ['one', 'two', 'three', 'thumbs up', 'thumbs down']
    labels = ['open_fist']
    # This defines how many images there will be for each
    number_images = 10

    # This defines the base image path that will be augmented for each label
    IMAGE_PATH = 'C:/Users/Dami/PycharmProjects/C.A.R.I/images/collected_images/test_set'


    # This for loop iterates through every label within the labels list
    for label in labels:
        # This begins capturing the camera
        cap = cv2.VideoCapture(0)
        print('Collecting images for {}'.format(label))

        # This gives me some time to set up before the pictures start getting taken
        time.sleep(5)
        for num in range(number_images):
            # This gets the current frame from the camera
            ret, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #imagename is the directory + name given to the current image being taken and stored
            imagename = os.path.join(IMAGE_PATH, label, label+'.'+'{}.jpg'.format(str(uuid.uuid1())))
            # imagename = os.path.join(IMAGE_PATH, label, label + 'closed1.jpg')

            # This writes the image to the file directory
            # print("saving to {}".format(imagename))
            cv2.imwrite(imagename, frame)
            cv2.imshow('frame', frame)
            time.sleep(0.7)

            # This checks to see if the 'q' key is pressed and closes the window if so
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()



dataset_creation()


