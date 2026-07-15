from groq import AsyncGroq


async def extract_memory(
    groq_client: AsyncGroq,
    user_message: str,
):
    system_prompt = """
You are the memory manager for a personal AI assistant.

Analyze the user's message and decide whether it contains a useful
long-term personal fact about the user.

Save stable or useful information such as:
- Name
- Preferences
- Skills
- Career information
- Long-term goals
- Ongoing projects
- Important personal context

Do not save:
- Greetings
- Thanks
- General questions
- Coding questions
- Temporary requests
- AI-generated content
- Random conversation

If the message contains a useful long-term fact, return only the clean fact.

Example:
User: My name is Athi.
Return: My name is Athi

User: I prefer hybrid jobs.
Return: I prefer hybrid jobs

User: What is Python?
Return: NONE

User: Thanks.
Return: NONE

If there is no useful long-term personal fact, return exactly:
NONE
"""

    response = await groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
        temperature=0,
    )

    memory = response.choices[0].message.content

    if not memory:
        return None

    memory = memory.strip()

    if memory.upper() == "NONE":
        return None

    return memory