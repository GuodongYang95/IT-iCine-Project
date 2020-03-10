from django.urls import path
from icine import views
from django.conf.urls import url

app_name = 'icine'


urlpatterns = [
	path('', views.index, name='icine-index'),
	path('about/', views.about, name='icine-about'),
]
