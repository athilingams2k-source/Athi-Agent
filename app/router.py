async def detect_intent(
    groq_client,
    user_message: str,
):
    prompt = f"""
You are an intent classification system for a personal AI assistant.

Classify the user's message into exactly ONE of these intents:

ADD_TASK
LIST_TASKS
COMPLETE_TASK
ADD_REMINDER
GENERAL_CHAT

Rules:

ADD_REMINDER:
The user asks to be reminded and provides a specific time, date, or time duration.

Examples:
- Remind me to practice OData at 10 PM
- Remind me tomorrow at 7 PM to practice RAP
- Remind me in 30 minutes to drink water
- Remind me after 2 hours to call John
- Remind me on Friday at 9 AM to attend the meeting

ADD_TASK:
The user wants to add something to their task list or asks to be reminded without a specific time.

Examples:
- Add practice OData to my tasks
- Remind me to practice AMDP
- I need to practice CDS Views
- Add buy groceries to my task list

LIST_TASKS:
The user asks to view pending tasks.

Examples:
- What are my tasks?
- Show my tasks
- What do I need to do?
- What is pending?
- List my pending tasks

COMPLETE_TASK:
The user says a task is finished or completed.

Examples:
- I finished AMDP
- I completed OData
- CDS Views is done
- Mark AMDP as completed

GENERAL_CHAT:
Anything that does not match the intents above.

User message:
{user_message}

Return only the intent name.

Do not explain.
Do not add punctuation.
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

    intent = (
        response
        .choices[0]
        .message
        .content
        .strip()
        .upper()
    )

    valid_intents = {
        "ADD_TASK",
        "LIST_TASKS",
        "COMPLETE_TASK",
        "ADD_REMINDER",
        "GENERAL_CHAT",
    }

    if intent not in valid_intents:
        return "GENERAL_CHAT"

    return intent