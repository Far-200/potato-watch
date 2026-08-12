from enum import Enum

from pydantic import BaseModel


class CandidateStatus(str, Enum):
    NEW = "NEW"
    REPLIED = "REPLIED"
    SKIPPED = "SKIPPED"
    IGNORED = "IGNORED"


class CandidatePost(BaseModel):
    post_id: str | None = None
    author: str
    text: str
    likes: int = 0
    replies: int = 0
    reposts: int = 0


class ScoreResult(BaseModel):
    score: int
    decision: str
    reasons: list[str]