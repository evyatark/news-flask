from app import app, bs1, ReadSinglePage
from flask import render_template, Response
import json
import logging



logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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
return content-type json
'''
@app.route('/flask/start-page') # return content-type json
def page():
    urls = bs1.process_all()
    json_str = json.dumps(urls)
    return convert_to_json_response(json_str)

def convert_to_json_response(json_str):
    logger.error(json_str)
    r = Response(response=json_str, status=200, mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r

@app.route('/all.html')
def pageHtml():
    urls = bs1.process_all()
    #return "found the following urls: " + '        '.join(urls)
    return render_template('displayUrls.html', urls=urls)


'''
Process a single page of one article.
Returns: JSON representation of ArticleDetails
(return content-type json)
'''
@app.route('/flask/scrape-single-page/<string:url>') # return content-type json
def scrape_single_page(url):
    articleDetails = ReadSinglePage.readAndProcess(url)
    # dict = articleDetails.__dict__
    # dict.pop('id', 'dummy_value')
    # logger.error('+++' + str(dict))
    # json_str = json.dumps(dict)
    return convert_to_json_response1(articleDetails)

def convert_to_json_response1(articleDetails):
    dict = articleDetails.__dict__
    dict.pop('id', 'dummy_value')
    json_str = json.dumps(str(dict), ensure_ascii=False)
    logger.error(json_str)
    r = Response(response=json.loads(json_str), status=200, mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r
