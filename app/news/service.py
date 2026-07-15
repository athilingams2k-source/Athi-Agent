import html
import re
from urllib.parse import quote_plus
from xml.etree import ElementTree

import httpx


GOOGLE_NEWS_SEARCH_URL = "https://news.google.com/rss/search"
GOOGLE_NEWS_TOP_URL = "https://news.google.com/rss"


def clean_text(value: str) -> str:
    if not value:
        return ""

    value = html.unescape(value)

    # Remove HTML tags from RSS descriptions
    value = re.sub(r"<[^>]+>", " ", value)

    # Remove extra spaces
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def build_news_url(topic: str) -> str:
    cleaned_topic = topic.strip()

    if cleaned_topic.lower() == "general":
        return (
            f"{GOOGLE_NEWS_TOP_URL}"
            "?hl=en-IN&gl=IN&ceid=IN:en"
        )

    encoded_topic = quote_plus(cleaned_topic)

    return (
        f"{GOOGLE_NEWS_SEARCH_URL}"
        f"?q={encoded_topic}"
        "&hl=en-IN"
        "&gl=IN"
        "&ceid=IN:en"
    )


async def get_news(topic: str):
    news_url = build_news_url(topic)

    print(f"Fetching news topic: {topic}")

    try:
        async with httpx.AsyncClient(
            timeout=15.0,
            follow_redirects=True,
        ) as client:
            response = await client.get(
                news_url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "Athi-Agent/1.0"
                    )
                },
            )

            response.raise_for_status()

            rss_content = response.content

    except Exception as error:
        print(f"News request failed: {error}")
        return None

    try:
        root = ElementTree.fromstring(
            rss_content
        )

    except ElementTree.ParseError as error:
        print(
            f"News RSS parsing failed: {error}"
        )
        return None

    items = root.findall("./channel/item")

    if not items:
        print(
            f"No news found for topic: {topic}"
        )
        return None

    news_items = []

    for item in items[:8]:
        title_element = item.find("title")
        source_element = item.find("source")
        description_element = item.find(
            "description"
        )
        published_element = item.find(
            "pubDate"
        )

        title = clean_text(
            title_element.text
            if title_element is not None
            else ""
        )

        source = clean_text(
            source_element.text
            if source_element is not None
            else ""
        )

        description = clean_text(
            description_element.text
            if description_element is not None
            else ""
        )

        published = clean_text(
            published_element.text
            if published_element is not None
            else ""
        )

        if not title:
            continue

        news_items.append(
            {
                "title": title,
                "source": source,
                "description": description,
                "published": published,
            }
        )

    if not news_items:
        return None

    return news_items