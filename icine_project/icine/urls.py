from django.urls import path
from icine import views
from django.conf.urls import url

app_name = 'icine'


urlpatterns = [
	path('', views.IndexView.as_view(), name='icine-index'),
	path('about/', views.AboutView.as_view(),name='icine-about'),
	path('category/<slug:category_name_slug>/',views.ShowCategoryView.as_view(), name='show_category'),
]
