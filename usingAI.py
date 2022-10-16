import tensorflow as tf
import numpy as np
import cv2

HRAI = tf.keras.models.load_model('handRecognition.h5')

test_image = tf.keras.utils.load_img('images/collected_images/predict/predictclosed1.jpg', target_size=(128, 128))
test_image = tf.keras.utils.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)
result = HRAI.predict(test_image)

print(result[0][0])

if result[0][0] == 1:
    prediction = 'you are showing a closed fist'
else:
    prediction = 'you are showing a open fist'

print(prediction)

