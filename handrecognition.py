# These are the modules that will be used for the AI
import tensorflow as tf
from keras.preprocessing import image
import numpy as np

# === Section 1 - Importing Dataset === #

# Here the data is being imported and augmentations are being applied to the images
training_datagen = image.ImageDataGenerator(rescale=1./255,
                                            shear_range=0.2,
                                            zoom_range=0.2,
                                            horizontal_flip=True)
training_set = training_datagen.flow_from_directory('images/collected_images/training_set',
                                                    target_size=(128, 128),
                                                    batch_size=16,
                                                    class_mode='binary')

# Here the data is being imported and augmentations are being applied to the images
test_datagen = image.ImageDataGenerator(rescale=1./255)
test_set = test_datagen.flow_from_directory('images/collected_images/test_set',
                                                    target_size=(128, 128),
                                                    batch_size=16,
                                                    class_mode='binary')

# === Section 2 - Neural Network Creation === #

# This creates a basic, empty CNN
cnn = tf.keras.models.Sequential()

# This adds the first convolutional layer to the CNN and a pooling layer
cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=[128, 128, 3]))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

# This adds the second convolutional layer to the CNN and a pooling layer
cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

# This flattens all the data so it can by inputted into a fully connected layer
cnn.add(tf.keras.layers.Flatten())

# This adds the fully connected layer
cnn.add(tf.keras.layers.Dense(units=256, activation='relu'))

# This adds an output layer
cnn.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

# === Section 3 - Training the CNN === #
cnn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

cnn.fit(x=training_set, validation_data=test_set, epochs=50)

cnn.save('handRecognition.h5')

