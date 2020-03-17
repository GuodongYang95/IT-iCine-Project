from django.urls import path
from .views import( PostListView, 
	PostDetailView, 
	PostCreateView,
	PostUpdateView,
	PostDeleteView
)
from icine import views
from django.conf.urls import url
from django.contrib import admin

app_name = 'icine'


urlpatterns = [
	path('', views.index, name='index'),
	path('about/', views.about, name='about'),
	path('blog/', PostListView.as_view(), name='blog'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='postDetail'),
	path('post/new/', PostCreateView.as_view(), name='postCreate'),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name='postUpdate'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='postDelete'),
	
]

