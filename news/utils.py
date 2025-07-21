import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timezone


def fetch_bbc_news_rss():
    BBC_RSS_FEED_URL = "https://feeds.bbci.co.uk/news/rss.xml"
    articles_data = []

    try:
        # Make HTTP request to BBC feed
        response = requests.get(
            BBC_RSS_FEED_URL,
            headers={'User-Agent': 'ByteNewsScraper/1.0'},
            timeout=10
        )
        response.raise_for_status()  # Raise error for bad HTTP status

        # Parse RSS feed content
        feed = feedparser.parse(response.content)

        for entry in feed.entries:
            title = entry.title
            link = entry.link

            # Use summary or description for content
            content = entry.get('summary', entry.get('description', 'No content available.'))

            # Try parsing published date
            published_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            elif hasattr(entry, 'published'):
                try:
                    published_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
                    published_date = published_date.replace(tzinfo=timezone.utc)
                except Exception:
                    published_date = None

            # Append article dictionary
            articles_data.append({
                'title': title,
                'link': link,
                'content': content,
                'publication_date': published_date,
                'source': 'BBC News'
            })


        return articles_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed from BBC News: {e}")
        return []
    except Exception as e:
        print(f"An error occurred during RSS parsing: {e}")
        return []