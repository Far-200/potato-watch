from src.models import CandidatePost, ScoreResult


DEV_KEYWORDS = {
    "code",
    "coding",
    "developer",
    "debug",
    "debugging",
    "bug",
    "python",
    "javascript",
    "typescript",
    "react",
    "git",
    "github",
    "api",
    "docker",
    "linux",
    "programming",
    "compiler",
    "database",

    # Frontend / backend
    "css",
    "html",
    "frontend",
    "backend",
    "node",
    "npm",
}

PAIN_KEYWORDS = {
    "error",
    "failed",
    "broken",
    "hours",
    "why",
    "finally",
    "fix",
    "fixed",
    "problem",
    "issue",
    "crash",
}

PROMO_KEYWORDS = {
    "buy now",
    "limited offer",
    "discount",
    "course",
    "dm me",
    "link in bio",
    "giveaway",
    "subscribe",
}


def score_post(post: CandidatePost) -> ScoreResult:
    score = 0
    reasons = []

    text = post.text.lower()

    # Hard blocker: promotional content
    if any(keyword in text for keyword in PROMO_KEYWORDS):
        return ScoreResult(
            score=0,
            decision="SKIP",
            reasons=["BLOCKED: promotional content"],
        )

    # Developer relevance
    if any(keyword in text for keyword in DEV_KEYWORDS):
        score += 25
        reasons.append("+25 developer-related")

    # Relatable developer pain / humor potential
    if any(keyword in text for keyword in PAIN_KEYWORDS):
        score += 20
        reasons.append("+20 relatable pain")

    # Questions are naturally replyable
    if "?" in post.text:
        score += 15
        reasons.append("+15 asks a question")

    # Existing conversation
    if post.replies >= 3:
        score += 15
        reasons.append("+15 active conversation")

    # Healthy amount of engagement
    if 5 <= post.likes <= 500:
        score += 10
        reasons.append("+10 healthy engagement")

    # Short posts are easier to engage with
    if len(post.text) <= 280:
        score += 5
        reasons.append("+5 concise post")

    # Keep score inside 0–100
    score = max(0, min(score, 100))

    if score >= 60:
        decision = "REPLY"
    elif score >= 35:
        decision = "MAYBE"
    else:
        decision = "SKIP"

    return ScoreResult(
        score=score,
        decision=decision,
        reasons=reasons,
    )