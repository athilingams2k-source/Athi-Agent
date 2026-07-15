import os
from datetime import datetime

from dotenv import load_dotenv
from groq import AsyncGroq
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from app.memory.database import (
    create_database,
    get_memories,
    save_memory,
)

from app.memory.extractor import extract_memory

from app.tasks.database import (
    add_task,
    complete_task,
    create_tasks_table,
    find_pending_task,
    get_pending_tasks,
)

from app.reminders.database import (
    add_reminder,
    complete_reminder,
    create_reminders_table,
    get_pending_reminders,
)


from app.weather.extractor import extract_weather_location
from app.weather.service import get_weather

from app.news.extractor import (
    extract_news_topic,
    summarize_news,
)
from app.news.service import get_news

from app.reminders.extractor import extract_reminder

from app.router import detect_intent


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


groq_client = AsyncGroq(
    api_key=GROQ_API_KEY
)


conversation_history = {}


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "Hello! 👋 I am Athi Agent."
    )


async def remember(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id

    memory = " ".join(context.args)

    if not memory:
        await update.message.reply_text(
            "Please tell me what to remember.\n\n"
            "Example: /remember My name is Athi"
        )
        return

    save_memory(
        user_id,
        memory,
    )

    await update.message.reply_text(
        f"🧠 I'll remember that: {memory}"
    )


async def addtask(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id

    task = " ".join(context.args)

    if not task:
        await update.message.reply_text(
            "Please tell me the task.\n\n"
            "Example: /addtask Practice CDS Views"
        )
        return

    add_task(
        user_id,
        task,
    )

    await update.message.reply_text(
        f"✅ Task added: {task}"
    )


async def tasks(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id

    pending_tasks = get_pending_tasks(
        user_id
    )

    if not pending_tasks:
        await update.message.reply_text(
            "🎉 You have no pending tasks."
        )
        return

    task_lines = []

    for task_id, task in pending_tasks:
        task_lines.append(
            f"{task_id}. {task}"
        )

    task_list = "\n".join(task_lines)

    await update.message.reply_text(
        "📋 Your pending tasks:\n\n"
        f"{task_list}"
    )


async def done(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text(
            "Please tell me the task ID.\n\n"
            "Example: /done 1"
        )
        return

    try:
        task_id = int(context.args[0])

    except ValueError:
        await update.message.reply_text(
            "Task ID must be a number.\n\n"
            "Example: /done 1"
        )
        return

    task_completed = complete_task(
        user_id,
        task_id,
    )

    if task_completed:
        await update.message.reply_text(
            f"✅ Task {task_id} marked as completed."
        )

    else:
        await update.message.reply_text(
            f"❌ Task {task_id} was not found."
        )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_message = update.message.text
    user_id = update.effective_user.id

    intent = await detect_intent(
        groq_client,
        user_message,
    )

    print(
        f"Detected intent: {intent}"
    )

    # -------------------------
    # REMINDER
    # -------------------------

    if intent == "ADD_REMINDER":
        reminder_data = await extract_reminder(
            groq_client,
            user_message,
        )

        if not reminder_data:
            await update.message.reply_text(
                "⏰ I couldn't understand the reminder time.\n\n"
                "Example: Remind me to practice OData at 10 PM"
            )
            return

        reminder, remind_at = reminder_data

        add_reminder(
            user_id,
            reminder,
            remind_at,
        )

        await update.message.reply_text(
            f"⏰ Reminder created: {reminder}\n"
            f"🕒 {remind_at}"
        )

        return

    # -------------------------
    # ADD TASK
    # -------------------------

    if intent == "ADD_TASK":
        task = user_message

        lower_message = user_message.lower()

        prefixes = [
            "add ",
            "add task ",
            "addtask ",
            "remind me to ",
            "i need to ",
            "i should ",
        ]

        for prefix in prefixes:
            if lower_message.startswith(prefix):
                task = user_message[len(prefix):]
                break

        suffixes = [
            " to my tasks",
            " to my task",
            " to tasks",
        ]

        for suffix in suffixes:
            if task.lower().endswith(suffix):
                task = task[:-len(suffix)]
                break

        task = task.strip()

        add_task(
            user_id,
            task,
        )

        await update.message.reply_text(
            f"✅ Task added: {task}"
        )

        return

    # -------------------------
    # COMPLETE TASK
    # -------------------------

    if intent == "COMPLETE_TASK":
        matched_task = find_pending_task(
            user_id,
            user_message,
        )

        if not matched_task:
            await update.message.reply_text(
                "🤔 I couldn't find a matching pending task."
            )
            return

        task_id, task_name = matched_task

        completed = complete_task(
            user_id,
            task_id,
        )

        if completed:
            await update.message.reply_text(
                f"✅ Task completed: {task_name}"
            )

        else:
            await update.message.reply_text(
                "❌ I couldn't complete that task."
            )

        return

    # -------------------------
    # LIST TASKS
    # -------------------------

    if intent == "LIST_TASKS":
        pending_tasks = get_pending_tasks(
            user_id
        )

        if not pending_tasks:
            await update.message.reply_text(
                "🎉 You have no pending tasks."
            )
            return

        task_lines = []

        for task_id, task in pending_tasks:
            task_lines.append(
                f"{task_id}. {task}"
            )

        task_text = "\n".join(task_lines)

        await update.message.reply_text(
            "📋 Your pending tasks:\n\n"
            f"{task_text}"
        )

        return

    # -------------------------
    # WEATHER
    # -------------------------

    if intent == "WEATHER":
        location = await extract_weather_location(
            groq_client,
            user_message,
        )

        if not location:
            await update.message.reply_text(
                "🌦️ Which city would you like the weather for?"
            )
            return

        weather = await get_weather(
            location
        )

        if not weather:
            await update.message.reply_text(
                f"⚠️ Sorry, I couldn't get the weather for {location}."
            )
            return

        await update.message.reply_text(
            weather
        )

        return
    
    if intent == "NEWS":
        topic = await extract_news_topic(
            groq_client,
            user_message,
        )

        if not topic:
            topic = "general"

        news_items = await get_news(topic)

        if not news_items:
            await update.message.reply_text(
                f"📰 Sorry, I couldn't get the latest news about {topic}."
            )
            return

        news_summary = await summarize_news(
            groq_client,
            topic,
            news_items,
        )

        if not news_summary:
            await update.message.reply_text(
                f"📰 I found news about {topic}, "
                "but I couldn't summarize it right now."
            )
            return

        await update.message.reply_text(
            news_summary
        )

        return
    
    

    # -------------------------
    # MEMORY EXTRACTION
    # -------------------------

    extracted_memory = await extract_memory(
        groq_client,
        user_message,
    )

    if extracted_memory:
        save_memory(
            user_id,
            extracted_memory,
        )

    memories = get_memories(
        user_id
    )

    memory_context = "\n".join(
        memories
    )

    # -------------------------
    # SYSTEM PROMPT
    # -------------------------

    system_prompt = f"""
You are Athi Agent, a personal AI assistant.

Known facts about the user:
{memory_context}

Use these known facts when they are relevant.

Do not claim to remember information that is not listed above.

Be helpful, conversational, and concise.
"""

    # -------------------------
    # CONVERSATION HISTORY
    # -------------------------

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    messages.extend(
        conversation_history[user_id]
    )

    # -------------------------
    # AI RESPONSE
    # -------------------------

    response = (
        await groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
        )
    )

    ai_reply = (
        response
        .choices[0]
        .message
        .content
    )

    conversation_history[user_id].append(
        {
            "role": "assistant",
            "content": ai_reply,
        }
    )

    await update.message.reply_text(
        ai_reply
    )


async def check_reminders(
    context: ContextTypes.DEFAULT_TYPE,
):
    current_time = datetime.now()

    pending_reminders = get_pending_reminders()

    for (
        reminder_id,
        user_id,
        reminder,
        remind_at,
    ) in pending_reminders:

        try:
            reminder_time = datetime.strptime(
                remind_at,
                "%Y-%m-%d %H:%M:%S",
            )

        except ValueError:
            print(
                f"Invalid reminder time: {remind_at}"
            )
            continue

        if reminder_time <= current_time:

            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"⏰ Reminder: {reminder}",
                )

                complete_reminder(
                    reminder_id
                )

                print(
                    f"Reminder sent: {reminder}"
                )

            except Exception as error:
                print(
                    f"Reminder send failed: {error}"
                )


def main():
    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN not found in .env"
        )

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found in .env"
        )

    create_database()
    create_tasks_table()
    create_reminders_table()

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.job_queue.run_repeating(
        check_reminders,
        interval=10,
        first=5,
    )

    app.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    app.add_handler(
        CommandHandler(
            "remember",
            remember,
        )
    )

    app.add_handler(
        CommandHandler(
            "addtask",
            addtask,
        )
    )

    app.add_handler(
        CommandHandler(
            "tasks",
            tasks,
        )
    )

    app.add_handler(
        CommandHandler(
            "done",
            done,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    print(
        "Athi Agent is running..."
    )

    app.run_polling()


if __name__ == "__main__":
    main()