import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from google.colab import drive
import numpy as np
import os
import matplotlib.pyplot as plt

# --- Step 1: Mount Google Drive ---
print("Step 1: Mounting Google Drive...")
drive.mount('/content/drive')

# --- Step 2: Define paths and load the model ---
# Define the path to your saved model file
model_load_path = '/content/drive/MyDrive/weed_classifier/weed_binary_classifier_model.keras'

# Define the image size used during training
img_height = 224
img_width = 224

# Load the entire model
try:
    model = tf.keras.models.load_model(model_load_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# --- Step 3: Define class names and the test image path ---
# This list must match the alphabetical order of your dataset's folders
# Example: If your folders were 'Other_Weeds' and 'Target_Weed'
class_names = ['0.Kena_(Commplina_benghalensio)', '1..Lavhala_(Cyperus_Rotundus)']

# IMPORTANT: Replace this path with the location of your new test image on Drive
new_image_path = '/content/drive/MyDrive/mh-16 weed/Individual Weed_Species/0.Kena_(Commplina_benghalensio)/1108v77ej3i7042531_72..png_Class_0.png'

if not os.path.exists(new_image_path):
    print(f"Error: The image file at {new_image_path} does not exist.")
else:
    # --- Step 4: Load and preprocess the new image for prediction ---
    img = load_img(new_image_path, target_size=(img_height, img_width))
    img_array = img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    # --- Step 5: Make a prediction ---
    # The output is a single value between 0 and 1
    predictions = model.predict(img_array)[0][0]

    # --- Step 6: Interpret and display the result ---
    plt.imshow(img)
    plt.axis('off')

    if predictions > 0.5:
        # The second class name in the list is the target weed
        predicted_name = class_names[1]
        confidence = predictions * 100
        plt.title(f"Prediction: {predicted_name}\nConfidence: {confidence:.2f}%")
        print(f"This image is the target weed ({predicted_name}).")
        print(f"Confidence: {confidence:.2f}%")
    else:
        # The first class name in the list is the other weed
        predicted_name = class_names[0]
        confidence = (1 - predictions) * 100
        plt.title(f"Prediction: {predicted_name}\nConfidence: {confidence:.2f}%")
        print(f"This image is a different weed ({predicted_name}).")
        print(f"Confidence: {confidence:.2f}%")

    plt.show()