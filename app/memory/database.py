import sqlite3
from pathlib import Path


DATABASE_PATH = Path("athi_agent.db")


def create_database():
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            memory TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_memory(user_id: int, memory: str):
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM memories
        WHERE user_id = ?
        AND LOWER(memory) = LOWER(?)
        """,
        (user_id, memory),
    )

    existing_memory = cursor.fetchone()

    if existing_memory:
        connection.close()
        return False

    cursor.execute(
        """
        INSERT INTO memories (user_id, memory)
        VALUES (?, ?)
        """,
        (user_id, memory),
    )

    connection.commit()
    connection.close()

    return True


def get_memories(user_id: int):
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT memory
        FROM memories
        WHERE user_id = ?
        """,
        (user_id,),
    )

    rows = cursor.fetchall()

    connection.close()

    return [row[0] for row in rows]