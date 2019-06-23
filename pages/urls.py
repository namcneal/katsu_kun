from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
	path('', views.home, name='home'),
    path('select/', views.select, name='select'),
    path('play/', views.play, name='play'),
    path('about/', views.about, name='about')
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
