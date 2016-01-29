# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from .get_data_from_rss import get_data_from_rss
from .models import Article
from collections import OrderedDict


def index(request):
    newspapers = OrderedDict({
        'ukr_pravda': 'Українська правда',
        'espreso_tv': 'Еспресо.тв',
        '5_ua': '5 канал',
    })
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

    all_articles = Article.objects.filter(newspaper=newspaper)
    # todo дичь какая-то
    if all_articles is []:
        all_articles = 'Нет ни одной статьи!'
    return render_to_response('details.html', {'data': all_articles})

