# -*- coding: utf-8 -*-
from lxml import etree
import re
import requests
from datetime import datetime


def get_xml(link):
    r = requests.get(link)
    if r.status_code == requests.codes.ok:
        xml_string = r.content
        return etree.XML(xml_string)
    else:
        return None


def get_articles(root):
    find_text = etree.XPath("/rss/channel/item/title/text()")
    titles = find_text(root)

    # todo add "корупція/корумпований" and other regex
    regex_bribe = re.compile(r'([а-яії-]*хабар[а-яії-]*)', re.IGNORECASE)
    # regex_bribe = re.compile(r'Україн[\w]*', re.IGNORECASE)

    articles = []
    for title in titles:
        result_re = re.search(regex_bribe, title)
        if result_re:
            title_index = titles.index(title)

            # get link
            link = etree.XPath('/rss/channel/item[' + str(title_index + 1) + ']/pdalink/text()')
            if not link(root):
                link = etree.XPath('/rss/channel/item[' + str(title_index + 1) + ']/link/text()')

            # get date
            date = etree.XPath('/rss/channel/item[' + str(title_index + 1) + ']/pubDate/text()')
            date = datetime.strptime(date(root)[0], "%a, %d %b %Y %H:%M:%S %z")

            articles.append([title, link(root)[0], date])
    return articles


def get_data_from_rss(link):
    newspapers = {
        'ukr_pravda': 'http://www.pravda.com.ua/rss/view_news/',
        'espreso_tv': 'http://espreso.tv/rss',
        '5_ua': 'http://www.5.ua/novyny/rss/',
    }

    if link in newspapers.keys():
        xml = get_xml(newspapers[link])
        if xml is not None:
            return get_articles(xml)
        else:
            return None
