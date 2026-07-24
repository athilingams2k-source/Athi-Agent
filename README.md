# 🤖 Athi-Agent

Athi-Agent is an AI-powered personal productivity assistant built with Python and Telegram.

It understands natural language, manages tasks, stores useful information, creates reminders, and provides intelligent assistance through a conversational interface.

The project is designed with a modular architecture, making it easy to extend with additional AI-powered capabilities such as weather updates, news summaries, voice interaction, web search, and more.

---

# ✨ Features

## 🧠 AI Memory

Store useful user preferences and information during conversations.

Examples:

- "I prefer remote work."
- "I enjoy learning Python."
- "My favorite programming language is Java."

The assistant can recall this information in future conversations.

Example:

> User: What programming language do I like?

> Athi-Agent: You enjoy learning Python.

---

## 📋 Task Management

Create and manage tasks using natural language.

Examples:

- "Add grocery shopping to my tasks."
- "I need to finish my assignment."
- "Create a task to call John."

View pending tasks:

- "What are my tasks?"
- "Show my to-do list."

Complete tasks naturally.

Example:

> User: I finished grocery shopping.

> Athi-Agent: Task completed: grocery shopping.

---

## ⏰ Smart Reminders

Create reminders using conversational language.

Relative reminders

> Remind me in 30 minutes to drink water.

Time-based reminders

> Remind me to join the meeting at 3 PM.

Scheduled reminders are automatically delivered through Telegram.

---

## 🌤️ Weather Updates

Get real-time weather information for any city.

Examples:

- "What's the weather today?"
- "Weather in London"
- "Will it rain in Chennai?"

The assistant returns current weather conditions including:

- Temperature
- Feels like
- Humidity
- Wind speed
- Weather condition

---

## 📰 AI News Summaries

Get concise AI-generated summaries of the latest news.

Examples:

- "Latest AI news"
- "News about OpenAI"
- "Technology news"

Instead of returning only links, Athi-Agent summarizes the latest headlines into an easy-to-read briefing.

---

## 🤖 AI Intent Detection

The assistant automatically understands user intent without requiring predefined commands.

Supported intents include:

- Memory Management
- Task Creation
- Task Listing
- Task Completion
- Reminder Creation
- Weather Requests
- News Requests
- General Conversation

---

# 🏗️ Project Structure

```text
Athi-Agent/
│
├── app/
│   ├── memory/
│   ├── reminders/
│   ├── tasks/
│   ├── weather/
│   ├── news/
│   ├── router.py
│   └── __init__.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🛠️ Technology Stack

- Python
- Telegram Bot API
- python-telegram-bot
- Groq API
- SQLite
- APScheduler
- HTTPX
- Python Dotenv

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/athilingams2k-source/Athi-Agent.git
```

Navigate into the project

```bash
cd Athi-Agent
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file.

```text
BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
```

Never commit secrets to Git.

---

# ▶️ Running Athi-Agent

```bash
python main.py
```

Expected output

```text
Athi Agent is running...
```

Start chatting with your Telegram bot.

---

# 🚀 Roadmap

Planned capabilities include:

- Voice Assistant
- Text-to-Speech
- Speech-to-Text
- Web Search
- Email Integration
- Calendar Management
- Daily Planner
- Recurring Reminders
- Long-term AI Memory
- Document Understanding
- Personal Knowledge Base
- AI Dashboard
- Multi-language Support

---

# 🔒 Security

The following files are excluded from version control:

```text
.env
.venv/
*.db
__pycache__/
```

Sensitive credentials should always remain outside the repository.

---

# 📌 Project Status

The project is under active development.

### ✅ Current Features

- AI Chat
- AI Memory
- Task Management
- Reminder Scheduling
- Weather Information
- AI News Summaries
- Intent Detection
- Telegram Integration

More modules will be added over time.

---

# 🤝 Contributing

Contributions, ideas, and feature requests are welcome.

Feel free to fork the repository, open issues, or submit pull requests.

---
