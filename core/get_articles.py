# -*- coding: utf-8 -*-
import re
import lxml.html as html
import time
from random import randint

# regex_bribe = re.compile(r'([а-яії-]*хабар[а-яії-]*)', re.IGNORECASE)
regex_bribe = re.compile(r'на', re.IGNORECASE)
remove_script_1 = re.compile(r'\(function.*?deferIframeInit=.*\n.*', re.IGNORECASE)
remove_script_2 = re.compile(r'pagespeed.*?convertToIframe\(\);', re.IGNORECASE)
data = {
    'link': 'http://www.5.ua',
    'news_link': 'http://www.5.ua/novyny/?page=',
    'header':
        {
            'top': "//div[contains(@class, 'b-main-section-news--top__info cutter')]/span[contains(@class, 'caption')]/a/text()",
            'list': "//div[contains(@class, 'b-main-section-news-list--info cutter')]/span[contains(@class, 'caption')]/a/text()",

        },
    'url':
        {
            'top': "//div[contains(@class, 'b-main-section-news--top__info cutter')]/span[contains(@class, 'caption')]/a/@href",
            'list': "//div[contains(@class, 'b-main-section-news-list--info cutter')]/span[contains(@class, 'caption')]/a/@href",
        },
    'text':
        {
            'p': "//div[contains(@class, 'article-content')]/p",
            'p_body': "//div[contains(@class, 'article-content')]/div[contains(@class, 'body')]/p",
        },
    'date': "//span[contains(@class, 'article-date')]/text()"
    # todo: add category?
}


def scrap_text(article_page):
    # link = 'http://www.5.ua/suspilstvo/U-MVS-ozvuchyly-novi-dani-shchodo-chyselnosti-i-ozbroiennia-okupatsiinykh-viisk-na-Donbasi-108572.html'
    # article_page = html.parse(link)
    article_text = []
    p = article_page.xpath(data['text']['p'])
    p_body = article_page.xpath(data['text']['p_body'])
    for item in p:
        article_text.append(item.text_content())
    for item in p_body:
        article_text.append(item.text_content())
    text = ' '.join(article_text)
    text = re.sub(remove_script_1, '', text)
    text = re.sub(remove_script_2, '', text)
    return text


def get_pub_date(article_page):
    pub_date = article_page.xpath(data['date'])
    pub_date = pub_date[0].split(' |')
    return pub_date[0]


def parse_article_page(link_article):
    article_page = html.parse(link_article)
    pub_date = get_pub_date(article_page)
    text_article = scrap_text(article_page)
    return pub_date, text_article


def parse_news(articles, page, header_xpath, url_xpath):
    header_list = page.xpath(header_xpath)
    for header in header_list:
        header_list_bribe = re.findall(regex_bribe, str(header))
        if header_list_bribe:
            index = header_list.index(header)
            url_list = page.xpath(url_xpath)
            link_article = data['link'] + url_list[index]
            pub_date, text_article = parse_article_page(link_article)
            articles.append({
                'header': header,
                'url': link_article,
                'text': text_article,
                'pub_date': pub_date
            })
    return articles


def parse_5_ua():
    articles = []
    for i in range(1, 2):
        time.sleep(randint(0, 2))
        # todo: make check of response
        page = html.parse(data['news_link'] + str(i))

        # parse top news
        parse_news(articles, page=page, header_xpath=data['header']['top'], url_xpath=data['url']['top'])

        # parse list news
        parse_news(articles, page=page, header_xpath=data['header']['list'], url_xpath=data['url']['list'])
    return articles
