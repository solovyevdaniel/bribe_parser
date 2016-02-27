# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from .get_data_from_rss import get_data_from_rss
from .models import Article
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

