from django.urls import path
from icine import views
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

app_name = 'icine'


urlpatterns = [
	path('', views.index, name='icine-index'),
	path('about/', views.about, name='icine-about'),
	path('signup/',views.signup, name='icine-signup'),
	path('logout/',views.logout, name='icine-logout')

]+ static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
