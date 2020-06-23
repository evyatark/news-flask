


def rest_of_processing():
    remove_parts_of_article(first, ['c-quick-nl-reg', 'c-related-article-text-only-wrapper', 'c-dfp-ad'])
    # logger.debug("2")
    # if first.find(class_='c-quick-nl-reg') is not None:
    #     first.find(class_='c-quick-nl-reg').replace_with(omit('c-quick-nl-reg'))
    # logger.debug("3")
    # if first.find(class_='c-related-article-text-only-wrapper') is not None:
    #     first.find(class_='c-related-article-text-only-wrapper').replace_with(omit('c-related-article-text-only-wrapper'))
    logger.debug("4")
    all_figures = first.find_all(name='figure')
    # while (len(all_figures) > 0):
    #     first.find(name='figure').replace_with(omit('figure'))
    #     all_figures = first.find_all(name='figure')
    while (first.find(name='figure') is not None):
        first.find(name='figure').replace_with(omit('figure'))

    # logger.debug("5")
    # while (first.find(class_="c-dfp-ad") is not None):
    #     first.find(class_="c-dfp-ad").replace_with(omit("c-dfp-ad"))

    logger.debug("6")
    bs.html.find(name='div',attrs={"hidden":""}).replace_with(omit('hidden'))
    bs.html.find(attrs={"id":"amp-web-push"}).replace_with(omit('amp-web-push'))
    #bs.html.find(name='section',attrs={"amp-access":"TRUE"}).replace_with(omit('amp-access'))
    # logger.debug("7")
    # bs.html.find(name='amp-sidebar').replace_with(omit('amp-sidebar'))
    remove_parts_of_article(bs.html, ['amp-sidebar'])
    while (bs.html.find(name='div', attrs={"class":"delayHeight"}) is not None):
        bs.html.find(name='div', attrs={"class": "delayHeight"}).replace_with(omit("delayHeight"))

# convert every <section amp-access="NOT ampConf.activation OR currentViews &lt; ampConf.maxViews OR subscriber">
# to     <section amp-access="TRUE">
    logger.debug("8")
    list_of_sections = bs.html.findAll(
        lambda tag: tag.name == "section" and "amp-access" in tag.attrs.keys() and tag.attrs['amp-access'] != "TRUE")
    for section in list_of_sections:
        logger.debug(".", end='')
        section.attrs['amp-access'] = "TRUE"

    logger.debug("9")
    bs.html.body.attrs['style'] = "border:2px solid"
    # assuming that 3rd child of <head> is not needed and can be changed...
    bs.html.head.contents[3].attrs={"name":"viewport","content":"width=device-width, initial-scale=1"}
    htmlText=bs.html.prettify()
    logger.debug('[%s] processing completed in %s seconds', id, time() - ts)
    logger.debug("!")
    return Article(id, header, publishedAt, updatedAt, htmlText, subject, sub_subject)


