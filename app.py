from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files['image']
        if image_file:
            image_filename = os.path.join('uploads', image_file.filename)
            image_file.save(image_filename)
            return redirect(url_for('index', image_filename=image_filename))
    image_filename = request.args.get('image_filename')
    return render_template('index.html', image_filename=image_filename)


if __name__ == '__main__':
    app.run(debug=True)
