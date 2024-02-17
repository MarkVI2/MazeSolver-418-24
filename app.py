from uuid import uuid4
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, send_from_directory, url_for, Response
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    image_filename = 'default.jpg'
    if 'image_filename' in request.args:
        image_filename = request.args['image_filename']
    return render_template('index.html', image_filename=image_filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Return the URL of the uploaded image
            return redirect(url_for('index', image_filename=filename))
        else:
            invalid_file_type = True
    else:
        invalid_file_type = False

    return render_template('index.html', invalid_file_type=invalid_file_type)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
