from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q, Count
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect  # ✅ fixed order
from django.contrib.auth.decorators import login_required
from django.urls import reverse  # ✅ moved to top
import logging

from .models import Article, Category, ReadingHistory, UserPreference
from .utils import generate_summary  # ✅ for summarization
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from .models import Article
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import SummaryFeedback


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

        if self.request.user.is_authenticated:
            try:
                preferences = self.request.user.userpreference.preferred_categories.all()
                if preferences.exists():
                    queryset = queryset.filter(categories__in=preferences)
                    messages.info(self.request, "Showing articles based on your preferences.")
                else:
                    messages.info(self.request, "No preferences set. Showing all articles.")
            except UserPreference.DoesNotExist:
                messages.info(self.request, "No preferences found. Showing all articles.")

        if category_name:
            queryset = queryset.filter(categories__name__iexact=category_name)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(summary__icontains=query) |
                Q(categories__name__icontains=query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(article_count=Count('article'))
        context['current_category'] = self.request.GET.get('category', '')
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
                        categories__in=prefs
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

        # ✅ Save to reading history
        if self.request.user.is_authenticated:
            ReadingHistory.objects.get_or_create(user=self.request.user, article=obj)

        # ✅ Auto-generate summary if it's missing
        if not obj.summary and obj.content:
            try:
                obj.summary = generate_summary(obj.content, num_sentences=3)
                obj.save()
            except Exception as e:
                logger.error(f"Error generating summary: {e}")

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


# ✅ Step 1: Manual summary generation view (for Task 5)


@login_required
def generate_article_summary(request, pk):
    article = get_object_or_404(Article, pk=pk)

    # ❌ this is wrong
    # summary = generate_summary(article.content, article.title, 3)

    # ✅ this is correct
    try:
        num_sentences = int(request.GET.get('num_sentences', 3))
        num_sentences = max(1, min(num_sentences, 10))
    except (ValueError, TypeError):
        num_sentences = 3

    summary = generate_summary(article.content, article.title, num_sentences)

    article.summary = summary
    article.save()

    return redirect('detail', pk=article.pk)


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'news/article_detail.html', {'article': article})

@login_required
@require_POST
def submit_summary_feedback(request, pk):
    article = get_object_or_404(Article, pk=pk)
    is_helpful = request.POST.get('is_helpful')

    if is_helpful is not None:
        is_helpful_bool = (is_helpful.lower() == 'true')

        feedback, created = SummaryFeedback.objects.update_or_create(
            user=request.user,
            article=article,
            defaults={'is_helpful': is_helpful_bool}
        )

        messages.success(request, 'Thank you for your feedback!')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'helpful': is_helpful_bool})
        else:
            return redirect('detail', pk=pk)

    messages.error(request, 'Invalid feedback provided.')
    return redirect('detail', pk=pk)

