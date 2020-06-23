from app import app
from flask import render_template

@app.route('/hello')
def hello():
    return "Hello, amazing microblog World!"

@app.route('/')
def index():
    print('rendering...')
    return render_template('index.html')

