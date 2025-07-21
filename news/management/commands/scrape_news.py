# news/management/commands/scrape_news.py
from django.core.management.base import BaseCommand
from news.utils import fetch_bbc_news_rss
from news.models import Article, Category

class Command(BaseCommand):
    help = 'Scrapes news articles from BBC RSS feed and saves them to the database.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting news scraping...")

        articles_data = fetch_bbc_news_rss()

        if not articles_data:
            self.stdout.write(self.style.WARNING("No articles fetched. Check the scraper."))
            return

        articles_added = 0
        general_category, _ = Category.objects.get_or_create(name='General')

        for article_data in articles_data:
            if not Article.objects.filter(title=article_data['title']).exists():
                article = Article.objects.create(
                    title=article_data['title'],
                    content=article_data['content'],
                    link=article_data['link'],
                    publication_date=article_data['publication_date'],
                    author=article_data['source'],
                    category=general_category  # ✅ assign required category
                )
                articles_added += 1

        self.stdout.write(self.style.SUCCESS(f"Finished scraping. Added {articles_added} new articles."))