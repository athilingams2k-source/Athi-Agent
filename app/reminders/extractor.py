from datetime import datetime


async def extract_reminder(
    groq_client,
    user_message: str,
):
    current_time = datetime.now()

    prompt = f"""
You extract reminder information from user messages.

Current local date and time:
{current_time.strftime("%Y-%m-%d %H:%M:%S")}

User message:
{user_message}

Extract:
1. The reminder task.
2. The reminder date and time.

Understand expressions such as:
- at 10 PM
- tomorrow at 7 PM
- in 30 minutes
- in 2 hours

Return exactly in this format:

REMINDER: reminder text
TIME: YYYY-MM-DD HH:MM:SS

If the message does not contain a clear reminder time, return:

NONE

Do not add explanations.
"""

    response = await groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    result = response.choices[0].message.content.strip()

    if result == "NONE":
        return None

    reminder = None
    remind_at = None

    for line in result.splitlines():
        if line.startswith("REMINDER:"):
            reminder = line.replace(
                "REMINDER:",
                "",
                1,
            ).strip()

        elif line.startswith("TIME:"):
            remind_at = line.replace(
                "TIME:",
                "",
                1,
            ).strip()

    if not reminder or not remind_at:
        return None

    try:
        datetime.strptime(
            remind_at,
            "%Y-%m-%d %H:%M:%S",
        )
    except ValueError:
        return None

    return reminder, remind_at