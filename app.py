from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- Model Loading and Configuration ---
# Make sure your model file is in the same directory as this script.
model_load_path = 'weed_binary_classifier_model.keras'
img_height = 224
img_width = 224

try:
    model = tf.keras.models.load_model(model_load_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# This list must match the alphabetical order of your training dataset's folders
class_names = ['0.Kena_(Commplina_benghalensio)', '1..Lavhala_(Cyperus_Rotundus)']

# Set the upload folder and allowed file extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        # Save the uploaded image securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Preprocess and predict
        img = load_img(filepath, target_size=(img_height, img_width))
        img_array = img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch dimension

        predictions = model.predict(img_array)[0][0]

        if predictions > 0.5:
            predicted_name = class_names[1]
            confidence = float(predictions * 100)
        else:
            predicted_name = class_names[0]
            confidence = float((1 - predictions) * 100)

        return jsonify({
            'prediction': predicted_name,
            'confidence': f"{confidence:.2f}%",
            'image_url': f"/{filepath}"
        })
    else:
        return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    # Create the uploads folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)