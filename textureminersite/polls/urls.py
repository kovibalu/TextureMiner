from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       # ex: /polls/
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       # ex: /polls/refresh
                       url(r'^refresh$', views.refresh, name='refresh'),
                       # ex: /polls/5/
                       url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
                       # ex: /polls/5/results/
                       url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
)