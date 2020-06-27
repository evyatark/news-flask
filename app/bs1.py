import logging
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



'''
++++++++
+++
+++ Public API
+++
+++
'''
def process_all():
    #list_of_urls = urls()
    for url in urls():
        more_article_ids = process_page(url, 1000)
        return more_article_ids
'''
+++
++++++++
'''




def urls():
    return [
     'https://www.haaretz.co.il'
    ,'https://www.haaretz.co.il/news'
    , 'https://www.themarker.com/allnews'
    ,'https://www.haaretz.co.il/sport'
    ,'https://www.haaretz.co.il/magazine'
    , 'https://www.themarker.com/wallstreet'
    , 'https://www.themarker.com/misc/all-headlines'
    , 'https://www.themarker.com/realestate'
    , 'https://www.themarker.com/technation'
    , 'https://www.themarker.com/magazine'
    ,'https://www.haaretz.co.il/news/elections'
    ,'https://www.haaretz.co.il/news/world'
    ,'https://www.haaretz.co.il/news/education'
    ,'https://www.haaretz.co.il/news/politics'
    ,'https://www.haaretz.co.il/news/law'
    ,'https://www.haaretz.co.il/news/health'
    ,'https://www.haaretz.co.il/news/local'
    ,'https://www.haaretz.co.il/gallery'
    ,'https://www.haaretz.co.il/gallery/television'
    , 'https://www.haaretz.co.il/gallery/architecture'
    , 'https://www.haaretz.co.il/gallery/fashion'
    , 'https://www.haaretz.co.il/gallery/art'
    , 'https://www.haaretz.co.il/gallery/events'
    , 'https://www.haaretz.co.il/gallery/music'
    , 'https://www.haaretz.co.il/gallery/cinema'
    , 'https://www.haaretz.co.il/gallery/theater'
    , 'https://www.haaretz.co.il/gallery/night-life'
    ,'https://www.haaretz.co.il/opinions'
    ,'https://www.haaretz.co.il/captain'
    , 'https://www.haaretz.co.il/captain/net'
    , 'https://www.haaretz.co.il/captain/viral'
    , 'https://www.haaretz.co.il/captain/gadget'
    , 'https://www.haaretz.co.il/captain/software'
    , 'https://www.haaretz.co.il/captain/games'
    , 'https://www.haaretz.co.il/science'
    , 'https://www.haaretz.co.il/literature'
    , 'https://www.haaretz.co.il/blogs'
    , 'https://www.haaretz.co.il/nature'
    , 'https://www.haaretz.co.il/travel'
    , 'https://www.haaretz.co.il/misc/all-headlines'

        'https://www.haaretz.co.il/binge'
       ]

def is_link(link):
    return (link.find("1.8") >= 0)

def start_link(link):
    return link.find("1.8")



def process_page(url, limit):
    logger.info("loading url %s...", url)
    try:
        user_agent = 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        request = Request(url, headers={'User-Agent': user_agent})
        response = urlopen(request)
        html = response.read()
    except:
        logger.error("some exception when trying to retrieve URL %s", url)
        return []
    logger.debug("souping...")
    bs = BeautifulSoup(html, 'html.parser')
    list_of_articles = bs.html.find_all(
        lambda tag: (tag.name == "a") and
                    ('href' in tag.attrs.keys()) and
                    (is_link(tag.attrs['href'])), recursive=True)
    links = {"1"}   # links is a set. but links = {} creates it as a dict! ???
    for href in list_of_articles:
        link = href.attrs["href"]
        if is_link(link):
            links.add(link)
            limit = limit - 1
            if (limit <= 0):
                break
    links.remove("1")
    relativeHrefs = list(links)
    return relativeHrefs
    # linkes is a set (not list!) of relative URLs (such as '/food/sweets/1.8910277')
    #print("links:")
    # ids = []
    # for link in links:
    #     #print(link)
    #     if is_link(link):
    #         start = start_link(link)
    #         id = link[start:]
    #         ids.append(id)
    # for id in ids:
    #     logger.debug(id)
    # return ids

