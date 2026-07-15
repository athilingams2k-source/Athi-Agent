async def extract_weather_location(
    groq_client,
    user_message,
):
    prompt = f"""
Extract the city or location from the user's weather request.

User message:
{user_message}

Examples:

"What is the weather in Bangalore?"
Bangalore

"How is the weather in Chennai?"
Chennai

"Weather in Hyderabad"
Hyderabad

"Will it rain in Mumbai?"
Mumbai

"What is Bangalore weather today?"
Bangalore

If the user does not mention a city or location, return exactly:
NONE

Return only the location name.
Do not add explanation.
"""

    try:
        response = (
            await groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
        )

        location = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        if not location:
            return None

        if location.upper() == "NONE":
            return None

        return location

    except Exception as error:
        print(
            f"Weather location extraction failed: {error}"
        )

        return None