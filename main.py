 
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import numpy as np
import tensorflow as tf

# Load the pre-trained model
model = tf.keras.models.load_model('brand_identification_model.h5')

# Initialize the Flask app
app = Flask(__name__)

# Define the main route
@app.route('/')
def index():
    return render_template('index.html')

# Define the route to handle image uploads
@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded image
    image = request.files['image']

    # Preprocess the image
    image = Image.open(image)
    image = image.resize((224, 224))
    image = np.array(image) / 255.0

    # Make a prediction
    prediction = model.predict(np.expand_dims(image, axis=0))

    # Get the brand name
    brand = prediction.argmax()

    # Redirect to the results page
    return redirect(url_for('results', brand=brand))

# Define the route to display the results
@app.route('/results')
def results():
    # Get the brand name from the query string
    brand = request.args.get('brand')

    # Render the results page
    return render_template('results.html', brand=brand)

# Run the app
if __name__ == '__main__':
    app.run()
