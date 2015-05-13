from app import create_app
from flask import (render_template, request, redirect,
                   url_for, flash)
from flaskext.uploads import (UploadSet, configure_uploads, ARCHIVES,
                              UploadConfiguration)
from flask.ext.pymongo import PyMongo
import json
import os
import zipfile
import ogr2ogr

app = create_app()

UPLOAD_DEST = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'static/data')

uploaded_files = UploadSet('tracks', ARCHIVES,
                           default_dest=lambda app: app.instance_path)
configure_uploads(app, uploaded_files)
uploaded_files._config = UploadConfiguration(UPLOAD_DEST)

configure_uploads(app, uploaded_files)
mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html', tracks=get_all_tracks())


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
    """Extract the zip and save the contents of the zip into a directory
    organized by username in the config file.
    Save the GeoJSON output of the gpx in a mongo db instance."""
    with zipfile.ZipFile(os.path.join(UPLOAD_DEST, name)) as zipF:
        with zipF.open('config.json') as f:
            config = json.load(f)
            zipF.extractall(os.path.join(UPLOAD_DEST, 'extracted_data',
                                         config.get('Device ID'),
                                         config.get('User')))
        for files in zipF.infolist():
            if files.filename.endswith(".gpx"):
                with zipF.open(files) as f:
                    ogr2ogr.main(['', '-skipfailures', '-f', 'GeoJSON',
                                  os.path.join(UPLOAD_DEST, files.filename +
                                               '.json'),
                                  os.path.join(UPLOAD_DEST, 'extracted_data',
                                               config.get('Device ID'),
                                               config.get('User'),
                                               files.filename)])
                    filename = os.path.join(UPLOAD_DEST, files.filename +
                                            '.json')
                    with open(filename) as jsonFile:
                        config['track'] = json.load(jsonFile)
                    os.remove(filename)
                config['track-name'] = files.filename.rstrip('.gpx')
    mongo.db.tracks.save(config)
    return True


def get_all_tracks():
    tracks = [track for track in mongo.db.tracks.find()]
    for track in tracks:
        track['id'] = str(track['_id'])
        track['device_ID'] = track['Device ID']
        track['track_name'] = track['track-name']
        del(track['_id'])
        del(track['Device ID'])
        del(track['track-name'])
    return tracks
