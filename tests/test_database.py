import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.database import (
    create_post_key,
    get_candidate_status,
    init_db,
    save_candidate,
    update_candidate_status,
)
from src.models import CandidatePost, CandidateStatus
from src.scorer import score_post


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.db_patcher = patch(
            "src.database.DB_PATH",
            Path(self.temp_dir.name) / "test.db",
        )

        self.db_patcher.start()

        init_db()

        self.post = CandidatePost(
            author="debug_victim",
            text="Spent 4 hours debugging a Python bug.",
            likes=42,
            replies=8,
            reposts=2,
        )

        self.result = score_post(self.post)
        self.post_key = create_post_key(self.post)

        save_candidate(
            self.post,
            self.result,
        )

    def tearDown(self):
        self.db_patcher.stop()
        self.temp_dir.cleanup()

    def test_new_candidate_has_new_status(self):
        status = get_candidate_status(self.post_key)

        self.assertEqual(
            status,
            CandidateStatus.NEW,
        )

    def test_candidate_status_can_be_updated(self):
        updated = update_candidate_status(
            self.post_key,
            CandidateStatus.REPLIED,
        )

        self.assertTrue(updated)

        status = get_candidate_status(self.post_key)

        self.assertEqual(
            status,
            CandidateStatus.REPLIED,
        )

    def test_unknown_candidate_cannot_be_updated(self):
        updated = update_candidate_status(
            "missing-potato",
            CandidateStatus.SKIPPED,
        )

        self.assertFalse(updated)


if __name__ == "__main__":
    unittest.main()