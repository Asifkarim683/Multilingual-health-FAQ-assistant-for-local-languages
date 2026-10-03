"""SQLite database layer for feedback storage and privacy-first query logs."""
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
import os

DB_PATH = Path(os.getenv("DATABASE_PATH", "data/health_assistant.db"))


def init_db(db_path: Path = DB_PATH):
    """Initialize SQLite database tables for logs and feedback."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS query_logs (
                request_id TEXT PRIMARY KEY,
                language TEXT,
                status TEXT,
                question_length INTEGER,
                citation_count INTEGER,
                timestamp TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT,
                rating TEXT,
                comment TEXT,
                timestamp TEXT,
                FOREIGN KEY (request_id) REFERENCES query_logs (request_id)
            )
            """
        )
        conn.commit()


def log_query(
    request_id: str,
    language: str,
    status: str,
    question_length: int,
    citation_count: int,
    db_path: Path = DB_PATH,
):
    """Log anonymized request metadata."""
    init_db(db_path)
    now = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO query_logs 
            (request_id, language, status, question_length, citation_count, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (request_id, language, status, question_length, citation_count, now),
        )
        conn.commit()


def save_feedback(
    request_id: str,
    rating: str,
    comment: Optional[str] = None,
    db_path: Path = DB_PATH,
):
    """Store user rating and comment."""
    init_db(db_path)
    now = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO feedback_logs (request_id, rating, comment, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (request_id, rating, comment, now),
        )
        conn.commit()
