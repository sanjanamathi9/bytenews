from django.urls import path
from .views import ArticleListView, ArticleDetailView, generate_article_summary
from . import views

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<int:pk>/generate-summary/', generate_article_summary, name='generate_summary'),
    path('history/', views.reading_history, name='reading_history'),
    path('<int:pk>/', views.article_detail, name='detail'),
    path('article/<int:pk>/feedback/', views.submit_summary_feedback, name='submit_summary_feedback'),

]
