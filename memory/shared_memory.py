# memory/shared_memory.py
import sqlite3
from datetime import datetime

class SharedMemory:
    def __init__(self, db_path="shared_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                format TEXT,
                intent TEXT,
                timestamp TEXT,
                agent_output TEXT,
                thread_id TEXT
            )
        ''')
        self.conn.commit()

    def log(self, source, format_type, intent):
        timestamp = datetime.now().isoformat()
        self.conn.execute(
            'INSERT INTO logs (source, format, intent, timestamp) VALUES (?, ?, ?, ?)',
            (source, format_type, intent, timestamp)
        )
        self.conn.commit()

    def log_agent_output(self, source, format, intent, agent_output, timestamp, thread_id):
        # Store agent output and thread_id in the logs table
        self.conn.execute(
            'INSERT INTO logs (source, format, intent, timestamp, agent_output, thread_id) VALUES (?, ?, ?, ?, ?, ?)',
            (source, format, intent, timestamp, str(agent_output), thread_id)
        )
        self.conn.commit()
        print(f"[MEMORY] Logged agent output for {source} at {timestamp}")

    def close(self):
        self.conn.close()
