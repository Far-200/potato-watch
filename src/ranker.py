from src.models import CandidatePost, ScoreResult
from src.scorer import score_post


def rank_posts(
    posts: list[CandidatePost],
) -> list[tuple[CandidatePost, ScoreResult]]:

    ranked_posts = []

    for post in posts:
        result = score_post(post)
        ranked_posts.append((post, result))

    ranked_posts.sort(
        key=lambda item: item[1].score,
        reverse=True,
    )

    return ranked_posts