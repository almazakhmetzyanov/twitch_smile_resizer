# -*- coding: utf-8 -*-
import os
from flask import Flask, flash, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from image_converter import ImageConverter

app = Flask(__name__, static_folder='zip_files')
upload_folder = '/home/tsr/'
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
UPLOAD_FOLDER = '/home/tsr/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/tsr", methods=['POST'])
def twitch_smile_resizer():
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({"error": "please add square image file"})
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        filename = file.filename
        if file.filename == '':
            flash('No selected file')
            return jsonify({"error": "please add square image file"})

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        converted_images_name = ImageConverter().convert_image_to_twitch_format(secure_filename(file.filename))

        if not converted_images_name:
            os.remove(file.filename)
            return jsonify({"error": "please add square image file"})
        os.remove(file.filename)
        dwnld_url = 'http://corruptedmushroom.space:5000/dwnld/{}'.format(converted_images_name)
        return dwnld_url


@app.route('/dwnld/<filename>', methods=['GET'])
def dwnld(filename):
    return send_from_directory(directory='zip_files', filename=secure_filename(filename))


if __name__ == "__main__":
    app.debug = 'True'
    app.run(host='0.0.0.0')