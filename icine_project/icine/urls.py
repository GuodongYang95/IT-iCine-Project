from django.urls import path
from icine import views
from django.conf.urls import url

app_name = 'icine'

urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('about/', views.AboutView.as_view(),name='about'),
	path('category/<slug:category_name_slug>/',views.show_category, name='show_category'),
	path('goto/', views.GoToView.as_view(), name='goto'),
    path('register_profile/', views.RegisterProfileView.as_view(), name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profiles/', views.ListProfilesView.as_view(), name='list_profiles'),
	path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),
	path('suggest/', views.CategorySuggestionView.as_view(), name='suggest'),
]
