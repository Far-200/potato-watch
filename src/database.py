import hashlib
import sqlite3
from pathlib import Path

from src.models import CandidatePost, ScoreResult


DB_PATH = Path("data/potatowatch.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(DB_PATH)


def create_post_key(post: CandidatePost) -> str:
    if post.post_id:
        return post.post_id

    raw = f"{post.author}:{post.text}"

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_key TEXT UNIQUE NOT NULL,
                author TEXT NOT NULL,
                text TEXT NOT NULL,
                likes INTEGER NOT NULL DEFAULT 0,
                replies INTEGER NOT NULL DEFAULT 0,
                reposts INTEGER NOT NULL DEFAULT 0,
                score INTEGER NOT NULL,
                decision TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'NEW',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_candidate(
    post: CandidatePost,
    result: ScoreResult,
) -> bool:

    post_key = create_post_key(post)

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO candidates (
                    post_key,
                    author,
                    text,
                    likes,
                    replies,
                    reposts,
                    score,
                    decision
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    post_key,
                    post.author,
                    post.text,
                    post.likes,
                    post.replies,
                    post.reposts,
                    result.score,
                    result.decision,
                ),
            )

        return True

    except sqlite3.IntegrityError:
        return False