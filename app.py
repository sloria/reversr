from flask import Flask, render_template, request, \
                flash, redirect, abort, url_for, g
from flask.ext.uploads import UploadSet, AUDIO, configure_uploads, patch_request_class
import peewee

# Configuration
DATABASE = 'reversr.db'
UPLOADS_DEFAULT_DEST = '/Users/sloria1/projects/flask-projects/reversr/media/'
UPLOADS_DEFAULT_URL = 'http://localhost:5000/'
UPLOADED_AUDIO_DEST = '/Users/sloria1/projects/flask-projects/reversr/media/audio'
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'
DEBUG = True

# Database
db = peewee.SqliteDatabase(DATABASE)

app = Flask(__name__)      
app.config.from_object(__name__)

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Audio(BaseModel):
    filename = peewee.CharField()


# simple utility function to create tables
def create_tables():
    db.connect()
    if Audio.table_exists():
        print "Table already exists."
    else:
        print "Creating tables..."
        Audio.create_table()
        
# The upload set
audio = UploadSet('audio', AUDIO)
configure_uploads(app, upload_sets=[audio])
patch_request_class(app, 10 * 1024 * 1024) # 10 MB

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and 'audio' in request.files:
        filename = audio.save(request.files['audio'])
        rec = Audio.create(filename=filename)
        flash("Reversed!", 'info')
        return redirect(url_for('show', id=rec.id))
    return render_template('home.html')

@app.route('/audio/<id>', methods=['GET', 'POST'])
def show(id):
    if request.method == 'POST' and 'audio' in request.files:
        filename = audio.save(request.files['audio'])
        rec = Audio.create(filename=filename)
        flash("Reversed!", 'info')
        return redirect(url_for('show', id=rec.id))
    audio_obj = Audio.get(id=id)
    if not audio_obj: abort(404) # TODO: make a page for this case
    url = audio.url(audio_obj.filename)
    return render_template('home.html', url=url, audio=audio_obj)

# request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.  peewee will do
# this for us, but its generally a good idea to be explicit.
@app.before_request
def before_request():
    g.db = db
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response
 
if __name__ == '__main__':
    create_tables()
    app.run()