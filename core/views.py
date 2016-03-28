# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from .get_data_from_rss import get_data_from_rss
from .get_info_from_article import article_processing
from .translate import translate
from .get_articles import parse_5_ua
from .models import Article
import time
import dateutil.parser as dp


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
    articles = parse_5_ua()
    for article in articles:
        # translate
        translated_article = translate(article['text'])
        translated_pub_date = translate(article['pub_date'])
        date = dp.parse(translated_pub_date)
        # save to Article
        art = Article(newspaper='5_ua', title=article['header'], link=article['url'], pub_date=date)
        art.save()
        # processing
        places, money = article_processing(translated_article)
        # save to Bribe
        if money:
            for item in money:
                art.bribe_set.create(place=places, money=item[0], currency=item[1])

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
