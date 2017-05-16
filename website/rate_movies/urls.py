from django.conf.urls import url

#remember current dir is package
from . import views 

urlpatterns = [
    url(r'^$', views.index,name='index'),
]