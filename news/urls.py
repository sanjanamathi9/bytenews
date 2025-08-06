from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    generate_article_summary,
    generate_audio_view,  # You already have this
)
from . import views



urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<int:pk>/generate-summary/', generate_article_summary, name='generate_summary'),
    path('history/', views.reading_history, name='reading_history'),
    path('<int:pk>/', views.article_detail, name='detail'),
    path('article/<int:pk>/feedback/', views.submit_summary_feedback, name='submit_summary_feedback'),
    path('articles/<int:pk>/generate-audio/', generate_audio_view, name='generate_audio'),

    # ✅ NEW: AJAX endpoint (do not rename, used in JS)
    path('<int:pk>/generate-audio-ajax/', views.generate_audio_ajax, name='generate_audio_ajax'),
]
