import hashlib
import sqlite3
from pathlib import Path
from src.models import CandidatePost, CandidateStatus, ScoreResult
from contextlib import contextmanager

DB_PATH = Path("data/potatowatch.db")

@contextmanager
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    try:
        with connection:
            yield connection
    finally:
        connection.close()
        
def create_post_key(post: CandidatePost) -> str:
    if post.post_id:
        return post.post_id
    raw = f"{post.author}:{post.text}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

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
                    post_key, author, text, likes, replies, reposts, score, decision
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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

def update_candidate_status(
    post_key: str,
    status: CandidateStatus,
) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE candidates SET status = ? WHERE post_key = ?",
            (
                status.value,
                post_key,
            ),
        )
        return cursor.rowcount > 0

def get_candidate_status(
    post_key: str,
) -> CandidateStatus | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT status FROM candidates WHERE post_key = ?",
            (post_key,),
        ).fetchone()
        if row is None:
            return None
        return CandidateStatus(row[0])
