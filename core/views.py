# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from .get_data_from_rss import get_data_from_rss
from .get_info_from_article import article_processing
from .translate_article import translate_article
from .get_articles import get_articles
from .models import Article, Bribe
import time


def index(request):
    newspapers = {
        'ukr_pravda': 'Українська правда',
        'espreso_tv': 'Еспресо.тв',
        '5_ua': '5 канал',
        '112_ua': '112.ua',
        'unian': 'Уніан.net',
    }
    return render_to_response('main.html', {'newspapers': newspapers})


def parse(request):
    start_time = time.time()
    newspapers = {
        '5_ua':
            {
                'link': 'http://www.5.ua/novyny/?page=',
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
            },
    }
    result = get_articles(newspapers)
    return render_to_response('main.html', {'end': 'the end. Time is ' + str(time.time() - start_time) + ' seconds'})


def details(request, newspaper):
    data = get_data_from_rss(newspaper)
    if data is not []:
        for item in data:
            title, link, pub_date = item
            check_article = Article.objects.filter(newspaper=newspaper, title=title, pub_date=pub_date).exists()
            if not check_article:
                article = Article(newspaper=newspaper, title=title, link=link, pub_date=pub_date)
                article.save()

    articles_by_newspaper = Article.objects.filter(newspaper=newspaper)
    if not articles_by_newspaper:
        articles_by_newspaper = None
    return render_to_response('details.html', {'articles': articles_by_newspaper})
