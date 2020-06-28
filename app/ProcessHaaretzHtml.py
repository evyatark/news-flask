import logging
from bs4 import BeautifulSoup



logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




def omit(tag):
    omitted = BeautifulSoup("<div>omitted " + tag + "</div>", "html.parser")
    return omitted


def remove_parts_of_article(section, parts):
    for part in parts:
        logger.debug("2")
        while section.find(class_=part) is not None:
            section.find(class_=part).replace_with(omit(part))


'''
get an HTML of Haaretz article, and strips some parts from it,
so it will be possible and easier to read all of it.
args:
    bs - BeautifulSoup model of the original HTML
return: htmlText, or empty string if failed
'''
def strip_content(bs):
    sections = bs.article.findAll(name='section', class_='b-entry')
    if (sections is None) or len(sections) == 0:
        return ''
    first = sections[0]

    remove_parts_of_article(first, ['c-quick-nl-reg', 'c-related-article-text-only-wrapper', 'c-dfp-ad'])

    # remove images TODO fix
    while (first.find(name='figure') is not None):
        first.find(name='figure').replace_with(omit('figure'))

    bs.html.find(name='div',attrs={"hidden":""}).replace_with(omit('hidden'))
    bs.html.find(attrs={"id":"amp-web-push"}).replace_with(omit('amp-web-push'))
    remove_parts_of_article(bs.html, ['amp-sidebar'])

    while (bs.html.find(name='div', attrs={"class":"delayHeight"}) is not None):
        bs.html.find(name='div', attrs={"class": "delayHeight"}).replace_with(omit("delayHeight"))

    # fix document - set some <section amp-access="TRUE"> to bypass paywall
    list_of_sections = bs.html.findAll(
        lambda tag: tag.name == "section" and "amp-access" in tag.attrs.keys() and tag.attrs['amp-access'] != "TRUE")
    for section in list_of_sections:
        logger.debug(".", end='')
        section.attrs['amp-access'] = "TRUE"

    # fix document - style page so it is convenient to read
    bs.html.body.attrs['style'] = "border:2px solid"
    # assuming that 3rd child of <head> is not needed and can be changed...
    bs.html.head.contents[3].attrs={"name":"viewport","content":"width=device-width, initial-scale=1"}

    htmlText = bs.html.prettify()
    return htmlText




