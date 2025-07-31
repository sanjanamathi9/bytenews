import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timezone

# New imports for summarization
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
from collections import Counter
import os
from gtts import gTTS
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# ✅ General function for all RSS sources (BBC, CNN, Reuters)
def fetch_news_from_rss(feed_url, source_name):
    articles_data = []

    try:
        response = requests.get(
            feed_url,
            headers={'User-Agent': 'ByteNewsScraper/1.0'},
            timeout=10
        )
        response.raise_for_status()

        feed = feedparser.parse(response.content)

        for entry in feed.entries:
            title = entry.title
            link = entry.link
            content = entry.get('summary', entry.get('description', 'No content available.'))

            published_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            elif hasattr(entry, 'published'):
                try:
                    published_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
                    published_date = published_date.replace(tzinfo=timezone.utc)
                except Exception:
                    published_date = None

            articles_data.append({
                'title': title,
                'link': link,
                'content': content,
                'publication_date': published_date,
                'source': source_name
            })

        return articles_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed from {source_name}: {e}")
        return []
    except Exception as e:
        print(f"An error occurred during RSS parsing for {source_name}: {e}")
        return []

# ✅ Improved summarization for Task 6
def generate_summary(text, article_title="", num_sentences=3):
    if not text or not isinstance(text, str):
        return "No content available to summarize."

    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text

    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    word_frequencies = Counter(filtered_words)

    # ✅ Boost title words
    if article_title:
        title_words = word_tokenize(article_title.lower())
        for word in title_words:
            if word.isalnum() and word not in stop_words:
                word_frequencies[word] += 0.5

    # ✅ Score sentences
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                sentence_scores[i] = sentence_scores.get(i, 0) + word_frequencies[word]

        # ✅ Bonus for first/second sentence
        if i == 0:
            sentence_scores[i] = sentence_scores.get(i, 0) + 1.0
        elif i == 1:
            sentence_scores[i] = sentence_scores.get(i, 0) + 0.5

    # ✅ Select top N sentences based on score
    top_sentence_indices = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    top_sentence_indices = sorted([i for i, _ in top_sentence_indices])

    final_summary = [sentences[i] for i in top_sentence_indices]
    return " ".join(final_summary)


def generate_audio_summary(text, article_id):
    if not text:
        logger.warning(f"No text provided for audio summary for article_id: {article_id}")
        return None

    # Create a unique filename
    filename = f"summary_{article_id}.mp3"

    # Define the full folder path: media/news_audio/
    audio_dir = os.path.join(settings.MEDIA_ROOT, 'news_audio')
    os.makedirs(audio_dir, exist_ok=True)  # ✅ Creates the folder if not present

    # Full path to save the audio file
    filepath = os.path.join(audio_dir, filename)

    try:
        # Generate and save the MP3 file
        tts = gTTS(text=text, lang='en')
        tts.save(filepath)
        logger.info(f"Generated audio summary for article {article_id} at {filepath}")

        # Return URL relative to MEDIA_URL (used for model FileField or templates)
        return os.path.join(settings.MEDIA_URL, 'news_audio', filename)

    except Exception as e:
        logger.error(f"Error generating audio for article {article_id}: {e}")
        return None


