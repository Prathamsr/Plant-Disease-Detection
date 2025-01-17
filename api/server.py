from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from io import BytesIO
from PIL import Image
import os

# Define classes and solutions
classes = {
    'apple': ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy'],
    'cherry': ['Cherry_(including_sour)___healthy', 'Cherry_(including_sour)___Powdery_mildew'],
    'peach': ['Peach___Bacterial_spot', 'Peach___healthy'],
    'pepper': ['Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy'],
    'potato': ['Potato___Early_blight', 'Potato___healthy', 'Potato___Late_blight'],
    'strawberry': ['Strawberry___healthy', 'Strawberry___Leaf_scorch']
}

solutions = {
    'Apple___Apple_scab': "Use fungicides like Captan or Mancozeb. Practice proper pruning to improve air circulation.",
    'Apple___Black_rot': "Remove and destroy infected fruit and branches. Apply fungicides during the growing season.",
    'Apple___Cedar_apple_rust': "Use resistant apple varieties. Apply fungicides like Myclobutanil at bud break.",
    'Apple___healthy': "Maintain proper care with adequate watering, fertilization, and pest control.",
    'Cherry_(including_sour)___healthy': "Ensure regular pruning, pest management, and balanced fertilization.",
    'Cherry_(including_sour)___Powdery_mildew': "Apply sulfur-based fungicides. Remove and dispose of infected leaves.",
    'Peach___Bacterial_spot': "Use copper-based bactericides. Avoid overhead irrigation and remove infected material.",
    'Peach___healthy': "Maintain good cultural practices with proper pruning and pest management.",
    'Pepper,_bell___Bacterial_spot': "Use disease-free seeds, crop rotation, and copper-based bactericides.",
    'Pepper,_bell___healthy': "Maintain optimal growing conditions and monitor for pests or diseases.",
    'Potato___Early_blight': "Apply fungicides like Chlorothalonil or Mancozeb. Practice crop rotation.",
    'Potato___healthy': "Ensure proper soil fertility and drainage. Monitor for pests or diseases.",
    'Potato___Late_blight': "Apply fungicides like Metalaxyl or Mancozeb. Remove infected plants promptly.",
    'Strawberry___healthy': "Maintain clean cultivation practices and proper fertilization.",
    'Strawberry___Leaf_scorch': "Remove and destroy infected leaves. Apply fungicides like Captan or Thiram."
}

app = Flask(__name__)

# Enable CORS for all routes (for development purposes)
CORS(app)

# Function to read image as numpy array
def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.route('/predict', methods=['POST'])
def predict():
    # Check if the file and form data are provided
    if 'file' not in request.files or 'plant' not in request.form:
        return jsonify({"message": "Image and plant type are required"}), 400
    
    file = request.files['file']
    plant = request.form['plant']
    
    if file.filename == '':
        return jsonify({"message": "No file selected"}), 400
    
    # Read the image and prepare the input
    image = read_file_as_image(file.read())
    img_batch = np.expand_dims(image, 0)
    
    # Load the model for the specified plant type
    model_path = f"./models/{plant}"
    if not os.path.exists(model_path):
        return jsonify({"message": f"Model for {plant} not found"}), 400

    model = tf.keras.models.load_model(model_path)
    
    # Predict the class
    predictions = model.predict(img_batch)
    predicted_class = classes[plant][np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    
    # Get the solution
    solution = solutions.get(predicted_class, "Solution not available.")
    
    # Return the prediction results
    return jsonify({
        'class': " ".join(predicted_class.replace('_'," ").replace(","," ").split(" ")),
        'confidence': float(confidence),
        'plant': plant,
        'solution': solution
    }), 200

if __name__ == '__main__':
    app.run(debug=True,  port=8000)
