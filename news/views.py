from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from .models import Article, Category
from django.shortcuts import render
from django.views.generic import TemplateView

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

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(
            article_count=Count('article')
        ).order_by('name')
        context['current_category'] = self.request.GET.get('category', 'All')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

def home(request):
    return render(request, 'landing.html')

from django.shortcuts import render
from .models import Article  # If you have an Article model

def index(request):
    articles = Article.objects.all()
    return render(request, 'index.html', {'articles': articles})

from django.shortcuts import render, get_object_or_404
from .models import Article  # Make sure you have an Article model

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'article': article})

