from flask import Flask, redirect, request, jsonify, render_template, current_app
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from google.cloud import vision
from google.cloud.vision import types
import config
import requests
import os
import io

identified_food = None
array_of_locations = [[],[],[]]

app = Flask(__name__)

# Instantiates a client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "keys.json"
client = vision.ImageAnnotatorClient()

# Uploads settings
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads' # File save location
configure_uploads(app, photos)

# Main route
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        global file_name
        file_name = photos.save(request.files['photo'])
        return render_template('index.html')
    return render_template('index.html')

# Identify object route
@app.route('/identify', methods=['GET'])
def identify():
    # Loads the image into memory
    with io.open("static/uploads/" + file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)
        identified_food = label.description
        identified_food.replace(" ", "")
        
        # Make request to Places API
        result = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?query=' + identified_food + '&key=' + config.api_key)
        # print(result.json())

        # Show top 3 locations
        for i in range(3):
            array_of_locations[i].append(result.json()["results"][i]["geometry"]["location"]["lat"])
            array_of_locations[i].append(result.json()["results"][i]["geometry"]["location"]["lng"])
        print(array_of_locations)
        return render_template('index.html')
    return render_template('index.html', locations = array_of_locations)

if __name__ == '__main__':
    app.run(port=5000)