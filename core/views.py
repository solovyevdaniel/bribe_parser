# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from .get_data_from_rss import get_data_from_rss
from .models import Article


def index(request):
    newspapers = {
        'ukr_pravda': 'Українська правда',
        'espreso_tv': 'Еспресо.тв',
        '5_ua': '5 канал',
    }
    return render_to_response('main.html', {'newspapers': newspapers})


def details(request, newspaper):
    data = get_data_from_rss(newspaper)
    if data is not []:
        for item in data:
            title, link, pub_date = item
            #todo if exist in db
            article = Article(newspaper=newspaper, title=title, link=link, pub_date=pub_date)
            article.save()
            return render_to_response('details.html', {'data': data})
    else:
        return render_to_response('details.html', {'data': 'smth ne OK!!!!!!!!'})

