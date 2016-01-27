# -*- coding: utf-8 -*-
from lxml import etree
import re
import requests


def get_xml(link):
    r = requests.get(link)
    #todo if 404 or smthng else with rss
    xml_string = r.content
    return etree.XML(xml_string)


def get_articles(root):
    find_text = etree.XPath("/rss/channel/item/title/text()")
    titles = find_text(root)

    regex_bribe = re.compile(r'([а-яії-]*хабар[а-яії-]*)', re.IGNORECASE)

    indexes_title = []
    for title in titles:
        if re.search(regex_bribe, title):
            # print('regex result:', re.search(regex_bribe, title))
            indexes_title.append(titles.index(title))
        else:
            #todo if return None
            pass
    # print(indexes_title)

    for item in indexes_title:
        # print(item)

        find_text2 = etree.XPath('/rss/channel/item[' + str(item + 1) + ']/link/text()')
        # print(find_text2(root))

        find_text3 = etree.XPath('/rss/channel/item[' + str(item + 1) + ']/description/text()')
        # print(find_text3(root))


def get_data_from_rss(link):
    newspapers = {
        'ukr_pravda': 'http://www.pravda.com.ua/rss/view_news/',
        'espreso_tv': 'http://espreso.tv/rss',
        '5_ua': 'http://www.5.ua/novyny/rss/',
    }

    if link in newspapers.keys():
        #todo if None
        xml = get_xml(newspapers[link])
        articles = get_articles(xml)
