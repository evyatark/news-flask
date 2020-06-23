from app import app, bs1
from flask import render_template
import json

@app.route('/hello')
def hello():
    bs1.process_page()
    return "Hello, amazing microblog World!"

@app.route('/')
def index():
    print('rendering...')
    return render_template('index.html')

'''
Process start page.
Returns: a list of relative URLs (such as '/sport/world-soccer/1.8940657')
'''
@app.route('/page')
def page():
    urls = bs1.process_all()
    return json.dumps(urls)
    #return render_template('displayUrls.html', urls=urls)

@app.route('/all.html')
def pageHtml():
    urls = bs1.process_all()
    #return "found the following urls: " + '        '.join(urls)
    return render_template('displayUrls.html', urls=urls)
