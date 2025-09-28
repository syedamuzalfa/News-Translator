# newsapp/utils.py

import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import re
from datetime import datetime, date
from django.utils.timezone import now
from dateutil import parser

# Base sections
SECTIONS = {
    "Editorial": "https://www.dawn.com/newspaper/editorial",
    "Opinion": "https://www.dawn.com/newspaper/column",
}

# Default headers
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

translator = Translator()


# ---------------------------------------------------------------------
# Safe request
# ---------------------------------------------------------------------
def safe_request(url, headers=None, timeout=10):
    """Fetch a page safely with retry on 403."""
    if headers is None:
        headers = HEADERS

    try:
        response = requests.get(url, headers=headers, timeout=timeout)

        if response.status_code == 403:
            # Retry with alternate headers (Safari)
            alt_headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "Version/17.0 Safari/605.1.15"
                ),
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/",
            }
            response = requests.get(url, headers=alt_headers, timeout=timeout)

        if response.status_code != 200:
            print(f"⛔ Skipping {url}, HTTP {response.status_code}")
            return None

        return response

    except requests.RequestException as e:
        print(f"⛔ Error fetching {url}: {e}")
        return None


# ---------------------------------------------------------------------
# Collect article links
# ---------------------------------------------------------------------
def get_article_links(base_url, max_pages=1):
    """Fetch article links from Dawn with pagination (default 1 page)."""
    all_links = set()

    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}" if page > 1 else base_url
        response = safe_request(url)
        if not response:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article")

        page_links = [a.find("a")["href"] for a in articles if a.find("a")]
        if not page_links:
            break  # stop if no more articles

        all_links.update(page_links)

    return list(all_links)


# ---------------------------------------------------------------------
# Date cleaning and recency detection
# ---------------------------------------------------------------------
def clean_date_text(raw_text: str) -> str:
    """Normalize date text by removing extra prefixes."""
    raw = raw_text.strip().lower()
    raw = re.sub(r"published\s*", "", raw)  # remove "Published" prefix
    raw = re.sub(r"(\d{4})(\d{1,2}:\d{2}[ap]m)", r"\1 \2", raw)
    return raw


def is_recent_article(date_text: str) -> bool:
    """
    Returns True if:
    - published 'hours/minutes ago'
    - OR absolute date == today
    """
    if not date_text:
        return False

    text = clean_date_text(date_text)

    # Case A: Relative times
    if any(x in text for x in ["hour ago", "hours ago", "minute ago", "minutes ago"]):
        return True

    # Case B: Absolute date with time
    try:
        parsed_date = parser.parse(text, fuzzy=True).date()
        return parsed_date == date.today()
    except Exception:
        return False


def log_article_status(url: str, date_text: str):
    """Helper for pretty logging"""
    if is_recent_article(date_text):
        print(f"✅ Keeping {url}, published '{date_text}' (today/recent)")
    else:
        print(f"⏩ Skipping {url}, published '{date_text}' (not recent)")


# ---------------------------------------------------------------------
# Article content
# ---------------------------------------------------------------------
def get_article_content(url):
    response = safe_request(url)
    if not response:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Title (fallback to h1 if h2 missing)
    title_tag = soup.find("h2", class_="story__title") or soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "No Title"

    # Content
    story_div = soup.find("div", class_="story__content")
    content = (
        "\n".join(p.get_text(strip=True) for p in story_div.find_all("p"))
        if story_div
        else ""
    )

    # Timestamp: try multiple selectors
    date_tag = (
        soup.find("span", class_="timestamp--time")
        or soup.find("span", class_="story__time")
        or soup.find("span", class_="timestamp")
    )

    if not date_tag:
        print(f"⚠️ No timestamp found for {url}")
        return None

    date_text = clean_date_text(date_tag.get_text(strip=True))
    today = now().date()
    publish_date = None

    # Relative times
    if any(x in date_text for x in ["minute", "hour"]):
        publish_date = today
        print(f"✅ Keeping {url}, published '{date_text}' (recent)")
    else:
        # Absolute date
        if is_recent_article(date_text):
            publish_date = today
            print(f"✅ Keeping {url}, published '{date_text}' (today)")
        else:
            print(f"⏩ Skipping {url}, published '{date_text}' (not today)")
            return None

    return {"title": title, "content": content, "publish_date": publish_date}


# ---------------------------------------------------------------------
# Translation helper
# ---------------------------------------------------------------------
def translate_text(text, src="en", dest="ur"):
    parts = text.split("\n")
    translated_parts = []
    for part in parts:
        if part.strip():
            try:
                translated = translator.translate(part, src=src, dest=dest)
                translated_parts.append(translated.text)
            except Exception as e:
                print(f"⚠️ Translation failed: {e}")
                translated_parts.append(part)  # fallback to original
    return "\n".join(translated_parts)
