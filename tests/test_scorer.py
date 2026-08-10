import unittest

from src.models import CandidatePost
from src.scorer import score_post


class TestScorer(unittest.TestCase):

    def test_good_developer_post_is_reply(self):
        post = CandidatePost(
            author="random_dev",
            text="Spent 6 hours debugging. The problem was a missing comma.",
            likes=42,
            replies=8,
            reposts=3,
        )

        result = score_post(post)

        self.assertEqual(result.decision, "REPLY")
        self.assertGreaterEqual(result.score, 60)

    def test_promotional_post_is_blocked(self):
        post = CandidatePost(
            author="crypto_sigma",
            text="BUY NOW! My coding course is 90% off. DM me. Link in bio.",
            likes=500,
            replies=100,
            reposts=50,
        )

        result = score_post(post)

        self.assertEqual(result.score, 0)
        self.assertEqual(result.decision, "SKIP")

    def test_css_post_is_not_ignored(self):
        post = CandidatePost(
            author="frontend_victim",
            text="CSS is easy until you need to center something.",
            likes=120,
            replies=14,
            reposts=9,
        )

        result = score_post(post)

        self.assertGreaterEqual(result.score, 35)
        self.assertNotEqual(result.decision, "SKIP")

    def test_generic_post_is_skipped(self):
        post = CandidatePost(
            author="morning_person",
            text="Good morning everyone ☀️",
            likes=3,
            replies=1,
            reposts=0,
        )

        result = score_post(post)

        self.assertEqual(result.decision, "SKIP")


if __name__ == "__main__":
    unittest.main()