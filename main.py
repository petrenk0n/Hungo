from flask import Flask, redirect, request, jsonify, render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os

app = Flask(__name__)

# Uploads settings
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'
configure_uploads(app, photos)

# Main route
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        filename = photos.save(request.files['photo'])
        return render_template('index.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8000)