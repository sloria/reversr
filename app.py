import os
from flask import Flask, render_template

# Configuration
SECRET_KEY = 'hin6bab8ge25*r=x&amp;+5$0kn=-#log$pt^#@vrqjld!^2ci@g*b'
DEBUG = True

app = Flask(__name__)      
app.config.from_object(__name__)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)