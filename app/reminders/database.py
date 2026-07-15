import sqlite3


DATABASE_PATH = "athi_agent.db"


def create_reminders_table():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            reminder TEXT NOT NULL,
            remind_at TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
        """
    )

    connection.commit()
    connection.close()


def add_reminder(
    user_id: int,
    reminder: str,
    remind_at: str,
):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO reminders (
            user_id,
            reminder,
            remind_at
        )
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            reminder,
            remind_at,
        ),
    )

    connection.commit()
    connection.close()


def get_pending_reminders():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, user_id, reminder, remind_at
        FROM reminders
        WHERE status = 'pending'
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


def complete_reminder(reminder_id: int):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE reminders
        SET status = 'completed'
        WHERE id = ?
        """,
        (reminder_id,),
    )

    connection.commit()
    connection.close()