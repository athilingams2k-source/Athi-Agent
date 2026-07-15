# 🤖 Athi-Agent

Athi-Agent is an AI-powered personal productivity assistant built with Python and Telegram.

The assistant is designed to understand natural language, remember useful information, manage tasks, and send scheduled reminders through Telegram.

The long-term goal is to build a modular personal AI assistant that can help users manage daily activities, information, and productivity from a single conversational interface.

## ✨ Features

### 🧠 AI Memory

Athi-Agent can extract and store useful information from conversations.

Examples:

- "I prefer hybrid jobs"
- "I am learning SAP RAP"
- "I like Python"

The assistant can recall stored information during future conversations.

Example:

> User: What type of jobs do I prefer?

> Athi-Agent: You prefer hybrid jobs.

### 📋 Task Management

Users can create tasks using natural language.

Examples:

- "Add practice OData to my tasks"
- "Remind me to practice AMDP"
- "I need to practice CDS Views"

Users can view pending tasks by asking:

- "What are my tasks?"
- "What do I need to do?"

Tasks can also be completed naturally.

Example:

> User: I finished AMDP

> Athi-Agent: Task completed: practice AMDP

### ⏰ Smart Reminders

Athi-Agent supports scheduled Telegram reminders.

Relative time reminders:

> Remind me in 1 minute to drink water

Clock-based reminders:

> Remind me to practice RAP at 10 PM

When the reminder time is reached, Athi-Agent automatically sends a Telegram notification.

### 🤖 AI Intent Detection

Athi-Agent uses AI-based intent detection to understand user requests.

Currently supported intents:

- `ADD_TASK`
- `LIST_TASKS`
- `COMPLETE_TASK`
- `ADD_REMINDER`
- `CHAT`

This allows users to interact with the assistant using normal conversational language instead of relying only on commands.

## 🏗️ Project Structure

```text
Athi-Agent/
│
├── app/
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── extractor.py
│   │
│   ├── reminders/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── extractor.py
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── database.py
│   │
│   ├── __init__.py
│   └── router.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md

🛠️ Technology Stack
Python
Telegram Bot API
python-telegram-bot
Groq API
SQLite
APScheduler
python-dotenv
⚙️ Installation

Clone the repository:
git clone https://github.com/athilingams2k-source/Athi-Agent.git

Navigate to the project directory:
cd Athi-Agent

Create a virtual environment:
python -m venv .venv

Activate the virtual environment.

Windows:
.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

🔐 Environment Variables

Create a .env file in the project root.

Add:
BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key

The .env file is excluded from Git using .gitignore.

Never commit API keys or bot tokens to the repository.

▶️ Running Athi-Agent

Start the bot:
python main.py

Expected terminal output:

Athi Agent is running...

Open Telegram and start chatting with the configured bot.

🗺️ Roadmap

Planned modules include:

Voice assistant
Web search
Weather updates
News summaries
Email integration
Telegram message assistance
Personal daily planning
Recurring reminders
Advanced long-term memory
Personal AI dashboard
🔒 Security

Sensitive local files are excluded from version control.

Examples:

.env
.venv/
*.db
__pycache__/

API keys and Telegram bot tokens must never be stored directly in source code.

📌 Project Status

Athi-Agent is currently under active development.

Completed modules:

AI conversation
AI memory
Task management
Natural language task completion
Smart reminder creation
Automatic Telegram reminder delivery
AI intent routing

More productivity and personal assistant capabilities will be added incrementally.

👨‍💻 Developer

Athilingam S

Building Athi-Agent as a modular AI-powered personal productivity assistant.

📄 License

This project is currently intended for learning, experimentation, and personal development.