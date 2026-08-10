from src.database import init_db, save_candidate
from src.models import CandidatePost
from src.scorer import score_post


def main():
    print("🥔 PotatoWatch is awake.")

    init_db()

    post = CandidatePost(
        author="random_dev",
        text="Spent 6 hours debugging. The problem was a missing comma.",
        likes=42,
        replies=8,
        reposts=3,
    )

    result = score_post(post)

    saved = save_candidate(post, result)

    if saved:
        print("🧠 New post remembered.")
    else:
        print("🥔 I already remember this post.")


if __name__ == "__main__":
    main()