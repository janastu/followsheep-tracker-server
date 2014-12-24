from flask import (Flask, render_template, request, redirect,
                   url_for, flash)
from flaskext.uploads import (UploadSet, configure_uploads, ARCHIVES,
                              UploadConfiguration)
import os
import zipfile


SECRET_KEY = 'ajskbbcsdcudcusdvivaisciwef7t0239er9238reywoedhs'
app = Flask(__name__)
app.config.from_object(__name__)

uploaded_files = UploadSet('tracks', ARCHIVES,
                           default_dest=lambda app: app.instance_path)
configure_uploads(app, uploaded_files)

UPLOAD_DEST = os.path.join(os.path.abspath(__file__).rsplit('/', 1)[0],
                           'static/data')
uploaded_files._config = UploadConfiguration(UPLOAD_DEST)

configure_uploads(app, uploaded_files)


@app.route('/')
def index():
    print os.path.abspath(__file__)
    return render_template('index.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        filename = uploaded_files.save(request.files.get('track'))
        extract_file(filename)
        flash('Your upload was successful.')
        return redirect(url_for('upload'))
    return render_template('upload.html')


def extract_file(name):
    """TODO: Insert assertions for error handling."""
    zipF = zipfile.ZipFile(os.path.join(UPLOAD_DEST, name))
    zipF.extractall(os.path.join(UPLOAD_DEST, 'extracted_data'))

if __name__ == "__main__":
    app.run('localhost', 5000, True)