from django.urls import path
from icine import views


urlpatterns = [
	path('', views.index, name='icine-index'),
	path('about/', views.about, name='icine-about'),
]
