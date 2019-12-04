# -*- coding: utf-8 -*-
import os
import config
from flask import Flask, flash, request, send_from_directory, jsonify, send_file
from werkzeug.utils import secure_filename
from image_converter import ImageConverter

app = Flask(__name__, static_folder='zip_files')
app.config['UPLOAD_FOLDER'] = config.upload_folder
app.config['MAX_CONTENT_LENGTH'] = config.max_img_size_mb * 1024 * 1024
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['POST', 'GET'])
def twitch_smile_resizer():
    if request.method == 'GET':
        return send_from_directory(directory='./', filename='index.html')
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
        resample_type = request.form['resample']
        converted_images_name = ImageConverter().convert_image_to_twitch_format(secure_filename(file.filename), resample=resample_type)

        if not converted_images_name:
            os.remove(file.filename)
            return jsonify({"error": "please add square image file"})
        os.remove(file.filename)
        return send_file(os.path.join('zip_files', converted_images_name), as_attachment=True)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = config.debug
    app.run(host=config.flask_host, port=config.flask_port)
