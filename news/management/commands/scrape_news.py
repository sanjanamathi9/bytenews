from django.core.management.base import BaseCommand
from news.utils import fetch_news_from_rss, generate_summary  # ✅ Import generate_summary
from news.models import Article, Category
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Scrapes news articles from multiple RSS feeds and saves them.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting multi-source news scraping...")

        # ✅ Define multiple sources
        NEWS_SOURCES = {
            'BBC News': "https://feeds.bbci.co.uk/news/rss.xml",
            'CNN': "http://rss.cnn.com/rss/cnn_topstories.rss",
            'Reuters': "http://feeds.reuters.com/reuters/topNews",
        }

        total_articles_added = 0
        general_category, _ = Category.objects.get_or_create(name='General')

        for source_name, feed_url in NEWS_SOURCES.items():
            self.stdout.write(f"Fetching from {source_name}...")
            logger.info(f"Fetching from {source_name}...")

            articles_data = fetch_news_from_rss(feed_url, source_name)

            if not articles_data:
                self.stdout.write(self.style.WARNING(f"No articles fetched from {source_name}."))
                continue

            articles_added_from_source = 0
            for article_data in articles_data:
                try:
                    # ✅ Check for duplicate by URL
                    if not Article.objects.filter(link=article_data['link']).exists():
                        # ✅ Generate summary using article content
                        article_summary = generate_summary(article_data['content'], article_data['title'], num_sentences=5)  

                        # ✅ Create article with summary field included
                        article = Article.objects.create(
                            title=article_data['title'],
                            content=article_data['content'],
                            publication_date=article_data['publication_date'],
                            author=article_data.get('source', 'Unknown'),
                            link=article_data['link'],
                            source=article_data['source'],
                            summary=article_summary  # ✅ Save generated summary
                        )
                        article.categories.add(general_category)
                        articles_added_from_source += 1
                    else:
                        logger.info(f"Duplicate skipped: {article_data['title']}")
                except Exception as e:
                    logger.error(f"Error saving article: {e} - {article_data.get('title', 'N/A')}")

            total_articles_added += articles_added_from_source
            self.stdout.write(self.style.SUCCESS(f"Added {articles_added_from_source} new articles from {source_name}."))

        self.stdout.write(self.style.SUCCESS(f"✅ Finished multi-source scraping. Total new articles: {total_articles_added}."))
        logger.info(f"✅ Finished multi-source scraping. Total new articles: {total_articles_added}.")
