# -*- coding: utf-8 -*-
import re
import lxml.html as html
import requests
import time
from random import randint

# regex_bribe = re.compile(r'([а-яії-]*хабар[а-яії-]*)', re.IGNORECASE)
regex_bribe = re.compile(r'на', re.IGNORECASE)

data = {
    'link': 'http://www.5.ua',
    'news_link': 'http://www.5.ua/novyny/?page=',
    'header':
        {
            'top': "//div[contains(@class, 'b-main-section-news--top__info cutter')]/span[contains(@class, 'caption')]/a",
            'list': "//div[contains(@class, 'b-main-section-news-list--info cutter')]/span[contains(@class, 'caption')]/a",

        },
    'url':
        {
            'top': "//div[contains(@class, 'b-main-section-news--top__info cutter')]/span[contains(@class, 'caption')]/a/@href",
            'list': "//div[contains(@class, 'b-main-section-news-list--info cutter')]/span[contains(@class, 'caption')]/a/@href",
        },
    'text':
        {
            'p': "//div[contains(@class, 'article-content')]/p",
            'p_style': "//div[contains(@class, 'article-content')]/p[contains(@style, 'text-align:center;')]",
            'p_script': "//div[contains(@class, 'article-content')]/p/script",
        },
    'date': "//span[contains(@class, 'article-date')]/text()"

    # todo: add category?

}


def scrap_text(article_page):
    article_text = []
    p = article_page.xpath(data['text']['p'])
    p_style = article_page.xpath(data['text']['p_style'])
    p_script = article_page.xpath(data['text']['p_script'])

    for p_item in p:
        if p_style or p_script:
            if p_style:
                for p_style_item in p_style:
                    if p_item.text_content() not in p_style_item.text_content():
                        article_text.append(p_item.text_content())
            if p_script:
                for p_script_item in p_script:
                    if p_item.text_content() not in p_script_item.text_content():
                        article_text.append(p_item.text_content())
        else:
            article_text.append(p_item.text_content())

    return ' '.join(article_text)


def get_pub_date(page):
    pub_date = page.xpath(data['date'])
    pub_date = pub_date[0].split('\xa0\xa0')
    return ' '.join(pub_date)


def parse_5_ua():
    article = {}
    # todo: if you want get all the articles, you must stop when texts/htmls of responses will be the same. Use loop while. lol))
    for i in range(1, 2):
        time.sleep(randint(0, 2))
        page = html.parse(data['news_link'] + str(i))  # todo: make check of response

        header_top = page.xpath(data['header']['top'] + '/text()')
        header_top_bribe = re.findall(regex_bribe, header_top[0])
        if header_top_bribe:
            pub_date = get_pub_date(page)
            url_top = page.xpath(data['url']['top'])
            link_article = data['link'] + url_top[0]
            article_page = html.parse(link_article)
            article_text = scrap_text(article_page)

            article['url'] = link_article
            article['text'] = article_text
            article['pub_date'] = pub_date

            articles.append(article)
        header_list = page.xpath(data['header']['list'] + '/text()')

        for header in header_list:
            header_list_bribe = re.findall(regex_bribe, str(header))
            if header_list_bribe:
                pub_date = get_pub_date(page)
                url_list = page.xpath(data['url']['list'])
                link_article = data['link'] + url_list[0]
                article_page = html.parse(link_article)
                article_text = scrap_text(article_page)

                article['url'] = link_article
                article['text'] = article_text
                article['pub_date'] = pub_date
                articles.append(article)

articles = []
parse_5_ua()

for item in articles:
    for key, value in item.items():
        print(key, ' ', value)
        print('____________________')
