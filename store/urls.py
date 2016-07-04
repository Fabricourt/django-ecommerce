from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /store/
    url(r'^$', views.index, name='index'),
    # ex: /store/5/
    url(r'^(?P<product_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /store/5/results/
    url(r'^(?P<product_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /store/5/vote/
    url(r'^(?P<product_id>[0-9]+)/vote/$', views.vote, name='vote'),
]