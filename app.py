import os
import random
import tempfile
from flask import Flask, render_template, send_from_directory, request, jsonify
from werkzeug import secure_filename

# Configuration
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'
DEBUG = True
dirname, filename = os.path.split(os.path.abspath(__file__))
UPLOAD_FOLDER = '{0}/media/audio'.format(os.path.abspath(dirname))
ALLOWED_EXTENSIONS = set( ['wav', 'mp3'])

app = Flask(__name__)      
app.config.from_object(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    # if uploading
    if request.method == 'POST':
        # get the audio file
        audio = request.files['audio_file']
        # if the audio is of an allowed filetype
        if audio and allowed_file(audio.filename):
            # secure the filename
            filename = secure_filename(audio.filename)
            temp_directory = tempfile.mkdtemp(dir=app.config['UPLOAD_FOLDER'])
            temp_folder = os.path.split(temp_directory)[1]
            full_path = os.path.join(temp_directory, 
                                        filename)
            print temp_directory
            print full_path
            audio.save(full_path)
            return jsonify(filename=filename,
                            filepath=os.path.join('media','audio', temp_folder, filename),
                            )
    return render_template('home.html')

@app.route('/iknow')
def iknow():
    return render_template('iknow.html')

@app.route('/media/audio/<temp_directory>/<filename>')
def serve_temp_audio(temp_directory, filename):
    return send_from_directory(
                                os.path.join(app.config['UPLOAD_FOLDER'],
                                            temp_directory),
                                filename
                                )

@app.route('/media/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)