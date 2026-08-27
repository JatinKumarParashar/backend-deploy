import sqlite3
import json
import os

DB_FILE = "spotify_memory.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Phase 3 & 6: User Memories Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        preference_artist TEXT,
        preference_genre TEXT,
        episode_mood TEXT,
        episode_activity TEXT,
        correction TEXT,
        exclusion TEXT,
        raw_statement TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Chat History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def save_detailed_memory(user_id: str, extracted_data: dict, raw_statement: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO user_memories (
        user_id, preference_artist, preference_genre,
        episode_mood, episode_activity, correction, exclusion, raw_statement
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        extracted_data.get("preference_artist"),
        extracted_data.get("preference_genre"),
        extracted_data.get("episode_mood"),
        extracted_data.get("episode_activity"),
        extracted_data.get("correction"),
        extracted_data.get("exclusion"),
        raw_statement
    ))
    conn.commit()
    conn.close()

def get_latest_user_memory(user_id: str):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM user_memories WHERE user_id = ? ORDER BY id DESC LIMIT 1
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def add_chat_message(user_id: str, role: str, content: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO chat_history (user_id, role, content) VALUES (?, ?, ?)
    """, (user_id, role, content))
    conn.commit()
    conn.close()
    return True

def get_chat_history(user_id: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM chat_history WHERE user_id = ? ORDER BY id ASC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

def clear_user_memories(user_id: str):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_memories WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error clearing memory: {e}")
        return False