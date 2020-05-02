from django.conf.urls import url
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    url(r'^recommend', views.QuoteTodayView.as_view(), name='recommend')
]

urlpatterns += staticfiles_urlpatterns()