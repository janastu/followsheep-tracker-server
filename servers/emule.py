from app import create_app
from flask import (render_template, request, redirect,
                   url_for, flash, make_response, Response)
from flaskext.uploads import (UploadSet, configure_uploads, ARCHIVES,
                              UploadConfiguration)
from flask.ext.pymongo import PyMongo
import hashlib
import subprocess
import json
import os
import zipfile
from functools import wraps


app = create_app()

UPLOAD_DEST = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'static/data')

uploaded_files = UploadSet('tracks', ARCHIVES,
                           default_dest=lambda app: app.instance_path)
configure_uploads(app, uploaded_files)
uploaded_files._config = UploadConfiguration(UPLOAD_DEST)

configure_uploads(app, uploaded_files)
mongo = PyMongo(app)


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    users = app.config.get('USERS')
    passkey = app.config.get('SECRET')[0]
    if username in users and passkey == password:
        return username


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def index():
    return render_template('index.html', tracks=get_all_tracks())


@app.route('/upload', methods=['POST', 'GET'])
#@requires_auth
def upload():
    if request.method == "POST":
        filename = uploaded_files.save(request.files.get('track'))
        hash = hashlib.md5()
        fObject = open(os.path.join(UPLOAD_DEST, filename), 'r')
        for chunk in iter(lambda: fObject.read(
                4096), ""):
            hash.update(chunk)
        if mongo.db.tracks.find_one({'checksum': hash.hexdigest()}):
            flash('Duplicate file!!')
            return redirect(url_for('index'))
        extract_file(filename, hash.hexdigest())
        flash('Your upload was successful.')
        return redirect(url_for('index'))
    return render_template('upload.html')


def extract_file(name, checksum):
    """TODO: Insert assertions for error handling."""
    """Extract the zip and save the contents of the zip into a directory
    organized by username in the config file."""
    with zipfile.ZipFile(os.path.join(UPLOAD_DEST, name)) as zipF:
        for fileName in zipF.infolist():
            if fileName.filename.endswith('.json'):
                configFilePath = fileName.filename
                break
        if configFilePath.find('/'):
            configDirName = configFilePath.split('/')[0]
        with zipF.open(configFilePath) as f:
            config = json.load(f)
            zipF.extractall(os.path.join(UPLOAD_DEST, 'extracted_data',
                                         config.get('Device ID'),
                                         config.get('User')))
        for files in zipF.infolist():
            if files.filename.endswith(".gpx"):
                url = url_for('static',
                              filename=os.path.join('data',
                                                    'extracted_data',
                                                    config.get('Device ID'),
                                                    config.get('User'),
                                                    files.filename))
                config['track-path'] = url
                config['track-name'] = files.filename.rstrip('.gpx').split(
                    '/')[-1]
        try:
            dirPath = configDirName
        except NameError:
            dirPath = ''
        subprocess.Popen(['bash', os.path.abspath(os.path.join(
            os.path.dirname(__file__), os.pardir, 'scripts', 'convert.sh')),
                         os.path.join(UPLOAD_DEST, 'extracted_data',
                                      config.get('Device ID'),
                                      config.get('User'),
                                      dirPath)])
    config['data-path'] = config.get('track-path').rsplit('/', 1)[0]
    config['checksum'] = checksum
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


@app.route('/track/<ObjectId:id>', methods=["POST"])
def upload_track(id):
    mongo.db.tracks.update({'_id': id}, {'$set': {
        'track': json.loads(request.form.get('track'))}})
    response = make_response()
    return response
