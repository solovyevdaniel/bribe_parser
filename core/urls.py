from django.conf.urls import url
from . import views

app_name = 'core'
urlpatterns = [
    url(r'^(?P<newspaper>[\w]*)/$', views.details, name='details'),
    url(r'^$', views.index, name='index'),
]