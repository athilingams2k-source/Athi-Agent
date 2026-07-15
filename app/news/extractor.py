async def extract_news_topic(
    groq_client,
    user_message: str,
):
    prompt = f"""
You extract the news topic requested by a user.

USER MESSAGE:
{user_message}

Return only the topic to search for.

Examples:

User: Latest AI news
AI

User: Latest SAP news
SAP

User: Latest news about OpenAI
OpenAI

User: Latest AI news in India
AI India

User: What's happening in technology?
technology

User: Give me today's top news
general

User: Latest news
general

RULES:
- Return only the search topic.
- Do not explain.
- Do not use quotes.
- Keep important location words.
- If no specific topic is mentioned, return general.
"""

    try:
        response = await groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
            max_tokens=30,
        )

        topic = (
            response.choices[0]
            .message.content
            .strip()
        )

        if not topic:
            return "general"

        return topic

    except Exception as error:
        print(
            f"News topic extraction failed: {error}"
        )

        return "general"


async def summarize_news(
    groq_client,
    topic: str,
    news_items: list,
):
    if not news_items:
        return ""

    news_blocks = []

    for index, item in enumerate(
        news_items,
        start=1,
    ):
        title = item.get(
            "title",
            "",
        )

        source = item.get(
            "source",
            "",
        )

        if not title:
            continue

        news_blocks.append(
            (
                f"NEWS ITEM {index}\n"
                f"HEADLINE: {title}\n"
                f"SOURCE: {source}"
            )
        )

    if not news_blocks:
        return ""

    news_text = "\n\n".join(
        news_blocks
    )

    prompt = f"""
You are Athena, a personal AI news assistant.

The user asked for the latest news about:
{topic}

Below are recent news headlines collected from Google News RSS.

NEWS DATA:
{news_text}

Your task is to create a short, accurate news briefing
specifically about the user's requested topic.

IMPORTANT ACCURACY RULES:
- Use only information explicitly available in the headlines.
- Do not invent facts, dates, people, numbers, or events.
- Do not claim that a source "confirmed" something unless
  the headline explicitly says it was confirmed.
- Do not add background knowledge from memory.
- Do not make predictions.
- If multiple headlines describe the same event, combine them.
- Clearly distinguish allegations, reports, claims, and confirmed facts.
- Preserve words such as "reportedly", "claims", "may", and "plans".
- Ignore unrelated headlines.
- Never include URLs.
- Mention the source publication.
- Keep the response concise and easy to read.
- Prefer 3 important stories.
- Write for a Telegram chat.
- Do not use Markdown tables.

Use this exact general format:

📰 Latest {topic} News

1️⃣ <short topic heading>

<2 to 3 sentence factual summary>

Source: <source>

2️⃣ <short topic heading>

<2 to 3 sentence factual summary>

Source: <source>

3️⃣ <short topic heading>

<2 to 3 sentence factual summary>

Source: <source>

💡 Quick summary:
<short overall summary of the main developments>
"""

    try:
        response = await groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
            max_tokens=700,
        )

        summary = (
            response.choices[0]
            .message.content
            .strip()
        )

        return summary

    except Exception as error:
        print(
            f"News summarization failed: {error}"
        )

        return ""