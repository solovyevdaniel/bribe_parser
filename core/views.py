from django.shortcuts import render, render_to_response
import requests as rq


def index(request):
    newspapers = {
        'ukr_pravda': 'Українська правда',
        'espreso_tv': 'Еспресо.тв',
        '5_ua': '5 канал',
    }
    return render(request, 'main.html', {'newspapers': newspapers})


def details(request, newspaper):
    newspapers = {
        'ukr_pravda': 'http://www.pravda.com.ua/rss/view_news/',
        'espreso_tv': 'http://espreso.tv/rss',
        '5_ua': 'http://www.5.ua/novyny/rss/',
    }
    # if 404 or smthng else with rss, try
    return render_to_response('details.html')
