import sqlite3

DATABASE_PATH = "athi_agent.db"


def create_tasks_table():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


def add_task(user_id: int, task: str):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (user_id, task)
        VALUES (?, ?)
        """,
        (user_id, task),
    )

    connection.commit()
    connection.close()


def get_pending_tasks(user_id: int):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, task
        FROM tasks
        WHERE user_id = ?
        AND status = 'pending'
        ORDER BY created_at ASC
        """,
        (user_id,),
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


def complete_task(user_id: int, task_id: int):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET status = 'completed'
        WHERE id = ?
        AND user_id = ?
        """,
        (task_id, user_id),
    )

    connection.commit()

    updated_rows = cursor.rowcount

    connection.close()

    return updated_rows > 0

def find_pending_task(
    user_id: int,
    search_text: str,
):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, task
        FROM tasks
        WHERE user_id = ?
        AND status = 'pending'
        """,
        (user_id,),
    )

    rows = cursor.fetchall()

    connection.close()

    search_text = search_text.lower()

    for task_id, task in rows:
        task_lower = task.lower()

        if (
            search_text in task_lower
            or task_lower in search_text
        ):
            return task_id, task

        task_words = task_lower.split()

        for word in task_words:
            if (
                len(word) > 2
                and word in search_text
            ):
                return task_id, task

    return None
