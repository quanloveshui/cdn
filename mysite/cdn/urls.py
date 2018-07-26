from django.conf.urls import url
from cdn import views

app_name = 'cdn'

urlpatterns = [
    url(r'^data/', views.getdata, name='getdata'),
    url(r'^$', views.main, name='main'),
    url(r'^index/', views.index, name='index'),
    url(r'^check/', views.check, name='check'),
]
