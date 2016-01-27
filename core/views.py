# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from .get_data_from_rss import get_data_from_rss


def index(request):
    newspapers = {
        'ukr_pravda': 'Українська правда',
        'espreso_tv': 'Еспресо.тв',
        '5_ua': '5 канал',
    }
    return render(request, 'main.html', {'newspapers': newspapers})


def details(request, newspaper):
    f = get_data_from_rss(newspaper)
    return render_to_response('details.html')
