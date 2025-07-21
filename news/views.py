from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.contrib import messages
from django.shortcuts import render
from .models import Article, Category,ReadingHistory
from django.views.generic import TemplateView
from django.views.generic import DetailView
from news.models import UserPreference

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from news.models import ReadingHistory
import logging
logger = logging.getLogger(__name__)


class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    ordering = ['-published_date']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category_name = self.request.GET.get('category')
        query = self.request.GET.get('q')

        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)

         # ✅ Apply search filter
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(summary__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()
        if self.request.user.is_authenticated:
            try:
                preferences = self.request.user.userpreference.preferred_categories.all()
                if preferences.exists():
                    queryset = queryset.filter(category__in=preferences).distinct()
                    messages.info(self.request, "Showing articles based on your preferences.")
                else:
                    messages.info(self.request, "No preferences set. Showing all articles.")
            except UserPreference.DoesNotExist:
                messages.info(self.request, "No preferences found. Showing all articles.")

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['categories'] = Category.objects.annotate(article_count=Count('article')).order_by('name')
        context['current_category'] = self.request.GET.get('category', 'All')
        context['query'] = self.request.GET.get('q', '')
        context['recommendations'] = []


        if self.request.user.is_authenticated:
            try:
                prefs = self.request.user.userpreference.preferred_categories.all()
                read_ids = ReadingHistory.objects.filter(
                    user=self.request.user
                ).values_list('article__id', flat=True)

                if prefs.exists():
                    recommendations = Article.objects.filter(
                        category__in=prefs
                    ).exclude(id__in=read_ids).order_by('-published_date')[:5]
                    context['recommendations'] = recommendations
            except UserPreference.DoesNotExist:
                pass

        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_authenticated:
            ReadingHistory.objects.get_or_create(user=self.request.user, article=obj)
        return obj

class HomePageView(TemplateView):
    template_name = 'news/homepage.html'


def landing_page(request):
    return render(request, 'landing.html')


@login_required
def reading_history(request):
    history = ReadingHistory.objects.filter(
        user=request.user
    ).select_related('article').order_by('-read_at')
    return render(request, 'news/reading_history.html', {'history': history})