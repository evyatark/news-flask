import logging
from bs4 import BeautifulSoup
from time import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from app import Constants, ArticleDetails, ArticleContent, Utils, ProcessHaaretzHtml

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def browseUrl(url):
    ts = time()
    logger.debug("[%s] loading %s...", 'id', url)
    request = Request(url, headers={'User-Agent': Constants.user_agent})
    ##
    #
    html = Utils.load_html(request)
    #
    ##
    logger.debug('[%s] loading completed in %s seconds', 'id', time() - ts)
    ts = time()
    return html;


def soupHtml(html):
    ts = time()
    logger.debug("[%s] souping...", "id")
    bs = BeautifulSoup(html, 'html.parser')
    if (bs.article is None):
        return bs, False

    # first find publish time, if too old, we don't need to continue parsing
    if not decide_include_article(fast_find_times(bs)):
        logger.debug("stopped processing this article - too old")
        return bs, False

    logger.debug('[%s] souping completed in %s seconds', "id", time() - ts)

    return bs, True




'''
returns stripped HTML
'''
def readAndStrip(siteId):
    logger.info("===================== started ===================")
    url = "https://www.haaretz.co.il/amp/" + siteId
    try:
        html = browseUrl(url)   # create actual HTTP request to the url (including the special user-agent), to load its HTML
    except HTTPError as err:    # 404 not found
        logger.error("HTTPError, code={0}".format(err.code))
        return False

    bs, success = soupHtml(html)    # BeautifulSoup bs
    if success:
        stripped_html = ProcessHaaretzHtml.strip_content(bs)
        return stripped_html
    else:
        return False    # souping failed




def readAndProcess(siteId):
    logger.info("===================== started ===================")
    url = "https://www.haaretz.co.il/amp/" + siteId
    try:
        html = browseUrl(url)   # create actual HTTP request to the url (including the special user-agent), to load its HTML
    except HTTPError as err:    # 404 not found
        logger.error("HTTPError, code={0}".format(err.code))
        articleDetails = ArticleDetails.ArticleDetails('-1', err.code, '', '', '', '')
        return articleDetails

    logger.error(html)  #should be info not error
    bs, success = soupHtml(html)    # BeautifulSoup bs
    if not bs:
        return ArticleDetails.ArticleDetails('-1', Constants.HEADER_OF_UNKNOWN, '', '', '', '')

    articleDetails = scrape_details(siteId, bs)
    return articleDetails



def scrape_details(siteId, bs):
    url = "https://www.haaretz.co.il/amp/" + siteId

    ## scrape from <head>
    description = bs.head.find(name='meta', attrs={"name": "twitter:description"}).attrs['content']
    image1 = bs.head.find(name='meta', attrs={"name": "twitter:image"}).attrs['content']
    title = bs.head.find(name='meta', attrs={"name": "twitter:title"}).attrs['content']
    site = bs.head.find(name='meta', attrs={"name": "twitter:site"}).attrs['content']
    site_name_hebrew = bs.head.find(name='meta', attrs={"property": "og:site_name"}).attrs['content']
    originalUrl = bs.head.find(name='meta', attrs={"property": "og:url"}).attrs['content']
    pubDate = bs.head.find(name='meta', attrs={"property": "og:pubdate"}).attrs['content']


    article = ArticleDetails.ArticleDetails(siteId, title, pubDate, '', '', '')
    article.description = description
    article.url = url
    article.originalUrl = originalUrl
    article.site = site
    article.siteId = siteId
    article.image1 = image1

    ## scrape from <body>
    publishedAt, updatedAt = find_times(bs)
    try:
        author = bs.article.find(name='span', class_='js-stat-util-info').attrs['data-statutil-writer']
    except:
        author=''
    #image1 = bs.article.find(name='figure', class_='c-figure__main').find(name='amp-img').attrs['src']
    image2 = bs.article.find(name='figure', class_='c-figure--wide').find(name='amp-img').attrs['src']
    header_crumbs_root = bs.article.find(name='ol', class_='c-article-header__crumbs')
    header_crumbs = header_crumbs_root.find_all('li', class_='c-article-header__crumb')
    if len(header_crumbs) > 0:
        article.subject = header_crumbs[0].text.rstrip().lstrip()
    if len(header_crumbs) > 1:
        article.sub_subject = header_crumbs[1].text.rstrip().lstrip()

    article.updatedAt = updatedAt
    if (not article.createdAt):
        article.createdAt = publishedAt
    article.author = author
    article.image2 = image2

    # try:
    #     #header = bs.article.header.h1.contents[-1]
    #     header = bs.article.header.h1.text.rstrip().lstrip()
    # except:
    #     header = Constants.HEADER_OF_UNKNOWN
    #
    # ts = time()
    # logger.debug("[%s] processing...", 'id')
    # sections = bs.article.findAll(name='section', class_='b-entry')
    # if (sections is None) or len(sections) == 0:
    #     logger.error('0 sections, abort')
    #     return ArticleDetails.ArticleDetails(siteId, header, '', '', '', '')
    # first = sections[0]
    #
    # publishedAt, updatedAt = find_times(bs)
    #
    # header_crumbs_root = bs.article.find(name='ol', class_='c-article-header__crumbs')
    # header_crumbs = header_crumbs_root.find_all('li', class_='c-article-header__crumb')
    # description = bs.article.find(name='p', class_='c-article-header__lede').text.rstrip().lstrip()
    # author = bs.article.find(name='span', class_='js-stat-util-info').attrs['data-statutil-writer']
    # subject = ''
    # sub_subject = ''
    # if len(header_crumbs) > 0:
    #     subject = header_crumbs[0].text.rstrip().lstrip()
    # if len(header_crumbs) > 1:
    #     sub_subject = header_crumbs[1].text.rstrip().lstrip()
    # image1 = bs.article.find(name='figure', class_='c-figure__main').find(name='amp-img').attrs['src']
    # image2 = bs.article.find(name='figure', class_='c-figure--wide').find(name='amp-img').attrs['src']

# image: https://images.haarets.co.il/image/fetch/w_1200,q_auto,c_fill,f_auto/fl_any_format.preserve_transparency.progressive:none/https://www.haaretz.co.il/polopoly_fs/1.8941144!/image/2872796886.jpg
    # use w_1200 to request the width you want

    # <figure class="c-figure__main u-bgc--bg-inverse u-c--text-inverse u-mh--0 u-type--micro u-pos--r">    <amp-img layout='responsive'
    # <figure class="c-figure c-figure--wide u-mh--0 u-pos--r">     <amp-img layout='responsive'
    # <figure class="c-figure c-figure--wide u-mh--0 u-pos--r">     <amp-img layout='responsive'
    # article = ArticleDetails.ArticleDetails(siteId, header, publishedAt, updatedAt, subject, sub_subject)
    # if (description):
    #     article.description = description
    # if (image1):
    #     article.image1 = image1
    # if (image2):
    #     article.image2 = image2
    # if (author):
    #     article.author = author


    return article


def fast_find_times(bs):
    try:
        publishedAt = bs.head.find(name='meta', attrs={"property": "og:pubdate"}).attrs['content']
        return publishedAt
    except:
        return ''

def find_times(bs):
    publishedAt = ""
    updatedAt = ""
    try:
        logger.debug("1")
        elements = bs.find_all('time')
        if (elements is not None) and (len(elements) > 0):
            publishedAt = elements[0]['datetime']
            updatedAt = elements[1]['datetime']
        else:
            published = bs.head.find(name='meta', attrs={"property": "article:published"})
            if (published is not None):
                logger.debug("1.1")
                publishedAt = bs.head.find(name='meta', attrs={"property": "article:published"}).attrs['content']
            if bs.head.find(name='meta', attrs={"property": "article:modified"}) is not None:
                logger.debug("1.2")
                updatedAt = bs.head.find(name='meta', attrs={"property": "article:modified"}).attrs['content']
    except:
        pass
    if (publishedAt=='' and updatedAt==''):
        try:
            publishedAt = bs.head.find(name='meta', attrs={"property": "og:pubdate"}).attrs['content']
            logger.debug("1.3")
            updatedAt = bs.html.find(lambda tag: tag.name == "time" and "datetime" in tag.attrs.keys()).attrs['datetime']
            #publishedAt = updatedAt
        except:
            pass
    if (publishedAt == ''):
        publishedAt = Utils.today()  #'2020-03-25T00:01:00+0200'
    if (updatedAt == ''):
        updatedAt = Utils.today() # '2020-03-25T00:01:00+0200'
    return publishedAt, updatedAt


def decide_include_article(publishTime):
    if (publishTime == ''):
        return True         # could not find publishedTime in HTML, so include it in results
    # minimalAllowedDateAsStr was already calculated in main()
    publishedDateAsStr = Utils.date_to_str(publishTime)
    logger.debug("publishedDateAsStr=%s minimalAllowedDateAsStr=%s", publishedDateAsStr, Utils.minimalAllowedDateAsStr)
    return (publishedDateAsStr >= Utils.minimalAllowedDateAsStr)

# <title>בלי אף שיעול, הקונצרט הראשון מאז ההסגר היה מעניין מתמיד - מוזיקה קלאסית - חדשות, ידיעות מהארץ והעולם - עיתון הארץ</title>
#
# <link rel="canonical" href="https://www.haaretz.co.il/gallery/music/classicalmusic/1.8941148" />
# <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
# <meta name="description" content="התזמורת הוקטנה, הקהל המצומצם עטה מסכות והמרווחים בין הנגנים הוציאו את &quot;אביב בהרי האפלצ'ים&quot; מהאיזון המוכר. ובכל זאת — קונצרט פוסט הקורונה הראשון של הפילהרמונית הציע חוויה טובה יותר מהמצופה"/>
#
# <meta name="twitter:card" content="summary_large_image">
# <meta name="twitter:site" content="@haaretz">
# <meta name="twitter:title" content="בלי אף שיעול, הקונצרט הראשון מאז ההסגר היה מעניין מתמיד"/>
# <meta name="twitter:description" content="התזמורת הוקטנה, הקהל המצומצם עטה מסכות והמרווחים בין הנגנים הוציאו את &quot;אביב בהרי האפלצ'ים&quot; מהאיזון המוכר. ובכל זאת — קונצרט פוסט הקורונה הראשון של הפילהרמונית הציע חוויה טובה יותר מהמצופה"/>
# <meta name="twitter:image" content="https://www.haaretz.co.il/polopoly_fs/1.8941145.1592901507!/image/2872796886.jpg_gen/derivatives/headline_1200x630/2872796886.jpg"/>
#
# <meta property="og:pubdate" content="2020-06-23T11:45:34+0300">
# <meta property="og:url" content="https://www.haaretz.co.il/gallery/music/classicalmusic/1.8941148" >
# <meta property="og:title" content="בלי אף שיעול, הקונצרט הראשון מאז ההסגר היה מעניין מתמיד" >
# <meta property="og:description"content="התזמורת הוקטנה, הקהל המצומצם עטה מסכות והמרווחים בין הנגנים הוציאו את &quot;אביב בהרי האפלצ'ים&quot; מהאיזון המוכר. ובכל זאת — קונצרט פוסט הקורונה הראשון של הפילהרמונית הציע חוויה טובה יותר מהמצופה" >
# <meta property="og:site_name"content="הארץ" >
# <meta property="og:type" content="article" >
# <meta property="og:image"content="https://www.haaretz.co.il/polopoly_fs/1.8941145.1592901507!/image/2872796886.jpg_gen/derivatives/headline_1200x630/2872796886.jpg" >
# <meta name="apple-itunes-app" content="app-id=521559643">
