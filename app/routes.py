from app import app, bs1, ReadSinglePage
from flask import render_template, Response, make_response, jsonify
import json
import logging



logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.route('/hello')
def hello():
    #bs1.process_page()
    return "Hello, amazing microblog World!"

@app.route('/')
def index():
    print('rendering...')
    return render_template('index.html')

'''
Process start page. (currently starting from "www.haaretz.co.il",
in future the start-page will be specified by the argument)
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
    #json_str = json.dumps(str(dict), ensure_ascii=False)    # without ensure_ascii=False we receive \unnnn instead of Hebrew characters
    #json_str = json_str.replace("'", '"')
    #logger.error(json_str)
    r = jsonify(dict)
    #r = jsonify('{"siteId": "1","createdAt": "2", "updatedAt": "3"}')
    #r = Response(response=dict, status=200, mimetype="application/json")
    #r = Response(response=json.loads(json_str), status=200, mimetype="application/json")
    #r.headers["Content-Type"] = "application/json; charset=utf-8"
    return r


@app.route('/flask/strip-single-page/<string:siteId>') # return content-type HTML!!
def strip_single_page(siteId):
    html = ReadSinglePage.readAndStrip(siteId)
    content_type = 'text/html; charset=utf-8'
    headers = {'Content-Type': content_type}
    response = make_response(html, 200, headers)
    return response