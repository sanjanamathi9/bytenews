from django.urls import path
from .views import ArticleListView, ArticleDetailView
from . import views


urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),  # ✅ This name='home' must exist!
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('history/', views.reading_history, name='reading_history'),
    # news/urls.py
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),

]